import streamlit as st
from io import StringIO
import io
import zipfile
from logics.logics import process_data, info_display_box


st.sidebar.page_link('main.py', label="Home", icon="🏠")
st.sidebar.page_link('pages/filter.py', label="Manage Filter", icon="🔍")
st.sidebar.page_link('pages/airblue.py', label="AIRBLUE", icon="🔍")
st.sidebar.page_link('pages/split_data.py', label="SPLIT DATA", icon="➗")
st.sidebar.page_link('pages/merge_data.py', label="MERGE DATA", icon="➕")
st.sidebar.page_link('pages/test.py', label="TEST", icon="🔍")
st.sidebar.divider()




def split_dataframe_to_zip(df, number_of_files, zip_file_name="csv_files.zip"):
    chunk_size = len(df) // number_of_files
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for i in range(number_of_files):
            start_idx = i * chunk_size
            if i == number_of_files - 1:
                chunk = df[start_idx:]  # Last chunk
            else:
                chunk = df[start_idx:start_idx + chunk_size]
            csv_data = chunk.to_csv(index=False)
            zip_file.writestr(f"{uploaded_file.name}_chunk_{i+1}.csv", csv_data)
    zip_buffer.seek(0)
    return zip_buffer




uploaded_file = st.sidebar.file_uploader("Upload a text file with URL", type=["txt"])
if uploaded_file is not None:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    input_data = stringio.read()

    st.sidebar.success("File Uploaded Successfully")

    df = process_data(input_data)
    total_urls = len(df)

    col1, col2 = st.sidebar.columns(2)
    with col1:
        no_of_splits      = st.number_input("Select Splits Number", min_value=2, max_value=20, step=1)
    with col2:
        pass
    
    record_per_splits = int(total_urls / no_of_splits)

    col1, col2, col3 = st.columns(3)
    with col1:
        try:
            label = ""
            value = total_urls
            info  = "Records"
            info_display_box(label, value, info)
        except:
            pass
    with col2:
        try:
            label = ""
            value = no_of_splits
            info  = "No Of Splits"
            info_display_box(label, value, info)
        except:
            pass
    with col3:
        try:
            label = ""
            value = record_per_splits
            info  = "Records Per Splits"
            info_display_box(label, value, info)
        except:
            pass


    st.write("Filtered Data:")
    st.dataframe(df.head())
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        split_data = st.button("Split Data")
    with col2:
        if split_data:
            zip_file = split_dataframe_to_zip(df, no_of_splits)

            st.download_button(
                label=f"Download Zip File",
                data=zip_file,
                file_name=f"{uploaded_file.name}_chunks.zip",
                mime="application/zip"
            )