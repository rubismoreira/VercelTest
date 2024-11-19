import requests
import pandas as pd
import json;
import streamlit as st
from datetime import datetime

api_key = 'DDF9C85CAFC41A4C7EA9A44A2FA42441D693'

header = 'X-Adzerk-ApiKey'

def fetch_data():
    response = requests.get('https://api.kevel.co/v1/fast/flight?isActive=true&nameContains=BF&afterStartDate=2024-11-01', headers={header: api_key})
    data = response.text.split('\n')
    df_data = [json.loads(line) for line in data if line.strip()] 
    df = pd.DataFrame(df_data)
    df['EndDate'] = pd.to_datetime(df['EndDate'])
    
    df['Details'] = df['Id'].apply(lambda x: f'https://app.kevel.co/#!/10192/flight/{x}/edit/')
    return df[['Name', 'CustomFieldsJson', 'StartDate', 'IsDeleted', 'Id', 'IsActive', 'CustomTargeting', 'DailyCapAmount', 'Keywords', 'EndDate', 'CampaignId', 'Details']]



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

def get_from_csv():
    df = pd.read_csv('test2.csv')
    df['EndDate'] = pd.to_datetime(df['EndDate'])
    return df

if st.button('Reload Data'):
    df = fetch_data()
    styled_df = df.style.apply(highlight_rows, axis=1)
    st.dataframe(styled_df)

    
