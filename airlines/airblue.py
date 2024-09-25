import streamlit as st
from bs4 import BeautifulSoup
import requests
import tempfile
import threading
import os


def delete_file_after_delay(file_path, delay=120):
    def delete_file():
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                st.write(f"{file_path} has been deleted after {delay} seconds.")
        except Exception as e:
            st.error(f"Error deleting file: {e}")
    timer = threading.Timer(delay, delete_file)
    timer.start()



def account_status_process_for_airblue(df):
    st.title('LOGS')

    df['Account Status'] = ''

    for index, row in df.iterrows():
        username = row['username']
        password = row['password']

        st.write(f"{index+1} - Attempting login for Username: {username} and {password}")

        if username and password:
            with requests.Session() as session:
                try:
                    login_url = 'https://www.airblue.com/agents/default.asp'
                    response_get = session.get(login_url)

                    soup = BeautifulSoup(response_get.text, 'html.parser')
                    imagecheck_value = soup.find('input', {'name': 'imagecheck'})['value']

                    form_data = {
                        'login': username,
                        'password': password,
                        'ta_login_action': 'dologin',
                        'email_password': '',
                        'imagecheck': imagecheck_value
                    }

                    response_post = session.post(login_url, data=form_data)

                    if "Incorrect Login or Password" in response_post.text:
                        st.error(f"Login failed for {username}.")
                        df.at[index, 'Account Status'] = 'Invalid'
                    elif "Login Locked" in response_post.text:
                        st.warning(f"Account is locked for {username}.")
                        df.at[index, 'Account Status'] = 'Login Locked'
                    elif "Welcome" in response_post.text or "Logout" in response_post.text:
                        st.success(f"Login successful for {username}!")
                        df.at[index, 'Account Status'] = 'Valid'
                        protected_url = 'https://www.airblue.com/agents/protected_page'
                        protected_page = session.get(protected_url)
                        st.write(protected_page.text)
                    else:
                        st.error(f"Unexpected response for {username}.")
                        df.at[index, 'Account Status'] = 'Unexpected Response'
                
                except Exception as e:
                    st.error(f"An error occurred for {username}: {e}")
                    df.at[index, 'Account Status'] = f'Error: {e}'
        else:
            st.warning(f"Missing username or password for row {index}.")
            df.at[index, 'Account Status'] = 'Missing Credentials'
    st.divider()

    with tempfile.NamedTemporaryFile(delete=False, suffix="airblue.csv") as temp_file:
        df.to_csv(temp_file.name, index=False)
        temp_file_path = temp_file.name
        st.warning(f"Temporary CSV file Created at: {temp_file_path}")

    return df