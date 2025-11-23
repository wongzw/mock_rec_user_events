import streamlit as st

import zipfile
import io

def run():
    st.title("JSONL File Splitter")

    uploaded_file = st.file_uploader("Upload a JSONL file", type="jsonl")
    lines_per_file = st.number_input("Number of lines per file", min_value=1, value=1000)

    if st.button("Split File"):
        if uploaded_file is not None:
            try:
                file_name = uploaded_file.name
                base_name = file_name.split(".")[0]

                string_data = uploaded_file.getvalue().decode("utf-8")
                lines = string_data.splitlines()
                
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                    for i in range(0, len(lines), lines_per_file):
                        chunk = lines[i:i + lines_per_file]
                        chunk_data = "\n".join(chunk)
                        zip_file.writestr(f"{base_name}_split_{i // lines_per_file + 1}.jsonl", chunk_data)
                
                zip_buffer.seek(0)
                st.download_button(
                    label="Download Split Files",
                    data=zip_buffer,
                    file_name=f"{base_name}_split.zip",
                    mime="application/zip"
                )
                st.success("File split and zipped successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")