import streamlit as st
import mock_user_event_app
import jsonl_app
import jsonl_splitter_app

PAGES = {
    "Event Generation": mock_user_event_app,
    "JSONL Converter": jsonl_app,
    "JSONL Splitter": jsonl_splitter_app
}

st.sidebar.title('AI Search Tool Kit!')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

page = PAGES[selection]

page.run()