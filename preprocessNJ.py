import pandas as pd
import numpy as np
import utils as uti
import re

def remove_extra_rows_NJ(state = "NJ"):
    file_path = f'./data/{state}_disciplinary_actions.csv'
    df = pd.read_csv(file_path)

    # Keep only: 'misconduct' column
    cols_to_keep = ['misconduct'] 
    df = df[cols_to_keep]

    # Remove rows with no labels (RPC) and no 'misconduct'
    df_filtered = df[df['misconduct'].str.contains("RPC")]
    df_filtered = df_filtered.dropna(subset=['misconduct'])
    percentage_kept = (len(df_filtered) / len(df)) * 100
    print(f"Percentage of samples kept: {percentage_kept:.2f}%")
    return df_filtered

def extract_labels_rpc_NJ(text):
    # This regex looks for 'RPC ' followed by any 4 characters (and remove non-numbers)
    matches = re.findall(r'RPC (.{4})', text)    
    cleaned_matches = [''.join(re.findall(r'[\d\.]', match)) for match in matches]

    return cleaned_matches

