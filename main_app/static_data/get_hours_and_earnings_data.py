import requests
import os
import time
import pandas as pd
import re

base_url = 'https://www.nomisweb.co.uk/api/v01/dataset/NM_99_1.data.csv?geography=1811939329...1811939332,1811939334...1811939336,1811939338...1811939428,1811939436...1811939442,1811939768,1811939769,1811939443...1811939497,1811939499...1811939501,1811939503,1811939505...1811939507,1811939509...1811939517,1811939519,1811939520,1811939524...1811939570,1811939575...1811939599,1811939601...1811939628,1811939630...1811939634,1811939636...1811939647,1811939649,1811939655...1811939664,1811939667...1811939680,1811939682,1811939683,1811939685,1811939687...1811939704,1811939707,1811939708,1811939710,1811939712...1811939717,1811939719,1811939720,1811939722...1811939730&date=latestMINUS9-latest&sex=7&item=1...3,6...15&pay=1,5,7...9&measures=20100,20701&select=date_name,geography_name,geography_code,sex_name,pay_name,item_name,measures_name,obs_value,obs_status_name&RecordOffset='
script_directory = os.path.dirname(os.path.abspath(__file__))
filename_prefix = 'h_and_e'
subdirectory = 'h_and_e'
save_directory = os.path.join(script_directory, subdirectory)

counter = 0
for i in range(0,471900,25000):
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

output_filepath = os.path.join(script_directory, 'h-and-e-districts-joined.csv')
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