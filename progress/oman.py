import execjs
import streamlit as st
import requests

# Load the CryptoJS library from a CDN or file
CRYPTO_JS = """
    var CryptoJS = require("crypto-js");

    function encryptPassword(password, key) {
        var ciphertext = CryptoJS.AES.encrypt(password, key).toString();
        return ciphertext;
    }
"""

# Initialize the JS runtime
ctx = execjs.compile(CRYPTO_JS)

# Streamlit app
st.title("Sindbad Login with CryptoJS")

# Input fields for Sindbad number/email and password
sindbad_number = st.text_input("Sindbad number or Email", value="e.moroni60@gmail.com")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if sindbad_number and password:
        try:
            # Use the CryptoJS function to encrypt the password
            encrypted_password = ctx.call("encryptPassword", password, "some_key")
            st.write(f"Encrypted Password (CryptoJS): {encrypted_password}")

            # Define the form data to be sent in the POST request
            form_data = {
                "errorFlag": "",
                "sindbadno": sindbad_number,  # Replace with your actual Sindbad number or email
                "password": encrypted_password,  # Use the encrypted password
                "Login": "Login"
            }

            # Define the headers (mimicking a real browser request)
            headers = {
                "Host": "sindbad.omanair.com",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Referer": "https://sindbad.omanair.com/SindbadProd/login",
                "Content-Type": "application/x-www-form-urlencoded",
                "Origin": "https://sindbad.omanair.com",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            }

            # Define the login URL
            login_url = "https://sindbad.omanair.com/SindbadProd/loginProcess"

            # Send the POST request to the login URL with the form data and headers
            response = requests.post(login_url, headers=headers, data=form_data)

            # Output the response (status code and text)
            st.write(f"Response Status Code: {response.status_code}")
            st.write(f"Response Text: {response.text}")

        except Exception as e:
            st.error(f"An error occurred: {e}")
