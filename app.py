import streamlit as st
import json
import random
from datetime import datetime, date, timedelta


import pandas as pd

st.set_page_config(layout="wide")

def get_schema_from_file(uploaded_file):
    if not uploaded_file:
        return []
    uploaded_file.seek(0)
    first_line = uploaded_file.readline()
    uploaded_file.seek(0)
    try:
        return list(json.loads(first_line).keys())
    except (json.JSONDecodeError, AttributeError):
        return []



@st.cache_data
def load_translations():
    with open('/Users/bytedance/Documents/0sample/translations.json', 'r', encoding='utf-8') as f:
        return json.load(f)

TRANSLATIONS = load_translations()

def get_translation(key):
    lang = st.session_state.get('language', 'en')
    return TRANSLATIONS.get(lang, {}).get(key, key)

def initialize_session_state():
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    if 'user_flows' not in st.session_state:
        st.session_state.user_flows = get_default_flows()
    if 'generated_events' not in st.session_state:
        st.session_state.generated_events = None
    if 'user_journeys' not in st.session_state:
        st.session_state.user_journeys = None
    if 'language' not in st.session_state:
        st.session_state.language = 'en'

def get_default_flows(industry='E-commerce'):
    if industry == 'E-commerce':
        flows = [
            {
                'name': 'Browser/Window Shopper',
                'flow': [
                    {'event': 'Product View (Impression)', 'likelihood_of_progressing_to_next_step': 1.0},
                    {'event': 'Product Click', 'likelihood_of_progressing_to_next_step': 0.7},
                    {'event': 'Add to Wishlist', 'likelihood_of_progressing_to_next_step': 0.4},
                    {'event': 'Share Product', 'likelihood_of_progressing_to_next_step': 0.2}
                ],
                'weight': 0.4
            },
            {
                'name': 'Social Shopper',
                'flow': [
                    {'event': 'Product View (Impression)', 'likelihood_of_progressing_to_next_step': 1.0},
                    {'event': 'Product Click', 'likelihood_of_progressing_to_next_step': 0.8},
                    {'event': 'Like Product', 'likelihood_of_progressing_to_next_step': 0.6},
                    {'event': 'Share Product', 'likelihood_of_progressing_to_next_step': 0.5},
                    {'event': 'Follow Brand', 'likelihood_of_progressing_to_next_step': 0.3}
                ],
                'weight': 0.3
            },
            {
                'name': 'Purchaser',
                'flow': [
                    {'event': 'Product View (Impression)', 'likelihood_of_progressing_to_next_step': 1.0},
                    {'event': 'Product Click', 'likelihood_of_progressing_to_next_step': 0.9},
                    {'event': 'Add to Cart', 'likelihood_of_progressing_to_next_step': 0.4},
                    {'event': 'Initiate Checkout', 'likelihood_of_progressing_to_next_step': 0.6},
                    {'event': 'Complete Purchase', 'likelihood_of_progressing_to_next_step': 0.8}
                ],
                'weight': 0.3
            }
        ]
    elif industry == 'Stock Image Platform':
        flows = [
            {
                'name': 'Free User',
                'flow': [
                    {'event': 'View Image', 'likelihood_of_progressing_to_next_step': 1.0},
                    {'event': 'Search Images', 'likelihood_of_progressing_to_next_step': 0.8},
                    {'event': 'Download Watermarked Preview', 'likelihood_of_progressing_to_next_step': 0.5},
                    {'event': 'Create Free Account', 'likelihood_of_progressing_to_next_step': 0.15}
                ],
                'weight': 0.6
            },
            {
                'name': 'Subscriber',
                'flow': [
                    {'event': 'View Image', 'likelihood_of_progressing_to_next_step': 1.0},
                    {'event': 'Search Images', 'likelihood_of_progressing_to_next_step': 0.9},
                    {'event': 'Download High-Resolution Image', 'likelihood_of_progressing_to_next_step': 0.7},
                    {'event': 'Add to Collection', 'likelihood_of_progressing_to_next_step': 0.4},
                    {'event': 'License Extended Usage', 'likelihood_of_progressing_to_next_step': 0.25},
                    {'event': 'Share Collection', 'likelihood_of_progressing_to_next_step': 0.15}
                ],
                'weight': 0.4
            }
        ]
    elif industry == 'Video Platform':
        flows = [
            {
                'name': 'Casual Viewer',
                'flow': [
                    {'event': 'Watch Video', 'likelihood_of_progressing_to_next_step': 1.0},
                    {'event': 'Like Video', 'likelihood_of_progressing_to_next_step': 0.5},
                    {'event': 'Subscribe to Channel', 'likelihood_of_progressing_to_next_step': 0.2},
                    {'event': 'Save to Watch Later', 'likelihood_of_progressing_to_next_step': 0.3}
                ],
                'weight': 0.7
            },
            {
                'name': 'Power User',
                'flow': [
                    {'event': 'Watch Video', 'likelihood_of_progressing_to_next_step': 1.0},
                    {'event': 'Like Video', 'likelihood_of_progressing_to_next_step': 0.8},
                    {'event': 'Comment on Video', 'likelihood_of_progressing_to_next_step': 0.6},
                    {'event': 'Share Video', 'likelihood_of_progressing_to_next_step': 0.4},
                    {'event': 'Add to Playlist', 'likelihood_of_progressing_to_next_step': 0.3},
                    {'event': 'Create Video Response', 'likelihood_of_progressing_to_next_step': 0.15},
                    {'event': 'Download Video', 'likelihood_of_progressing_to_next_step': 0.1}
                ],
                'weight': 0.3
            }
        ]
    elif industry == 'Social Networking':
        flows = [
            {
                'name': 'Lurker',
                'flow': [
                    {'event': 'View Post', 'likelihood_of_progressing_to_next_step': 1.0},
                    {'event': 'Like Post', 'likelihood_of_progressing_to_next_step': 0.3},
                    {'event': 'Read Comments', 'likelihood_of_progressing_to_next_step': 0.4}
                ],
                'weight': 0.5
            },
            {
                'name': 'Engaged User',
                'flow': [
                    {'event': 'View Post', 'likelihood_of_progressing_to_next_step': 1.0},
                    {'event': 'Like Post', 'likelihood_of_progressing_to_next_step': 0.8},
                    {'event': 'Comment on Post', 'likelihood_of_progressing_to_next_step': 0.5},
                    {'event': 'Share Post', 'likelihood_of_progressing_to_next_step': 0.3},
                    {'event': 'Follow User', 'likelihood_of_progressing_to_next_step': 0.2},
                    {'event': 'Send Direct Message', 'likelihood_of_progressing_to_next_step': 0.25},
                    {'event': 'Create Post', 'likelihood_of_progressing_to_next_step': 0.2}
                ],
                'weight': 0.5
            }
        ]
    else:
        flows = []
    for flow in flows:
        flow['id'] = random.randint(1, 1000000)
        for step in flow['flow']:
            step['id'] = random.randint(1, 1000000)

    return flows

def step1_upload():
    lang = st.session_state.get('language', 'en')
    st.session_state.language = st.radio(
        get_translation("language"), 
        options=list(TRANSLATIONS.keys()), 
        format_func=lambda x: "English" if x == 'en' else "中文",
        horizontal=True,
        index=0 if lang == 'en' else 1,
        on_change=lambda: st.session_state.__setitem__('language', st.session_state.language)
    )

    st.header(get_translation("step1_header"))
    st.markdown(get_translation("step1_subheader"))

    uploaded_file = st.file_uploader(get_translation("upload_label"), type=["jsonl"], label_visibility="collapsed")

    if uploaded_file:
        st.session_state.uploaded_file = uploaded_file
        st.success(get_translation("upload_success"))

    st.markdown("---")
    if st.button(get_translation("next_to_configure_flows"), use_container_width=True, disabled=not st.session_state.uploaded_file):
        st.session_state.current_step = 2
        st.rerun()

def step2_configure_flows():
    st.header(get_translation("step2_header"))
    st.info(get_translation("step2_info"))

    industries = ['E-commerce', 'Stock Image Platform', 'Video Platform', 'Social Networking']
    selected_industry = st.selectbox(get_translation("industry_select_label"), industries, key='industry_select')

    if st.session_state.get('selected_industry') != selected_industry:
        st.session_state.selected_industry = selected_industry
        st.session_state.user_flows = get_default_flows(selected_industry)
        st.rerun()

    st.subheader(get_translation("flow_distribution_header"))

    # --- Flow Configuration ---
    for i, flow in enumerate(st.session_state.user_flows):
        # Make each journey collapsible
        with st.expander(f"{get_translation(f'flow_name:{flow['name']}')} ({flow['weight']:.0%})", expanded=st.session_state.get(f"flow_expanded_{flow['id']}", True)):
            # Journey Header
            header_cols = st.columns([0.8, 0.2])
            with header_cols[0]:
                st.text_input(get_translation("journey_name_label"), value=flow['name'], key=f"flow_name_{flow['id']}")
            with header_cols[1]:
                if st.button(get_translation("delete_journey_button"), key=f"delete_flow_{flow['id']}", use_container_width=True):
                    st.session_state.user_.pop(i)
                    st.rerun()

            # Journey Weight
            flow['weight'] = st.slider(
                get_translation("journey_weight_label"), 0.0, 1.0, flow['weight'], 0.05, key=f"flow_weight_{flow['id']}",
                label_visibility="collapsed"
            )

            # Journey Steps
            st.markdown(f"**{get_translation('journey_steps_header')}**")
            for j, step in enumerate(flow['flow']):
                step_cols = st.columns([0.6, 0.3, 0.1])
                with step_cols[0]:
                    all_events = [event for key, event in TRANSLATIONS[st.session_state.language].items() if key.startswith("event_name:")]
                    try:
                        event_index = all_events.index(get_translation(f"event_name:{step['event']}"))
                    except ValueError:
                        event_index = 0
                    selected_event_display = st.selectbox(
                        get_translation("step_event_label"),
                        all_events,
                        index=event_index,
                        key=f"event_type_{flow['id']}_{step['id']}"
                    )
                    # Find the original English event name
                    for key, value in TRANSLATIONS[st.session_state.language].items():
                        if value == selected_event_display:
                            step['event'] = key.replace("event_name:", "")
                            break
                    step['event'] = selected_event_display
                with step_cols[1]:
                    step['likelihood_of_progressing_to_next_step'] = st.slider(
                        get_translation("step_likelihood_label"), 0.0, 1.0,
                        step['likelihood_of_progressing_to_next_step'], 0.05,
                        key=f"event_likelihood_{flow['id']}_{step['id']}"
                    )
                with step_cols[2]:
                    if st.button(get_translation("delete_step_button"), key=f"delete_step_{flow['id']}_{step['id']}", use_container_width=True):
                        flow['flow'].pop(j)
                        st.rerun()

            if st.button(get_translation("add_step_button"), key=f"add_step_{flow['id']}", use_container_width=True):
                new_step = {'event': 'new_event', 'likelihood_of_progressing_to_next_step': 1.0, 'id': random.randint(1, 1000000)}
                flow['flow'].append(new_step)
                st.rerun()

    # --- Total Weight Check ---
    total_weight = sum(f['weight'] for f in st.session_state.user_flows)
    if abs(total_weight - 1.0) > 1e-9:
        st.warning(get_translation("total_weight_error").format(total_weight=total_weight))
    else:
        st.success(get_translation("total_weight_success").format(total_weight=total_weight))

    # --- Add/Reset Buttons ---
    footer_cols = st.columns([0.5, 0.5])
    with footer_cols[0]:
        if st.button(get_translation("add_flow_button"), use_container_width=True):
            new_flow = {
                'name': f'New Flow {len(st.session_state.user_flows) + 1}',
                'flow': [{'event': 'new_event', 'likelihood_of_progressing_to_next_step': 1.0, 'id': random.randint(1, 1000000)}],
                'weight': 0.0,
                'id': random.randint(1, 1000000)
            }
            st.session_state.user_flows.append(new_flow)
            st.rerun()
    with footer_cols[1]:
        if st.button(get_translation("reset_flows_button"), use_container_width=True):
            st.session_state.user_flows = get_default_flows(st.session_state.get('selected_industry', 'E-commerce'))
            st.rerun()

    st.markdown("---")

    # --- Navigation Buttons ---
    nav_cols = st.columns([0.5, 0.5])
    with nav_cols[0]:
        if st.button(get_translation("back_to_upload_button"), use_container_width=True):
            st.session_state.current_step = 1
            st.rerun()
    with nav_cols[1]:
        if st.button(get_translation("next_to_generate_button"), use_container_width=True):
            total_weight = sum(f['weight'] for f in st.session_state.user_flows)
            if abs(total_weight - 1.0) > 1e-9:
                st.error(get_translation("total_weight_error").format(total_weight=total_weight))
            else:
                st.session_state.current_step = 3
                st.rerun()

def step3_generate_events():
    st.header(get_translation("step3_header"))
    st.markdown(get_translation("step3_subheader"))

    if not st.session_state.uploaded_file:
        st.error(get_translation("upload_error"))
        if st.button(get_translation("back_to_upload_button")):
            st.session_state.current_step = 1
            st.rerun()
        return

    # --- Time Window ---
    st.subheader(get_translation("time_window_header"))
    st.info(get_translation("time_window_info"))
    time_cols = st.columns(4)
    start_date = time_cols[0].date_input(get_translation("start_date_label"), date.today() - timedelta(days=7))
    start_time = time_cols[1].time_input(get_translation("start_time_label"))
    end_date = time_cols[2].date_input(get_translation("end_date_label"), date.today())
    end_time = time_cols[3].time_input(get_translation("end_time_label"))

    start_datetime = datetime.combine(start_date, start_time)
    end_datetime = datetime.combine(end_date, end_time)

    if start_datetime >= end_datetime:
        st.error(get_translation("date_error"))

    days_difference = (date.today() - end_date).days
    if days_difference > 7:
        st.warning(get_translation("date_warning").format(days_difference=days_difference))

    # --- User and Event Settings ---
    st.subheader(get_translation("user_settings_header"))
    setting_cols = st.columns(2)
    num_users = setting_cols[0].number_input(get_translation("num_users_label"), min_value=1, value=1000)
    flows_per_user = setting_cols[1].number_input(get_translation("flows_per_user_label"), min_value=1, value=3)

    # --- Product ID Configuration ---
    st.subheader(get_translation("product_id_header"))
    schema = get_schema_from_file(st.session_state.uploaded_file)
    if schema:
        product_id_field = st.selectbox(get_translation("product_id_select_label"), schema)
    else:
        st.warning(get_translation("schema_warning"))
        product_id_field = st.text_input(get_translation("product_id_select_label"))

    st.markdown("---")

    # --- Navigation and Generation ---
    nav_cols = st.columns([0.5, 0.5])
    with nav_cols[0]:
        if st.button(get_translation("back_to_configure_button"), use_container_width=True):
            st.session_state.current_step = 2
            st.rerun()

    with nav_cols[1]:
        if st.button(get_translation("generate_events_button"), use_container_width=True):
            # Read product IDs from the uploaded file
            st.session_state.uploaded_file.seek(0)
            product_ids = [json.loads(line).get(product_id_field) for line in st.session_state.uploaded_file]
            product_ids = [pid for pid in product_ids if pid]

            if not product_ids:
                st.error(get_translation("product_id_error"))
            else:
                with st.spinner(get_translation("generating_spinner")):
                    events, user_journeys = generate_events(
                        st.session_state.user_flows,
                        num_users,
                        flows_per_user,
                        start_datetime,
                        end_datetime,
                        product_ids
                    )
                    st.session_state.generated_events = events
                    st.session_state.user_journeys = user_journeys
                st.success(get_translation("generation_success").format(event_count=len(st.session_state.generated_events)))

    if st.session_state.generated_events:
        st.subheader(get_translation("analysis_header"))
        
        # Create a pandas DataFrame from the generated events
        df = pd.DataFrame(st.session_state.generated_events)

        # Translate event types for charting
        df['translated_event_type'] = df['event_type'].apply(lambda x: get_translation(f"event_name:{x}"))

        st.subheader(get_translation("user_journey_analysis_header"))
        user_journey_counts = pd.Series(st.session_state.user_journeys).value_counts()
        user_journey_counts.index = [get_translation(f'flow_name:{name}') for name in user_journey_counts.index]
        st.bar_chart(user_journey_counts)

        # --- Event Counts Chart ---
        st.subheader(get_translation("Event Counts"))
        event_counts = df['translated_event_type'].value_counts().sort_index()
        st.bar_chart(event_counts)

        # --- Events Over Time Chart ---
        st.subheader(get_translation("Events Over Time"))
        df['event_timestamp'] = pd.to_datetime(df['event_timestamp'], unit='ms')
        events_over_time = df.set_index('event_timestamp').resample('h')['event_type'].count()
        st.line_chart(events_over_time)

        if st.button(get_translation("restart_button")):
            st.session_state.clear()
            initialize_session_state()
            st.rerun()

def generate_events(flows, num_users, flows_per_user, start_datetime, end_datetime, product_ids):
    events = []
    user_journeys = []
    start_timestamp = int(start_datetime.timestamp() * 1000)
    end_timestamp = int(end_datetime.timestamp() * 1000)

    flow_names = [flow['name'] for flow in flows]
    flow_weights = [flow['weight'] for flow in flows]

    for user_id in range(num_users):
        for _ in range(flows_per_user):
            # Choose a flow based on weight
            chosen_flow_name = random.choices(flow_names, weights=flow_weights, k=1)[0]
            chosen_flow = next(flow for flow in flows if flow['name'] == chosen_flow_name)
            user_journeys.append(chosen_flow_name)

            # Generate events for the chosen flow
            for step in chosen_flow['flow']:
                if random.random() <= step['likelihood_of_progressing_to_next_step']:
                    event = {
                        "user_id": str(user_id),
                        "event_type": step['event'],
                        "event_timestamp": random.randint(start_timestamp, end_timestamp),
                        "product_id": random.choice(product_ids)
                    }
                    events.append(event)
                else:
                    break  # User drops off
    return events, user_journeys

def main():
    initialize_session_state()

    if st.session_state.current_step == 1:
        step1_upload()
    elif st.session_state.current_step == 2:
        step2_configure_flows()
    elif st.session_state.current_step == 3:
        step3_generate_events()

if __name__ == "__main__":
    main()