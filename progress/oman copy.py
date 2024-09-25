import streamlit as st
import requests
import tempfile
import threading
import os
from bs4 import BeautifulSoup



sindbadno = st.text_input("Username", value="e.moroni60@gmail.com")
password  = st.text_input("Password", type="password", value="Parmalat2023@")


if st.button("Login"):
    if sindbadno and password:
        with requests.Session() as session:
            try:
                login_url = 'https://sindbad.omanair.com/SindbadProd/loginProcess'
                response_get = session.get(login_url)


                headers = {
                    "Host": "sindbad.omanair.com",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br, zstd",
                    "Referer": "https://sindbad.omanair.com/SindbadProd/login?errorType=1&atLeft=5",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Origin": "https://sindbad.omanair.com",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1"
                }


                form_data = {
                    "errorFlag": "",
                    "sindbadno": sindbadno,
                    "password": password,
                    "Login": "Login"
                }

                response_post = requests.post(login_url, headers=headers, data=form_data)
                st.write(response_post)
                st.write(response_post.text)
            except Exception as e:
                st.error(f"An error occurred for {sindbadno}: {e}")



# https://sindbad.omanair.com/SindbadProd/memberHome

# www.omanair.com/it/en
# e.moroni60@gmail.com
# Parmalat2023@



# https://sindbad.omanair.com/SindbadProd/memberHome?_gl=1*17hi915*_gcl_au*NjU0MTI5MTM1LjE3MjU2Mzg5MzU.
# mahmoud.alshukaili@gmail.com
# 3MotionMahmoud#202






# POST REQUEST:
# https://sindbad.omanair.com/SindbadProd/loginProcess




# ACTUAL
# Parmalat2023@ -------> U2FsdGVkX1+QXwZJdJsYZOg35CJh0zuKf6c2/2Q+wTI=


# 1jQdukM4nYyCyoJZtgWkYQ==