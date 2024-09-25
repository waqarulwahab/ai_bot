import streamlit as st
from logics.logics import *
from airlines.pia import *
from airlines.airblue import *
from airlines.gulfair import *

# MAIN CODE
st.sidebar.title("Hack Any Airline")
st.sidebar.divider()


st.sidebar.page_link('main.py',                label="Home",          icon="🏠")
st.sidebar.page_link('pages/data_analyzer.py', label="Data Analyzer", icon="📚")
st.sidebar.page_link('pages/airlines.py',      label="Airlines",      icon="✈️")

st.sidebar.divider()



df = None
uploaded_file = st.sidebar.file_uploader("Upload a text file with URL", type=["csv"])
if uploaded_file is not None:
    st.sidebar.success("File Uploaded Successfully")
    df     = pd.read_csv(uploaded_file)
    df     = df.dropna(how='all')
    df     = df.drop(df.columns[0], axis=1)

    df     = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    df_len = len(df)
    
    duplicate_mask          = df.duplicated(subset=df.columns[1:], keep=False)
    unique_duplicates       = df[duplicate_mask].drop_duplicates(subset=df.columns[1:], keep=False)
    unique_duplicate_length = len(unique_duplicates)

    duplicates_rows    = df.drop_duplicates(subset=df.columns[1:], keep='first')
    drop_no_duplicates = len(duplicates_rows)

    total_duplicate = df_len - drop_no_duplicates

    st.write(f"{df_len} Total Rows and found {total_duplicate}")

    df_unique = duplicates_rows.drop_duplicates()

st.sidebar.title("Airline Companies")

options         = ["None","PIA", "Airblue", "Gulfair"]
selected_option = st.sidebar.radio("Choose any airline", options)


if selected_option is not "None":
    col1, col2 =  st.columns([1,1])
    with col1:
        display_data   = st.toggle("Display Accounts", value=True)
    with col2:
        process_status = st.toggle("Process Status")



if selected_option == "None":
    st.info(f"""Please first upload airlne data but 
            remeber all the data must be related to any one these
            {options}""")
    



#__________________________________PIA__________________________________
elif selected_option == "PIA":
    st.title("PIA Logins")
    try:
        if display_data:
            st.table(df_unique)
        elif process_status and uploaded_file:
            updated_df = account_status_process_for_pia(df_unique)
            st.table(updated_df)
            st.download_button(
                label="Download updated CSV",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name='updated_pia_credentials.csv',
                mime='text/csv'
            )
    except:
        pass


#__________________________________AIRBLUE__________________________________
elif selected_option == "Airblue":
    st.title("AIRBLUE Logins")
    try:
        if display_data:
            st.table(df_unique)
        elif process_status and uploaded_file:
            updated_df = account_status_process_for_airblue(df_unique)
            st.table(updated_df)
            st.download_button(
                label="Download updated CSV",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name='updated_airblue_credentials.csv',
                mime='text/csv'
            )
    except:
        pass


#__________________________________GULFAIR__________________________________
elif selected_option == "Gulfair":
    st.title("GULFAIR Logins")
    try:
        if display_data:
            st.table(df_unique)
        elif process_status and uploaded_file:
            updated_df = account_status_process_for_gulfair(df_unique)
            st.table(updated_df)
            st.download_button(
                label="Download updated CSV",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name='updated_gulfair_credentials.csv',
                mime='text/csv'
            )
    except:
        pass

