import requests
import os
import time
import pandas as pd
import re

def get_data(base_url, subdirectory_name, filename_prefix, output_filename, request_num):
    directory = os.path.dirname(os.path.abspath(__file__))
    save_directory = os.path.join(directory, subdirectory_name)
    os.makedirs(save_directory, exist_ok=True)
    counter = 0
    for i in range(0,request_num,25000):
        print(f"Sending API request with RecordOffset={i}")
        url = f"{base_url}{i}"
        response = requests.get(url)
        if response.status_code == 200:
            filename = f"{filename_prefix}{counter}.csv"
            counter += 1
            file_path = os.path.join(save_directory, filename)
            with open(file_path, 'wb') as file:
                file.write(response.content)
                print(f'Saved {filename} successfully.')
        else:
            print(f'Error occurred while making the API call: {response.status_code}')
        time.sleep(0.5)    

    output_filepath = os.path.join(directory, output_filename)
    joined_data = pd.DataFrame()

    file_names = [filename for filename in os.listdir(save_directory) if filename.endswith('.csv')]
    file_names.sort(key=lambda x: int(re.findall(r'\d+', x)[0]))

    for filename in file_names:
        file_path = os.path.join(save_directory, filename)
        df = pd.read_csv(file_path)
        if joined_data.empty:
            joined_data = df
        else:
            joined_data = pd.concat([joined_data, df.iloc[1:]], ignore_index=True)

    joined_data = joined_data.reset_index(drop=True)
    joined_data.to_csv(output_filepath, index=False)
    print(f"Exported to '{output_filepath}' successfully.")