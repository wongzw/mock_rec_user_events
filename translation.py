import streamlit as st
import json

@st.cache_data(ttl= 300)
def load_translations():
    with open('./translations.json', 'r', encoding='utf-8') as f:
        return json.load(f)

TRANSLATIONS = load_translations()

def get_translation(key):
    lang = st.session_state.get('language', 'en')
    return TRANSLATIONS.get(lang, {}).get(key, key)
