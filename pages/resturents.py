import streamlit as st
import pandas as pd
from resturants.hilton import *

# MAIN CODE
st.sidebar.title("Hack Any Resturents")
st.sidebar.divider()


st.sidebar.page_link('main.py',                label="Home",          icon="🏠")
st.sidebar.page_link('pages/data_analyzer.py', label="Data Analyzer", icon="📚")
st.sidebar.page_link('pages/resturents.py',    label="Resturents",    icon="🍽️")

st.sidebar.divider()

df = None
uploaded_file = st.sidebar.file_uploader("Upload a text file with URL", type=["csv"])
if uploaded_file is not None:
    st.sidebar.success("File Uploaded Successfully")
    df = pd.read_csv(uploaded_file)
    df = df.dropna(how='all')

    df_no_duplicates = df.drop_duplicates(subset=df.columns[1:], keep='first')
    num_duplicates = len(df_no_duplicates)
    if num_duplicates > 0:
        st.write(f"{num_duplicates} duplicate rows have been deleted: ")
        df = df_no_duplicates.drop_duplicates()




    

st.sidebar.title("Resturents")

options         = ["None","Hilton"]
selected_option = st.sidebar.radio("Choose any resturents", options)


if selected_option is not "None":
    col1, col2 =  st.columns([1,1])
    with col1:
        display_data   = st.toggle("Display Accounts", value=True)
    with col2:
        process_status = st.toggle("Process Status")


if selected_option == "None":
    st.info(f"""Please first upload resturents data but 
            remeber all the data must be related to any one these
            {options}""")

#__________________________________PIA__________________________________
elif selected_option == "Hilton":
    if display_data:
        st.table(df)
    elif process_status and uploaded_file:
        updated_df = account_status_process_for_hilton(df)
        st.table(updated_df)
        st.download_button(
            label="Download updated CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name='updated_hilton_credentials.csv',
            mime='text/csv'
        )


