import streamlit as st
from translation import get_translation


import zipfile
import io

def run():
    st.title(get_translation("jsonl_splitter_title"))

    uploaded_file = st.file_uploader(get_translation("upload_jsonl"), type="jsonl")
    lines_per_file = st.number_input(get_translation("lines_per_file"), min_value=1, value=1000)

    if st.button(get_translation("split_file_button")):
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
                    label=get_translation("download_split_files"),
                    data=zip_buffer,
                    file_name=f"{base_name}_split.zip",
                    mime="application/zip"
                )
                st.success(get_translation("split_success_message"))
            except Exception as e:
                st.error(get_translation("error_message").format(e=e))