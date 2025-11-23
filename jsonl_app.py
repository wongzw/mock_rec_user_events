import streamlit as st
import pandas as pd
import json
import xml.etree.ElementTree as ET
import yaml

def convert_to_jsonl(data, file_type):
    if file_type in ["csv", "excel", "tsv", "parquet"]:
        return data.to_json(orient="records", lines=True, force_ascii=False)
    elif file_type == "json":
        if isinstance(data, list):
            return "\n".join([json.dumps(record, ensure_ascii=False) for record in data])
        else:
            return json.dumps(data, ensure_ascii=False)
    elif file_type == "txt":
        return "\n".join([json.dumps({"line": line.strip()}, ensure_ascii=False) for line in data])
    elif file_type == "xml":
        return "\n".join([json.dumps({child.tag: child.text for child in record}, ensure_ascii=False) for record in data])
    elif file_type == "yaml":
        return "\n".join([json.dumps(record, ensure_ascii=False) for record in data])

def run():
    st.title("File to JSONL Converter")

    uploaded_file = st.file_uploader("Upload a CSV, JSON, TXT, Excel, XML, TSV, YAML or Parquet file", type=["csv", "json", "txt", "xlsx", "xml", "tsv", "yml", "yaml", "parquet"])

    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1]
        
        if file_extension == "csv":
            df = pd.read_csv(uploaded_file, encoding='utf-8')
            jsonl_data = convert_to_jsonl(df, "csv")
        elif file_extension == "tsv":
            df = pd.read_csv(uploaded_file, encoding='utf-8', sep='\t')
            jsonl_data = convert_to_jsonl(df, "tsv")
        elif file_extension == "xlsx":
            df = pd.read_excel(uploaded_file)
            jsonl_data = convert_to_jsonl(df, "excel")
        elif file_extension == "json":
            data = json.load(uploaded_file)
            jsonl_data = convert_to_jsonl(data, "json")
        elif file_extension == "txt":
            data = uploaded_file.read().decode("utf-8").splitlines()
            jsonl_data = convert_to_jsonl(data, "txt")
        elif file_extension == "xml":
            tree = ET.parse(uploaded_file)
            root = tree.getroot()
            jsonl_data = convert_to_jsonl(root, "xml")
        elif file_extension in ["yml", "yaml"]:
            data = yaml.safe_load(uploaded_file)
            jsonl_data = convert_to_jsonl(data, "yaml")
        elif file_extension == "parquet":
            df = pd.read_parquet(uploaded_file)
            jsonl_data = convert_to_jsonl(df, "parquet")
            
        st.download_button(
            label="Download JSONL",
            data=jsonl_data,
            file_name=f"{uploaded_file.name.split('.')[0]}.jsonl",
            mime="application/jsonl",
        )