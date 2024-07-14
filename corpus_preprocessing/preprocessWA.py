import pandas as pd
import numpy as np
import utils.utils as uti
import re

def remove_extra_rows_WA(state = "WA"):
    file_path = f'../../data/csv_files/{state}_disciplinary_actions.csv'
    df = pd.read_csv(file_path)

    # Keep only: 'Description' and those starting with 'conduct'
    conduct_cols = [col for col in df.columns if col.startswith('rule')]
    cols_to_keep = ['Description'] + conduct_cols
    df = df[cols_to_keep]

    # Remove rows with no labels (conducts) and no description
    df_filtered = df.dropna(how='all', subset=conduct_cols)
    df_filtered = df_filtered.dropna(subset=['Description'])
    percentage_kept = (len(df_filtered) / len(df)) * 100
    print(f"Percentage of samples kept: {percentage_kept:.2f}%")
    df_filtered
    return df_filtered, conduct_cols 