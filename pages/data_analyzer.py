import streamlit as st
import pandas as pd


st.sidebar.page_link('main.py',                label="Home",          icon="🏠")
st.sidebar.page_link('pages/data_analyzer.py', label="Data Analyzer", icon="📚")



df = None
uploaded_file = st.sidebar.file_uploader("Upload CSV file to analyze", type=["csv"])
if uploaded_file is not None:
    st.sidebar.success("File Uploaded Successfully")
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)


    display_locked_accounts = st.sidebar.checkbox("Locked Accounts")
    if display_locked_accounts:
        try:
            df_locked = df[df['Account Status'] == "Login Locked"]
            total_locked_accounts = len(df_locked)
            st.write(f"**Total Locked Accounts are: {total_locked_accounts}")
            st.dataframe(df_locked)
            st.divider()
        except:
            st.warning("There is no Account Status in current CSV")
            
    valid_accounts = st.sidebar.checkbox("Valid Accounts")
    if valid_accounts:
        try:
            df_valid = df[df['Account Status'] == "Valid"]
            total_valid_accounts = len(df_valid)
            st.write(f"**Total Valid Accounts are: {total_valid_accounts}")
            st.dataframe(df_valid)
            st.divider()
        except:
            st.warning("There is no Account Status in current CSV")

    invalid_accounts = st.sidebar.checkbox("Invalid")
    if invalid_accounts:
        try:
            df_invalid = df[df['Account Status'] == "Invalid"]
            total_invalid_accounts = len(df_invalid)
            st.write(f"**Total Inalid Accounts are: {total_invalid_accounts}")
            st.dataframe(df_invalid)
            st.divider()
        except:
            st.warning("There is no Account Status in current CSV")