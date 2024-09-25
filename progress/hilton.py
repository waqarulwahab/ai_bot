import streamlit as st        
import requests
import random


username = st.text_input("USERNAME" , value='550165646')
password = st.text_input("PASSWORD" , type='password', value='Ifeyinwa1')

if st.button("LOGIN"):

    user_identifier = username

    if user_identifier and password:
        with requests.Session() as session:
            try:    
                login_url = 'https://secure3.hilton.com/en/hi/customer/login/index.htm'
                response_get = session.get(login_url)

                form_data = {
                    'username': user_identifier,
                    'password': password,
                }

                cookies = {
                    "_abck": "CCD67C1C8BE013E51A50BFED589D66EB~-1~YAAQFLQRYPkH7/+RAQAAjNT8CwySI2wy9UVJK/Kd5OBchLkyfj9mE6/yox7CD9XnAIfipUemwXZJodfGUtQicHp7r0lQLRx/MYwx5iw0KgE4Xg0JNSLYBMBZFH8KDB4vzi4ti0ly/G8oy3aQu9HaH4WmKsbn6W9gUIHAPIPgrvdkXqfSf23s0lyvypQJcxieVIOI1WMdkfHXfA9uG29HEgBbhiwnQ5pnLxT2IjiTxA04Exaaj1lmP+kDK/pxdVGufwRDHgsotMSI5EUE+EZWUh4vC1wd3ZnaSz1A6/O4ND3naD+MEjqa50jngqVGj1vDTF6BYzRduztVxAZHM2sfEycyiJkSttfAaNaXV0zdatStjRjIPJ+zctZG+NODRFs7b/1xq/HA64I9tpeIWSx/pOeRC0Qld1nClxI2XRjwkfujAif6wKiWPRUJrFL6N97zD5+VFlHNjKKo2aFulH5xMgukvbwZX0WHzwEPa9DGiscjj5mJlknsMZpoW5ywGYeVzZoFvmzGu4mo/uDdX+Mkl5s2fo6w6ev/1OBCLnn4C5LlkDeissLaM3Z/kfQurw==~0~-1~1726778589",
                    "ak_bmsc": "193AD792DCAED67BD96E6957783AF623~000000000000000000000000000000~YAAQFLQRYPiU5f+RAQAACvehCxmYKCW5cUMJvi13c/WUaI440z6IQgj7RVS5YlUXrGwVdA6xocCu6i32YFIfIf+yF0ZxB085bZn7rQZIp+df3uwh+0mjOd2ZsOKJPPWcYUfQd4da49klVjQpYaQegOz3iZEsQJZFhRV7wXIVxxwe5kKGybXkvaTjFEmiDiWjvUg+VbbQvsgMOiBmsfGwWSaFX/HWcwh9M9Lny7VE1qPXtLR/6yNDADlZ8xIiGnSMjPxVGqSUSlMvv1EvtF+5nF0lovn/R5dgbOZFeu2sLl4Dv3XS+IPwM8nTtR2tzov/7x6uNSM0PMoDotDj4318P938IF1vDyDf6ddZ+Bodiw0ho8fz48o98DBJM5Erc1ubLCZM8YPnIZsr",
                    "AKA_A2": "A",
                    "akacd_ohw_prd_external": "3904216979~rv=42~id=41ac048ee5d029e0bb940c24b41ff25e",
                    "bm_lso": "19C4FFC4FD4886CDF9952F09DAABD5CE958913E94329C63D91731A195A07F014~s9Goea5/TI7ICD6fGwrqzcTpb5HUVPfmpHX9/dbBA2ity5jahOJT6L/wTgSYsJVzI0B6yFFzdk9a/YEHgpOzwcnbmfRjSGMwzASNbQlJf4niUeLtQneAFak/kHoYvYttzq6m0iIjahTPShVy895ZklDOieOE1gWNv+jU6aumUUzG+rW+Djw7qDTnUVB6HO1zU+MrTj2gWmTu8FJr9SkAGSsXdfsazRYulPKnlospbWG4=^1726777754028",
                    "bm_sv": "3E79A7E5F5CDBBCF8A0C3E90E72D4383~YAAQFLQRYCAI7/+RAQAA6tf8Cxm/g+nNbxemd+qekqZe/Beu7PSDR92jcyEfP9oJRaq798TBOd6v+H4NGn7EjKmkOug1pbMN3X5H16n6otMbMUhTnmMHmozOn3hv7k5KJlPLc1CwC8/sVua/54r++yhTY6xHtrBqVXvT+YITNVoxrMLI28F6drtfondzvwZQxdInrcrZt1IkfVG6/4tQAUjb+jhplYxSpc5WmImU9lEJg/O5s4i0k37Y+PqPGRaX3g==~1",
                    "bm_sz": "60FF1909C0DC481ABD7BAD42C6313E6E~YAAQFLQRYPsH7/+RAQAAjNT8Cxn+y1cyGRhU+sjEO++bUJvVJxNV2QxNUecMl3Vb+3FuJRsM8gwJzI58BRcV1Fs7Tx+L5EsouVaTSl/zoKAD+0tVFscy/dHtSy3/QTynkiQkLDTXDHuoE/1/utM3LF2ZS5KUCyu7oDHLb6OTz13F92syQMyCN8u9RkK0IlOUtNsLKWRVrnnu1TJKKHSJrSUGw1aWXYncLNZIQQATDHLqE3oGTf4z+2ylZ27mfqWd+LfAWJEMG47qLXrIqzxpG/1R1fKkazcHZ03mc5u0Oxk8pswc5skkeITcEE8HNPHwPVkv4dQ32PJQjJ3uy3QOfN7JAvMg0+d+NGixXimgsLIePwjCJz2TXISJNm36+pYGvAncS+MiEVmZUDinQVes9Y/2nSCBqGo5Bwu3ejqsg9WZswRGJlFnZ5O/XDxdyfwCZepfuBvSYLceIzD9M1Zoq7gNVzekGWUUjh+XnZyV465XFQt0XQ==~4469049~3748917",
                    "dtCookie": "v_4_srv_9_sn_3D419697IDIC7LQDDLEOJL3QEK8ODH5K_app-3A0da30f11c94bda74_1_ol_0_perc_100000_mul_1_rcs-3Acss_0",
                    "dtPC": "9$577747505_703h48vKGICMHUPGNSFHWFVPWWVKKMKNFPHPRWR-0e0",
                    "dtSa": "false|xhr|48|fetch|fetch|1726777971096|577747505_703|https://www.hilton.com/en/hilton-honors/login/||||",
                    "forterToken": "aceef484222049a18f85370fb476551c_1726777747766__UDF43-m4_15ck",
                    "ftr_blst_1h": "1726776193628",
                    "loggedIn": "true",
                    "RT": '"z=1&dm=hilton.com&si=0d86a289-18eb-41d6-8c7c-106569068fe9&ss=m19pz13s&sl=4&se=p0&tt=pof&bcn=//684d0d44.akstat.io/&ld=x1ef&nu=2mdwefw3&cl=11n42&ul=11pct"',
                    "rxVisitor": "1726764180560464UE2I35FH2I067PQBEG7TSC5SN1RB5",
                    "rxvt": "1726779771918|1726775621815",
                    "sbsd": "s1DbKbEPOpzVGKjj8wRlk9AxicF+Q4QtjShif6nwBjRSGhqXc9+374mUbkgYT0xIAMiozUVS/A6rycZmn4DN3j9E8kNS3kbdNa9E20vOtlQgiU3Z0BQniJTAGuaHQtwebhm7QR4qWZojf25eY0AFXA2lMDLkfFmAWCmJESPJnS87wJ8uY+gVaZkxJ9w17sSMQ",
                    "sbsd_o": "19C4FFC4FD4886CDF9952F09DAABD5CE958913E94329C63D91731A195A07F014~s9Goea5/TI7ICD6fGwrqzcTpb5HUVPfmpHX9/dbBA2ity5jahOJT6L/wTgSYsJVzI0B6yFFzdk9a/YEHgpOzwcnbmfRjSGMwzASNbQlJf4niUeLtQneAFak/kHoYvYttzq6m0iIjahTPShVy895ZklDOieOE1gWNv+jU6aumUUzG+rW+Djw7qDTnUVB6HO1zU+MrTj2gWmTu8FJr9SkAGSsXdfsazRYulPKnlospbWG4=",
                    "sbsd_ss": "ab8e18ef4e",
                    "TMS": "undefined",
                    "visitorId": "3e8ced91-6edd-4a04-9b63-b6f5d9e70b5c",
                    "wso2AuthToken": '{"accessToken":"DX.eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkEyNTZHQ00iLCJwaWQiOiJ3ZWIiLCJraWQiOiI4UVl1RTZfdHBValdjUmVnem1RZFlBaF9RYlk1ckVqUlpPTThwWmNKeU5BIn0.X3mPWRnw7Gd21VRNwgCznqR1-Mcvde2VPlUsVvpRwrmaN4WbtQfhc3HrSGixGOTQ9a8YNRKGFDHsHlCfVQH8LgHPJlOAmMi4XJD25W1om7zCk4P9-7ThcnsUH3F8aoLpACxOH94eFJ0KFzI3rgD5zYQfStrhK5Tiz-0MX5wtHNqIhDZnzaBV0U2G5L6m9-TFcElkhlXwu40GkQubHRiOkmSWfldQDnV0Ngd3lJOxeCgHdCCGLhHQx1swEX-3UbHpGCsjJUcOepdxpL4M4xmED7LLvSLR2SqAVqh4lkFCDCVEq3HDN_jq6nWwvgi1mG4LMJQ5VwwH7e9mli9pW-G3ow.st2sAdHvVLTiVmfs.…Fl9AJuc8Sr-j_1FJpDG7tD09DXId7roBrfYl5Y2uDVJLOBBZizhdzePWjkoQK2a1ZnwOqsOp-PQhuYPI26aiy7mUdpHwwaJOoxcdIWEKthE4Z5NuTNOjdsYkHr67Ji9KJQGBwRs3zHNxM8-wSLYNjo5l-tmZlw8oPEagwIJnP8ZM9w1zctWo3fGO8uj0eezgMdw3A1tnU_WGqIogf4NhFJgWcKo5u17QH28qdMppBojuxS-cbo_OWEEUdhCHycdl-VlDd14UNCcz4CESyuO0C7nomKdvFfdO0_rbPBTEBcXoNso4Tmj1FQCD754SBEabY6nJ-tFEeEDC6fyk_C7ggllyV8WimAjOrkQOcR4jkkYDbV8Ght6dRea80xQ-aYRrw.StD5Scu4CnFULHuuzD8pPA","expiresIn":1506,"tokenType":"Bearer","timestamp":1726777971095,"username":null,"guestId":420121024}'
                }

                headers = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br, zstd',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Connection': 'keep-alive',
                    'Cookie': 'sbsd_o=19C4FFC4FD4886CDF9952F09DAABD5CE958913E94329C63D91731A195A07F014~s9Goea5/TI7ICD6fGwrqzcTpb5HUVPfmpHX9/dbBA2ity5jahOJT6L/wTgSYsJVzI0B6yFFzdk9a/YEHgpOzwcnbmfRjSGMwzASNbQlJf4niUeLtQneAFak/kHoYvYttzq6m0iIjahTPShVy895ZklDOieOE1gWNv+jU6aumUUzG+rW+Djw7qDTnUVB6HO1zU+MrTj2gWmTu8FJr9SkAGSsXdfsazRYulPKnlospbWG4=; sbsd=s1DbKbEPOpzVGKjj8wRlk9AxicF+Q4QtjShif6nwBjRSGhqXc9+374mUbkgYT0xIAMiozUVS/A6rycZmn4DN3j9E8kNS3kbdNa9E20vOtlQgiU3Z0BQniJTAGuaHQtwebhm7QR4qWZojf25eY0AFXA2lMDLkfFmAWCmJESPJnS87wJ8uY+gVaZkxJ9w17sSMQ; ...',
                    'Host': 'www.hilton.com',
                    'Priority': 'u=0, i',
                    'Referer': 'https://www.hilton.com/en/hilton-honors/login/',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-User': '?1',
                    'TE': 'trailers',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0'
                }



                proxies = [
                    {"http": "http://3.124.133.93:80", "https": "https://3.124.133.93:80"},
                    {"http": "http://8.215.12.103:8008", "https": "https://8.215.12.103:8008"},
                    {"http": "http://47.91.121.127:8081", "https": "https://47.91.121.127:8081"},
                    {"http": "http://165.154.224.14:80", "https": "https://165.154.224.14:80"},
                    {"http": "http://8.220.205.172:8008", "https": "https://8.220.205.172:8008"},
                    {"http": "http://149.129.226.9:80", "https": "https://149.129.226.9:80"},
                    {"http": "http://8.220.205.172:8081", "https": "https://8.220.205.172:8081"},
                    {"http": "http://47.91.29.151:8443", "https": "https://47.91.29.151:8443"},
                    {"http": "http://8.138.82.6:8081", "https": "https://8.138.82.6:8081"},
                    {"http": "http://8.221.141.88:9098", "https": "https://8.221.141.88:9098"},
                    {"http": "http://47.92.194.235:4000", "https": "https://47.92.194.235:4000"},
                    {"http": "http://8.220.204.92:9080", "https": "https://8.220.204.92:9080"},
                    {"http": "http://47.238.128.246:8081", "https": "https://47.238.128.246:8081"},
                    {"http": "http://54.233.119.172:3128", "https": "https://54.233.119.172:3128"},
                    {"http": "http://3.130.65.162:3128", "https": "https://3.130.65.162:3128"},
                    {"http": "http://8.213.197.208:80", "https": "https://8.213.197.208:80"},
                    {"http": "http://8.210.17.35:8443", "https": "https://8.210.17.35:8443"},
                    {"http": "http://18.228.198.164:3128", "https": "https://18.228.198.164:3128"},
                    {"http": "http://80.249.112.162:80", "https": "https://80.249.112.162:80"},
                    {"http": "http://8.212.151.166:3128", "https": "https://8.212.151.166:3128"},
                    {"http": "http://47.238.60.156:80", "https": "https://47.238.60.156:80"},
                    {"http": "http://8.220.205.172:3749", "https": "https://8.220.205.172:3749"},
                    {"http": "http://47.251.87.74:8443", "https": "https://47.251.87.74:8443"},
                    {"http": "http://154.205.152.96:8800", "https": "https://154.205.152.96:8800"},
                    {"http": "http://46.51.249.135:3128", "https": "https://46.51.249.135:3128"},
                    {"http": "http://47.237.2.245:3128", "https": "https://47.237.2.245:3128"}
                ]





                proxy = random.choice(proxies)
                response_post = session.post(login_url, json=form_data, cookies=cookies, headers=headers, proxies=proxy, timeout=10)
                st.write(response_post.content)
                # if "Usuario/Contraseña incorrecto." in response_post.text:
                #     st.error(f"Login failed for {user_identifier}.")
                # elif "Bienvenido:" in response_post.text:
                #     st.success(f"Login successful for {user_identifier}!")
                # else:
                #     st.error(f"Unexpected response for {user_identifier}.")

            except Exception as e:
                st.error(f"An error occurred for {user_identifier}: {e}")
    else:
        st.warning(f"Missing username/email or password for row .") 



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