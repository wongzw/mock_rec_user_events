import streamlit as st
import json
import os

@st.cache_data(ttl= 30)
def load_translations():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'translations.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

TRANSLATIONS = load_translations()

def get_translation(key):
    lang = st.session_state.get('language', 'en')
    return TRANSLATIONS.get(lang, {}).get(key, key)
