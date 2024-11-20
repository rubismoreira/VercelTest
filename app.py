import requests
import pandas as pd
import json;
import streamlit as st
import os
from datetime import datetime

api_key = 'DDF9C85CAFC41A4C7EA9A44A2FA42441D693'

header = 'X-Adzerk-ApiKey'
file_path = 'response.json'

st.markdown(
    """
    <style>
    .main .block-container {
        width: 80%;
        height: 80%;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def fetch_data():
    response = requests.get('https://api.kevel.co/v1/fast/flight?isActive=true&nameContains=BF&afterStartDate=2024-11-01', headers={header: api_key})
    data = response.text.split('\n')
    df_data = [json.loads(line) for line in data if line.strip()] 
    result = {
        'updated_on': datetime.now().isoformat(),
        'data': df_data
    }
        
    with open('response.json', 'w') as f:
        json.dump(result, f, indent=4)
        
def treat_data():
    with open('response.json', 'r') as f:
        data = json.load(f)
        df = pd.DataFrame(data.get('data'))
        df['EndDate'] = pd.to_datetime(df['EndDate'])
        df['Id'] = df['Id'].astype(str)
        df['CampaignId'] = df['Id'].astype(str)
        df['Details'] = df['Id'].apply(lambda x: f'https://app.kevel.co/#!/10192/flight/{x}/edit/')
        st.write(f"data last updated on {data.get('updated_on')}")
        return df[['Name', 'Keywords', 'StartDate', 'EndDate',  'Id', 'CampaignId', 'IsActive', 'CustomTargeting', 'DailyCapAmount','IsDeleted','CustomFieldsJson', 'Details']]


def highlight_rows(row):
    styles = [''] * len(row)
    if row['IsActive'] == False:
       styles[row.index.get_loc('IsActive')] = 'background-color: red' 
    if row['DailyCapAmount'] is not None:
        styles[row.index.get_loc('DailyCapAmount')] = 'background-color: red'
    if row['EndDate'] < pd.Timestamp.now(tz='UTC'):
        styles[row.index.get_loc('EndDate')] = 'background-color: red'
    if '$user.key !~ ".+\\=$"' not in row['CustomTargeting']:
        styles[row.index.get_loc('CustomTargeting')] = 'background-color: red' 
    
    return styles

def display_grid():
    df = treat_data()
    styled_df = df.style.apply(highlight_rows, axis=1)
   
    
    st.dataframe(styled_df)

    

if st.button('Reload Data'):
    df = fetch_data()
    
with open(file_path, 'r') as f:
    content = f.read()
    if not content:
        st.write("File is empty")
        fetch_data()

display_grid()

            
    