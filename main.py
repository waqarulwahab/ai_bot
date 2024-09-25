import streamlit as st
import pandas as pd
from io import StringIO
from logics.logics import *
from plots.visualize_status import visualize_status_plot


st.set_page_config(layout="wide")


# MAIN CODE

st.sidebar.title("Data Analytics App")
st.sidebar.divider()

st.sidebar.page_link('main.py',                label="Home",          icon="🏠")
st.sidebar.page_link('pages/filter.py',        label="Manage Filter", icon="🔍")
st.sidebar.page_link('pages/data_analyzer.py', label="Data Analyzer", icon="📚")
st.sidebar.page_link('pages/split_data.py',    label="SPLIT DATA",    icon="➗")
st.sidebar.page_link('pages/merge_data.py',    label="MERGE DATA",    icon="➕")
st.sidebar.page_link('pages/airlines.py',      label="Airline",       icon="✈️")
st.sidebar.page_link('pages/resturents.py',    label="Resturents",    icon="🍽️")
st.sidebar.divider()

credentials_status_file = 'credentials_status.csv'

total_urls           = None
total_apply_filter   = None
total_filter_records = None
df                   = None

# Multi-file uploader in the sidebar
uploaded_files = st.sidebar.file_uploader("Upload text or CSV files with URLs", type=["txt", "csv"], accept_multiple_files=True)

if uploaded_files:
    all_dfs = []  # List to hold DataFrames from each CSV file
    total_urls = 0

    for uploaded_file in uploaded_files:
        # Check if the file is a text file
        if uploaded_file.type == 'text/plain':
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            input_data = stringio.read()
            st.sidebar.success(f"Text File '{uploaded_file.name}' Uploaded Successfully")
            # Process the text file (assuming `process_data` is a function you define)
            # df here can be None if text files are not processed into a DataFrame
            df = process_data(input_data)
            if df is not None:
                all_dfs.append(df)
                total_urls += len(df)

        # Check if the file is a CSV file
        elif uploaded_file.type == 'text/csv':
            st.sidebar.success(f"CSV File '{uploaded_file.name}' Uploaded Successfully")
            df = pd.read_csv(uploaded_file)
            df = df.dropna(how='all')  # Drop rows that are entirely NaN
            all_dfs.append(df)
            total_urls += len(df)

    # After processing all files, you can combine DataFrames or do other operations
    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)  # Combine all DataFrames into one
        # st.write(f"Total URLs Processed: {total_urls}")
        # st.write(combined_df)

    if df is not None:
        total_urls = len(combined_df)

    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        check_actual_data         = st.toggle("Display Actual Data", key="check_actual_data")
    with col2:
        check_active_credentials  = st.toggle("Check Credentials", key="check_active_credentials")
    with col3:
        analysis_of_credentials   = st.toggle("Analysis Credentials", key="analysis_credentials")

    st.sidebar.divider()
    filter_keyword_list = load_filter_keywords()
    filter_keywords     = st.sidebar.multiselect("Keywords:", options=filter_keyword_list)


    if filter_keywords:
        # Filter based on all selected keywords
        filtered_df = combined_df[combined_df['url'].apply(lambda x: any(keyword in x for keyword in filter_keywords))]
        filtered_df = pd.DataFrame(filtered_df)
        total_apply_filter   = len(filter_keywords)
        total_filter_records = len(filtered_df)
        title = """"""
    else:
        title = """No Specific Filter is Apply"""
        filtered_df = combined_df


    
    if check_actual_data:
        actual_data(input_data)
    elif check_active_credentials:
        all_status = asyncio.run(check_credentials_async(filtered_df, credentials_status_file))
    elif analysis_of_credentials:
        df = pd.read_csv("credentials_status.csv")
        valid_df   = df[df['status'] == "Valid"]
        invalid_df = df[df['status'] == "Invalid"]
        other_status_df = df[~df['status'].isin(['Valid', 'Invalid'])]


        total_valid_credentials   = len(valid_df)
        total_invalid_credentials = len(invalid_df)
        total_filter_records      = len(df)

        top_information_for_status(total_filter_records, total_valid_credentials, total_invalid_credentials)

        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            display_all_status     = st.checkbox("Display All Status")
        with col2:
            display_valid_status   = st.checkbox("Display Valid Status")
        with col3:
            display_invalid_status = st.checkbox("Display Invalid Status")
        with col4:
            visualize_status       = st.checkbox("Visualize Status", value=True)
        with col5:
            pass
        with col6:
            pass

        if display_all_status:
            st.write("All Status:")
            st.dataframe(df)
            st.divider()

        col1, col2 = st.columns(2)
        with col1:
            if display_valid_status:
                st.write("Only Valid:")
                st.dataframe(valid_df)
            else:
                pass
        
        with col2:
            if display_invalid_status:
                st.write("Only Invalid:")
                st.dataframe(invalid_df)
            else:
                pass  

        if visualize_status:
            visualize_status_plot(valid_df, invalid_df, other_status_df)


    else:
        top_information(total_urls, total_filter_records, total_apply_filter)
        st.write("Filtered Data:", title)
        st.dataframe(filtered_df)
        st.divider()
else:
    st.warning("Upload Any .txt file that contains url links for analysis")