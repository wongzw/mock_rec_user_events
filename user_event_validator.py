import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

@st.cache_data
def load_translations():
    with open('./translations.json', 'r', encoding='utf-8') as f:
        return json.load(f)

TRANSLATIONS = load_translations()

def get_translation(key):
    lang = st.session_state.get('language', 'en')
    return TRANSLATIONS.get(lang, {}).get(key, key)

def run():
    plt.rcParams['font.family'] = ['Heiti TC']
    st.title(get_translation("user_event_validation_title"))



    uploaded_file = st.file_uploader(get_translation("choose_jsonl"), type="jsonl")


    if uploaded_file is not None:
        lines = uploaded_file.getvalue().decode("utf-8").splitlines()
        try:
            first_line = json.loads(lines[0])
            schema = list(first_line.keys())
        except (json.JSONDecodeError, IndexError):
            st.error(get_translation("invalid_jsonl"))
            st.stop()

        st.subheader(get_translation("configure_fields"))
        user_id_field = st.selectbox(get_translation("user_id_field"), schema, index=1 if len(schema) > 1 else 0)
        item_id_field = st.selectbox(get_translation("item_id_field"), schema, index=2 if len(schema) > 2 else 0)
        event_type_field = st.selectbox(get_translation("event_type_field"), schema, index=0)
        timestamp_field = st.selectbox(get_translation("timestamp_field"), schema, index=3 if len(schema) > 3 else 0)

        data = [json.loads(line) for line in lines]
        df = pd.DataFrame(data)

        st.subheader(get_translation("configure_event_types"))
        all_event_types = df[event_type_field].unique().tolist()
        exposure_event_types = st.multiselect(get_translation("select_exposure_event_types"), all_event_types)

        st.subheader(get_translation("high_heat_recall_logic_configuration"))
        time_frame_days = st.number_input(get_translation("time_frame_days"), min_value=1, value=1, max_value=7)
        high_heat_event_types = st.multiselect(get_translation("select_high_heat_event_types"), all_event_types)

        if st.button(get_translation("run_validation")):
            timestamps = pd.to_numeric(df[timestamp_field])
            if timestamps.mean() > 1e12:
                timestamps = pd.to_datetime(timestamps, unit='ms')
            else:
                timestamps = pd.to_datetime(timestamps, unit='s')

            validation_results = {}

            # 1. Are the configured fields all strings?
            for field in [event_type_field, user_id_field, item_id_field]:
                if df[field].dtype != 'object':
                    validation_results[get_translation("field_is_string").format(field=field)] = get_translation("fail_field_not_string").format(field=field, dtype=df[field].dtype)
                else:
                    validation_results[get_translation("field_is_string").format(field=field)] = get_translation("pass")

            # Is the event timestamp in unix milisecond or second timestamp?
            try:
                pd.to_numeric(df[timestamp_field])
                if df[timestamp_field].mean() > 1e12:
                    validation_results[get_translation("timestamp_format")] = get_translation("pass_unix_milliseconds")
                else:
                    validation_results[get_translation("timestamp_format")] = get_translation("pass_unix_seconds")
            except (ValueError, TypeError):
                invalid_timestamps = pd.to_numeric(df[timestamp_field], errors='coerce').isna()
                first_invalid_timestamp = df[timestamp_field][invalid_timestamps].iloc[0]
                validation_results[get_translation("timestamp_format")] = get_translation("fail_invalid_timestamp").format(first_invalid_timestamp=first_invalid_timestamp)

            # Recent events (within 7 days)
            now = datetime.now(timestamps.dt.tz)
            seven_days_ago = now - timedelta(days=7)
            recent_events = df[(timestamps > seven_days_ago) & (~df[event_type_field].isin(exposure_event_types))]
            if len(recent_events) > 0:
                validation_results[get_translation("events_within_last_7_days")] = get_translation("pass_events_found").format(num_events=len(recent_events))
                validation_results[get_translation("users_with_events_within_last_7_days")] = get_translation("pass_users_found").format(num_users=recent_events[user_id_field].nunique())
            else:
                validation_results[get_translation("events_within_last_7_days")] = get_translation("fail_no_events_found_7_days")
                validation_results[get_translation("users_with_events_within_last_7_days")] = get_translation("fail_no_users_found_7_days")
            
            # High-heat recall logic validation
            high_heat_time_window = now - timedelta(days=time_frame_days)
            high_heat_events = df[(timestamps > high_heat_time_window) & (df[event_type_field].isin(high_heat_event_types))]
            if len(high_heat_events) > 0:
                validation_results[get_translation("high_heat_recall")] = get_translation("pass_high_heat_recall").format(num_events=len(high_heat_events))
            else:
                validation_results[get_translation("high_heat_recall")] = get_translation("fail_high_heat_recall")

            st.subheader(get_translation("validation_results"))

            for key, value in validation_results.items():
                if get_translation("pass") in value:
                    st.success(f"{key}: {value}")
                else:
                    st.error(f"{key}: {value.replace(get_translation('fail'), '')}")

            # 2. Number of users
            st.subheader(get_translation("user_counts"))
            num_users = df[user_id_field].nunique()
            user_event_types = df.groupby(user_id_field)[event_type_field].unique().apply(set)
            users_with_only_exposure = user_event_types[user_event_types.apply(lambda x: x.issubset(set(exposure_event_types)))].index
            num_users_only_exposure = len(users_with_only_exposure)
            users_with_other_events = user_event_types[user_event_types.apply(lambda x: not x.issubset(set(exposure_event_types)))].index
            num_users_with_other_events = len(users_with_other_events)

            if num_users_with_other_events == 0:
                st.error(get_translation("fail_zero_users_with_non_exposure_events"))
            
            col1, col2, col3 = st.columns(3)
            col1.metric(get_translation("total_users"), num_users)
            col2.metric(get_translation("users_with_only_exposure_events"), num_users_only_exposure)
            col3.metric(get_translation("users_with_more_than_just_exposure_events"), num_users_with_other_events)



            # 5. Distribution of users in each event type
            st.subheader(get_translation("event_type_distribution"))
            event_type_counts = df.groupby(event_type_field)[user_id_field].nunique()
            st.bar_chart(event_type_counts)

            # 6. Distribution of user events according to event timestamp
            st.subheader(get_translation("event_timestamp_distribution"))
            fig, ax = plt.subplots()
            timestamps.hist(ax=ax, bins=50)
            ax.set_title(get_translation("event_timestamp_distribution"))
            ax.set_xlabel(get_translation("timestamp"))
            ax.set_ylabel(get_translation("frequency"))
            st.pyplot(fig)

            # 7. Any other validation that is important
            st.subheader(get_translation("additional_validations"))
            if df.isnull().values.any():
                st.warning(get_translation("missing_values_detected"))
                st.write(df.isnull().sum())
            else:
                st.success(get_translation("no_missing_values_detected"))