import streamlit as st
import mock_user_event_app
import jsonl_app
from translation import get_translation, TRANSLATIONS
import jsonl_splitter_app
import user_event_validator

PAGES = {
    "Event Generation": mock_user_event_app,
    "JSONL Converter": jsonl_app,
    "JSONL Splitter": jsonl_splitter_app,
    "User Event Validator": user_event_validator
}

st.sidebar.title(get_translation('sidebar_title'))

lang = st.session_state.get('language', 'en')
st.session_state.language = st.sidebar.radio(
    get_translation("language"), 
    options=list(TRANSLATIONS.keys()), 
    format_func=lambda x: "English" if x == 'en' else "中文",
    horizontal=True,
    index=0 if lang == 'en' else 1,
)

page_keys = list(PAGES.keys())
translated_page_names = [get_translation(key) for key in page_keys]
translated_to_original_map = {translated: original for translated, original in zip(translated_page_names, page_keys)}

selection_translated = st.sidebar.radio(get_translation("go_to"), translated_page_names)
selected_key = translated_to_original_map[selection_translated]

page = PAGES[selected_key]

page.run()