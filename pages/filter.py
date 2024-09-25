import streamlit as st
import pandas as pd
import os

st.sidebar.page_link('main.py', label="Home", icon="🏠")
st.sidebar.page_link('pages/filter.py', label="Manage Filter", icon="🔍")
st.sidebar.divider()

def update_csv_file(keyword, file_path):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        if keyword not in df['Keywords'].values:
            new_row = pd.DataFrame({'Keywords': [keyword]})
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(file_path, index=False)
            st.success(f"Keyword '{keyword}' added to the CSV file.")
        else:
            st.warning(f"Keyword '{keyword}' already exists in the CSV file.")
    else:
        df = pd.DataFrame({'Keywords': [keyword]})
        df.to_csv(file_path, index=False)
        st.success(f"CSV file created and keyword '{keyword}' added.")


def remove_keyword_from_csv_file(keyword, file_path):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        if keyword in df['Keywords'].values:
            df = df[df['Keywords'] != keyword]
            df.to_csv(file_path, index=False)
            st.success(f"Keyword '{keyword}' removed from the CSV file.")
        else:
            st.warning(f"Keyword '{keyword}' not found in the CSV file.")
    else:
        st.error(f"CSV file '{file_path}' does not exist.")


# MAIN CODE

st.title("Filter Your Data")
st.divider()
csv_file = 'filter_keywords.csv'

 
add_filter_keyword    = st.sidebar.toggle("Add Filter Keyword")
remove_filter_keyword = st.sidebar.toggle("Remove Filter Keyword")
display_all_filters   = st.sidebar.toggle("Display Filters", value=True)


if add_filter_keyword:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        add_filter_in_list = st.text_input("Add Filter Keyword")
    with col2:
        pass
    with col3:
        pass
    with col4:
        pass

    submit_filter = st.button("Add Filter")
    if submit_filter:
        update_csv_file(add_filter_in_list, csv_file)


elif remove_filter_keyword:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        remove_filter_in_list = st.text_input("Remove Filter Keyword")
    with col2:
        pass
    with col3:
        pass
    with col4:
        pass

    remove_filter = st.button("Remove Filter")
    if remove_filter:
        remove_keyword_from_csv_file(remove_filter_in_list, csv_file)

else:
    if display_all_filters:
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            st.table(df)






