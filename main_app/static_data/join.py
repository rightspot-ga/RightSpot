import os
import pandas as pd
import re

script_directory = os.path.dirname(os.path.abspath(__file__))
subdirectory = 'data'
save_directory = os.path.join(script_directory, subdirectory)
output_filepath = os.path.join(script_directory, 'ons-data-districts-joined.csv')
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