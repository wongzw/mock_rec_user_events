import streamlit as st
import mock_user_event_app
import jsonl_app

PAGES = {
    "Event Generation": mock_user_event_app,
    "JSONL Converter": jsonl_app
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

page = PAGES[selection]

page.run()