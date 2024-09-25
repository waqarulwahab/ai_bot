import streamlit as st
import pandas as pd

st.sidebar.page_link('main.py', label="Home", icon="🏠")
st.sidebar.page_link('pages/filter.py', label="Manage Filter", icon="🔍")
st.sidebar.page_link('pages/airblue.py', label="AIRBLUE", icon="🔍")
st.sidebar.page_link('pages/split_data.py', label="SPLIT DATA", icon="➗")
st.sidebar.page_link('pages/merge_data.py', label="MERGE DATA", icon="➕")
st.sidebar.divider()



st.title('Upload Multiple CSV Files')
st.divider()

uploaded_files = st.sidebar.file_uploader("Choose CSV files", type="csv", accept_multiple_files=True)


dfs = []
total_records = 0

if uploaded_files:
    merge_button = st.sidebar.toggle("Merger All Data")

    for uploaded_file in uploaded_files:
        df = pd.read_csv(uploaded_file)
        dfs.append(df)

        num_records = len(df)
        total_records += num_records
        st.sidebar.success(f"**File name:** {uploaded_file.name}")
        display_data = st.checkbox(f"**File name:** {uploaded_file.name} | **Total Records in this file:** {num_records}", key=f"{uploaded_file.name}")
        if display_data:    
            st.dataframe(df)
            st.divider()
    st.write(f"**Total Record of All files:** {total_records}")
    st.divider()


    if merge_button:
        if dfs:
            merged_df = pd.concat(dfs, ignore_index=True)
            
            st.write("Merged DataFrame:")
            st.dataframe(merged_df)

            merged_csv = merged_df.to_csv(index=False)
            st.success("Data Merge Successfully")
            st.download_button(label="Download Merged CSV", data=merged_csv, file_name=f'{uploaded_file.name}-merged_file.csv', mime='text/csv')
        else:
            st.write("No files to merge.")




# Waqar.Wahab@Wiki122837,  93 - Attempting login for Username: zohaibhassan1 and lheskt88