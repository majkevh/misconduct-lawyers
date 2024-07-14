import pandas as pd
import numpy as np
import utils.utils as uti
import re

def remove_extra_rows_NJ(state = "NJ"):
    file_path = f'../../data/csv_files/{state}_disciplinary_actions.csv'
    df = pd.read_csv(file_path)

    # Keep only: 'misconduct' column
    cols_to_keep = ['misconduct'] 
    df = df[cols_to_keep]

    # Remove rows with no labels (RPC) and no 'misconduct'
    df_filtered = df[df['misconduct'].str.contains("RPC")]
    df_filtered = df_filtered.dropna(subset=['misconduct'])
    percentage_kept = (len(df_filtered) / len(df)) * 100
    print(f"Percentage of samples kept: {percentage_kept:.2f}%")

    labels_nj = df_filtered['misconduct'].apply(extract_labels_rpc_NJ)
    labels_nj = pd.DataFrame(labels_nj.to_list())
    df_filtered = pd.concat([df_filtered.reset_index(drop=True), labels_nj.reset_index(drop=True)], axis=1)
    df_filtered = df_filtered.rename(columns={"misconduct": "Description"})
    return df_filtered

def extract_labels_rpc_NJ(text):
    # This regex looks for 'RPC ' followed by any 4 characters (and remove non-numbers)
    matches = re.findall(r'RPC (\d+\.\d{1,2})', text)
    return matches

