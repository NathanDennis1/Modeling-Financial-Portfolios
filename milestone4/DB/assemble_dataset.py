import numpy as np
import pandas as pd
import csv

from constants import main_path

def assemble_dataset():
    df_cover = pd.read_csv(f'{main_path}/2024_Q2/COVERPAGE.tsv', sep='\t')
    df_info = pd.read_csv(f'{main_path}/INFOTABLE.tsv', sep='\t')
    df_summary = pd.read_csv(f'{main_path}/SUMMARYPAGE.tsv', sep='\t')
    
    df_info = df_info[df_info['SSHPRNAMTTYPE'] == 'SH']
    df_info = df_info[df_info['ACCESSION_NUMBER'] != '0001104659-24-089646']
    df_info = df_info[df_info['ACCESSION_NUMBER'] != '0000894189-24-004736']
    df_info['SSHPRNAMT'] = df_info['SSHPRNAMT'].astype(float)
    
    df_investor = df_cover.merge(df_summary, how='inner', on='ACCESSION_NUMBER')
    state_df = pd.read_csv("../../data/state_list.csv")
    state_set = set(list(state_df['Abbreviation']))
    def UnitedStatesIndicator(x):
        return (x in state_set) # check if the location is in the US based on the state abbreviation
    df_investor['US_Indicator'] = df_investor['FILINGMANAGER_STATEORCOUNTRY'].apply(UnitedStatesIndicator)
    
    # Initialize an empty dictionary
    state_dict = {}
    # Open the CSV file
    with open('../../data/state_country_abbreviations.csv', mode='r') as file:
        reader = csv.reader(file,skipinitialspace = True)
        # Iterate through the rows in the file
        for row in reader:
            # Assign the first column as the key and the second column as the value
            state_dict[row[0]] = row[1]
            
    def get_country_state(x):
        try: return state_dict[x]
        except KeyError: return np.nan
        
    df_investor['State_Country_Full'] = df_investor['FILINGMANAGER_STATEORCOUNTRY'].apply(get_country_state)
    # df_us = df_investor[df_investor['US_Indicator'] == True]
    df_us = df_investor
        
    
    # New dataframe for summary stats
    s = df_info.groupby(by="ACCESSION_NUMBER")['VALUE'].mean()
    s = s.rename("MEAN VALUE")
    df_stats = s.to_frame()
    df_stats['MIN VALUE'] = df_info.groupby(by='ACCESSION_NUMBER')['VALUE'].min()
    df_stats['MAX VALUE'] = df_info.groupby(by='ACCESSION_NUMBER')['VALUE'].max()
    df_stats['STD VALUE'] = df_info.groupby(by='ACCESSION_NUMBER')['VALUE'].std()
    df_stats['25% VALUE'] = df_info.groupby(by='ACCESSION_NUMBER')['VALUE'].quantile(q = 0.25)
    df_stats['50% VALUE'] = df_info.groupby(by='ACCESSION_NUMBER')['VALUE'].quantile(q = 0.50)
    df_stats['75% VALUE'] = df_info.groupby(by='ACCESSION_NUMBER')['VALUE'].quantile(q = 0.75)
    df_stats['10% VALUE'] = df_info.groupby(by='ACCESSION_NUMBER')['VALUE'].quantile(q = 0.10)
    df_stats['90% VALUE'] = df_info.groupby(by='ACCESSION_NUMBER')['VALUE'].quantile(q = 0.90)
    df_stats['99% VALUE'] = df_info.groupby(by='ACCESSION_NUMBER')['VALUE'].quantile(q = 0.99)
    df_stats['01% VALUE'] = df_info.groupby(by='ACCESSION_NUMBER')['VALUE'].quantile(q = 0.01)
    
    df_stats['MEAN SHAMT'] = df_info.groupby(by='ACCESSION_NUMBER')['SSHPRNAMT'].mean()
    df_stats['MIN SHAMT'] = df_info.groupby(by='ACCESSION_NUMBER')['SSHPRNAMT'].min()
    df_stats['MAX SHAMT'] = df_info.groupby(by='ACCESSION_NUMBER')['SSHPRNAMT'].max()
    df_stats['STD SHAMT'] = df_info.groupby(by='ACCESSION_NUMBER')['SSHPRNAMT'].std()
    df_stats['25% SHAMT'] = df_info.groupby(by='ACCESSION_NUMBER')['SSHPRNAMT'].quantile(q = 0.25)
    df_stats['50% SHAMT'] = df_info.groupby(by='ACCESSION_NUMBER')['SSHPRNAMT'].quantile(q = 0.50)
    df_stats['75% SHAMT'] = df_info.groupby(by='ACCESSION_NUMBER')['SSHPRNAMT'].quantile(q = 0.75)
    df_stats['10% SHAMT'] = df_info.groupby(by='ACCESSION_NUMBER')['SSHPRNAMT'].quantile(q = 0.10)
    df_stats['90% SHAMT'] = df_info.groupby(by='ACCESSION_NUMBER')['SSHPRNAMT'].quantile(q = 0.90)
    df_stats['99% SHAMT'] = df_info.groupby(by='ACCESSION_NUMBER')['SSHPRNAMT'].quantile(q = 0.99)
    df_stats['01% SHAMT'] = df_info.groupby(by='ACCESSION_NUMBER')['SSHPRNAMT'].quantile(q = 0.01)
    df_stats = df_stats.reset_index()
    
    df_state_gdp = pd.read_csv("../../data/state-gdp.csv")
    df_us2 = df_us
    # df_us2 = df_us.merge(
    #     right=df_state_gdp, 
    #     how='left', 
    #     left_on = 'FILINGMANAGER_STATEORCOUNTRY', 
    #     right_on='Abbreviation')
    df_us2 = df_us2.merge(right=df_stats, how='left',on='ACCESSION_NUMBER')
    df_us2['FILINGMANAGER_CITY'] = df_us2['FILINGMANAGER_CITY'].str.lower()
    
    
    features = [
        'TABLEENTRYTOTAL',
        'TABLEVALUETOTAL',
        'MIN VALUE',
        'MAX VALUE',
        'MEAN VALUE',
        'STD VALUE',
        '25% VALUE',
        '50% VALUE',
        '75% VALUE',
        '01% VALUE',
        '99% VALUE',
        '10% VALUE',
        '90% VALUE',
        'MIN SHAMT',
        'MAX SHAMT',
        'MEAN SHAMT',
        'STD SHAMT',
        '25% SHAMT',
        '50% SHAMT',
        '75% SHAMT',
        '01% SHAMT',
        '99% SHAMT',
        '10% SHAMT',
        '90% SHAMT',
    ]
    
    # for i, log_feature in enumerate(log_features):
    #     # Replace 0 with 1 or 0.0001 to avoid log(0) error
    #     # df_us2[features[i]] = df_us2[features[i]].replace(0, 0.0001)
    #     df_us2[log_feature] = df_us2[features[i]].apply(get_log_feature)  
    
    feature_list = features + ['OTHERINCLUDEDMANAGERSCOUNT', 'US_Indicator']
    df_star = df_us2[feature_list]  
    # df_starlog = df_us2[log_features]
    print(len(df_star))
    return df_star

if __name__ == "__main__":
    assemble_dataset().to_csv(f'{main_path}/encoded_data.csv', index=False)