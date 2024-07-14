
import pandas as pd
import numpy as np
import utils.utils as uti
import re
import os

dict_unique_conducts = {"1.1":1, "1.3":1, 
        "1.15":2, "1.15a":2, "1.15 (a)":2, "1.15A":2, "1.15 (A)":2,"1.15b":2,"1.15 (b)":2, "1.15B":2, "1.15 (B)":2,
        "1.4":3,
        "1.7":4, "1.8":4, "1.10":4, "1.11":4, "1.16":4, "1.17":4,
        "1.2":5, "1.5":5, "1.6":5, '1.9':5, "1.12":5, '1.13':5, '1.14':5,
        "2.1":6, "2.2":6, "2.3":6, "2.4":6, "3.1":6, "3.2":6, "3.3":6, "3.4":6, "3.5":6, "3.6":6, "3.7":6, "3.8":6, "3.9":6,
        "4.1":7, "4.2":7, "4.2.":7, "4.3":7, "4.4":7, "5.1":7, "5.2":7, "5.3":7, "5.4":7, "5.5":7, "5.6":7, "5.7":7,"5.8":7,
         "6.1":7, "6.2":7, "6.3":7, "6.4":7, "6.5":7, "7.1":7, "7.2":7, "7.3":7, "7.4":7, "7.5":7,"7.6":7,
        "8.4b":8, '8.4 (b)':8,
        "8.4c":9, '8.4 (c)':9,
        '8.1':10, '8.2':10, '8.4':10, '8.4a':10, '8.4 (a)':10, '8.4d':10, '8.4 (d)':10, '8.4e':10, '8.4 (e)':10, '8.4h':10, 
        '8.4 (h)':10, '8.4i':10, '8.4 (i)':10, '8.4j':10, '8.4 (j)':10, '8.4k':10, '8.4 (k)':10, '8.4l':10, '8.4 (l)':10, '8.4m':10, '8.4 (m)':10,
         '8.4n':10, '8.4 (n)':10, '8.5':10}
         

labels_ABA = list(dict_unique_conducts.keys())

def find_matches(description):
    matches = [item for item in labels_ABA if item in description]
    return matches if matches else None


def preprocess_NC(state = "NC"):

    file_path = f'../../data/raw/{state}/'
    # List all the txt files in the directory
    txt_files = [f for f in os.listdir(file_path) if f.endswith('.txt')]

    # Initialize an empty list to store the content of each txt file
    descriptions = []

    # Read each file and store its contents into the list
    for file in txt_files:
        with open(os.path.join(file_path, file), 'r', encoding='utf-8') as file_open:
            content = file_open.read().replace('\n', ' ')  # Replace newlines with space
            descriptions.append(content)

    # Create a DataFrame with a single column 'Descriptions' from the list of contents
    df = pd.DataFrame(descriptions, columns=['Description'])

    df['labels'] = df['Description'].apply(find_matches)
    df_filtered = df.dropna(subset=['labels'])
    percentage_kept = (len(df_filtered) / len(df)) * 100

    df_filtered = df_filtered[df_filtered['labels'].map(len) <= 16] 
    
    print(f"Percentage of rows kept: {percentage_kept:.2f}%", len(df_filtered))
    labels_nc = pd.DataFrame(df_filtered['labels'].to_list())
    df_filtered = pd.concat([df_filtered.drop(columns='labels').reset_index(drop=True), labels_nc.reset_index(drop=True)], axis=1)
    return df_filtered




