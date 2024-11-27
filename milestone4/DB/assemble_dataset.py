import numpy as np
import pandas as pd
import csv
from helper import get_stats, UnitedStatesIndicator, get_country_state

from constants import main_path

def assemble_dataset():
    df_cover = pd.read_csv(f'{main_path}/COVERPAGE.tsv', sep='\t')
    df_info = pd.read_csv(f'{main_path}/INFOTABLE.tsv', sep='\t')
    df_summary = pd.read_csv(f'{main_path}/SUMMARYPAGE.tsv', sep='\t')
    
    df_info = df_info[df_info['SSHPRNAMTTYPE'] == 'SH']
    df_info = df_info[df_info['ACCESSION_NUMBER'] != '0001104659-24-089646']
    df_info = df_info[df_info['ACCESSION_NUMBER'] != '0000894189-24-004736']
    df_info['SSHPRNAMT'] = df_info['SSHPRNAMT'].astype(float)
    
    df_investor = df_cover.merge(df_summary, how='inner', on='ACCESSION_NUMBER')
    
    df_investor['US_Indicator'] = df_investor['FILINGMANAGER_STATEORCOUNTRY'].apply(UnitedStatesIndicator)
    
    df_investor['State_Country_Full'] = df_investor['FILINGMANAGER_STATEORCOUNTRY'].apply(get_country_state)
    # df_us = df_investor[df_investor['US_Indicator'] == True]
    df_us = df_investor
        
    # New dataframe for summary stats
    df_stats = get_stats(df_info)
    
    df_state_gdp = pd.read_csv("../../data/state-gdp.csv")
    df_us2 = df_us
    df_us2 = df_us2.merge(right=df_stats, how='left',on='ACCESSION_NUMBER')
    df_us2['FILINGMANAGER_CITY'] = df_us2['FILINGMANAGER_CITY'].str.lower()
    
    from constants import features
    
    feature_list = features + ['OTHERINCLUDEDMANAGERSCOUNT', 'US_Indicator']
    df_star = df_us2[feature_list]  
    return df_star

if __name__ == "__main__":
    assemble_dataset().to_csv(f'{main_path}/encoded_data.csv', index=False)