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
                
                # Reset file pointer to the beginning
                uploaded_file.seek(0)
                
                zip_buffer = io.BytesIO()
                
                with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                    chunk = []
                    chunk_count = 1

                    # Stream the file line-by-line to prevent Out-of-Memory crashes
                    for line_bytes in uploaded_file:
                        line_text = line_bytes.decode("utf-8")
                        chunk.append(line_text)
                        
                        if len(chunk) == lines_per_file:
                            chunk_data = "".join(chunk)
                            zip_file.writestr(f"{base_name}_split_{chunk_count}.jsonl", chunk_data)
                            chunk = []
                            chunk_count += 1
                    
                    # Write any remaining lines left in the final chunk
                    if chunk:
                        chunk_data = "".join(chunk)
                        zip_file.writestr(f"{base_name}_split_{chunk_count}.jsonl", chunk_data)
                
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