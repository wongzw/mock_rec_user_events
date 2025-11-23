import streamlit as st
import pandas as pd
import json

def convert_to_jsonl(data, file_type):
    if file_type == "csv":
        return data.to_json(orient="records", lines=True, force_ascii=False)
    elif file_type == "json":
        if isinstance(data, list):
            return "\n".join([json.dumps(record, ensure_ascii=False) for record in data])
        else:
            return json.dumps(data, ensure_ascii=False)
    elif file_type == "txt":
        return "\n".join([json.dumps({"line": line.strip()}, ensure_ascii=False) for line in data])

def run():
    st.title("File to JSONL Converter")

    uploaded_file = st.file_uploader("Upload a CSV, JSON, or TXT file", type=["csv", "json", "txt"])

    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1]
        
        if file_extension == "csv":
            df = pd.read_csv(uploaded_file, encoding='utf-8')
            jsonl_data = convert_to_jsonl(df, "csv")
        elif file_extension == "json":
            data = json.load(uploaded_file)
            jsonl_data = convert_to_jsonl(data, "json")
        elif file_extension == "txt":
            data = uploaded_file.read().decode("utf-8").splitlines()
            jsonl_data = convert_to_jsonl(data, "txt")
            
        st.download_button(
            label="Download JSONL",
            data=jsonl_data,
            file_name=f"{uploaded_file.name.split('.')[0]}.jsonl",
            mime="application/jsonl",
        )