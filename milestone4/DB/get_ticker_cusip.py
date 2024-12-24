import requests
import time
def get_ticker_from_cusip(cusip):
    api_key = '3f713da7-a551-4614-bd1f-1b0313a0b89e'
    url = "https://api.openfigi.com/v3/mapping"
    headers = {
        "Content-Type": "application/json",
        "X-OPENFIGI-APIKEY": api_key
    }
    payload = [{
        "idType": "ID_CUSIP",
        "idValue": cusip
    }]
    
    
    def wait_for_rate_limit():
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 429:
            print("Rate limit exceeded. Waiting for 6 seconds...")
            time.sleep(6)
            wait_for_rate_limit()
        return response
    
    response = wait_for_rate_limit()
    
    if response.status_code == 200:
        data = response.json()
        if data and 'data' in data[0] and data[0]['data']:
            return data[0]['data'][0]['ticker']
        else:
            return "TICKER not found for the provided CUSIP."
    else:
        return f"Error: {response.status_code}, {response.text}"

# Replace with your own API key
# api_key = '3f713da7-a551-4614-bd1f-1b0313a0b89e'

import pandas as pd
df = pd.read_csv("../../data/2024_Q2/INFOTABLE.tsv", sep='\t')

df['CUSIP'] = df['CUSIP'].astype(str)
df_cusip =  pd.Series(df['CUSIP'].unique(), name= 'CUSIP').to_frame()

from tqdm import tqdm
tqdm.pandas()
df_cusip['TICKER'] = df_cusip['CUSIP'].progress_apply(get_ticker_from_cusip)

df_cusip.to_csv("../../data/2024_Q2/CUSIP_TICKER.csv", index=False)