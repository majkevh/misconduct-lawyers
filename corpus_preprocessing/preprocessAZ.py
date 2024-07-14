
import pandas as pd
import numpy as np
import utils.utils as uti
import re
import os
import pandas as pd
from bs4 import BeautifulSoup
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

def find_matches(description, label_list):
    """
    Searches for occurrences of items from 'label_list' in 'description'.
    
    Args:
    description (str): The text in which to search for labels.
    label_list (list): A list of labels to search for in the description.

    Returns:
    list or None: Returns a list of matches or None if no matches found.
    """
    matches = [item for item in label_list if item in description]
    return matches if matches else None

def preprocess_AZ():
    # Directory path containing the HTML files
    directory_path = '../../data/raw/AZ/'

    hand_path = directory_path + "AZ_disciplinary_hand.csv"
    # Initialize an empty DataFrame to store all data
    all_data = pd.DataFrame()

    # List all HTML files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".html"):
            file_path = os.path.join(directory_path, filename)
            
            try:
                # Read the HTML content from the file
                with open(file_path, 'r', encoding='utf-8') as file:
                    html_content = file.read()

                # Use BeautifulSoup to parse the HTML
                soup = BeautifulSoup(html_content, 'html.parser')

                # Find the table
                table = soup.find('table')
                descriptions = []
                potential_labels = []

                # Find the column index for 'Violations Description Disciplinary Rules' (case-insensitive)
                header_row = table.find('tr')
                headers = ["".join(th.stripped_strings).lower() for th in header_row.find_all('td')]  # Convert headers to lowercase
                search_header = 'violations descriptiondisciplinary rules'  # Also in lowercase
                try:
                    column_index = 1#headers.index(search_header)
                except ValueError:
                    raise ValueError("Specified column header not found in the table for file: " + filename)

                # Iterate over all rows and extract the data from the specified column
                for row in table.find_all('tr')[1:]:  # skip the header row
                    cells = row.find_all('td')
                    if len(cells) > column_index:
                        text = cells[column_index].get_text(strip=True)
                        # Split text on "ER" and handle accordingly
                        parts = text.split('ER', 1)
                        descriptions.append(parts[0].strip())
                        potential_labels.append('ER' + parts[1].strip() if len(parts) > 1 else '')

                # Create a DataFrame for the current file
                df = pd.DataFrame({
                    'Descriptions': descriptions,
                    'temp_labels': potential_labels
                })
                df['labels'] = df['temp_labels'].apply(lambda x: find_matches(x, labels_ABA))
                df = df.drop('temp_labels', axis=1)

                # Append to the main DataFrame
                all_data = pd.concat([all_data, df], ignore_index=True)

            except FileNotFoundError:
                print(f"The file {file_path} does not exist.")
            except Exception as e:
                print(f"An error occurred while processing {file_path}: {str(e)}")

    df_hand = pd.read_csv(hand_path)
    df_hand["Descriptions"] = df_hand["Descriptions"].str.replace('\n', ' ', regex=False)
    df_hand['labels'] = df_hand['Descriptions'].apply(lambda x: find_matches(x, labels_ABA))
    df_hand["Descriptions"] = df_hand["Descriptions"].str.split("ER").str[0] 
    df_tot = pd.concat([all_data, df_hand], ignore_index=True)

    df_filtered = df_tot.dropna(subset=['labels'])
    percentage_kept = (len(df_filtered) / (len(all_data) + len(df_hand))) * 100
    print(f"Percentage of rows kept: {percentage_kept:.2f}%")
    labels_az = pd.DataFrame(df_filtered['labels'].to_list())
    df_filtered = pd.concat([df_filtered.drop(columns='labels').reset_index(drop=True), labels_az.reset_index(drop=True)], axis=1)
    df_filtered = df_filtered.rename(columns={"Descriptions": "Description"})

    return df_filtered
