from .static_data.lookups import inverse_names, indexed_variables
import re

def remove_duplicates(list):    
    new = []
    for num in list:
        if num not in new:
            new.append(num)
    return new

def test_correctness(list):
    print(f"List length -> {len(list)}")
    for i in range(len(list)):
        if i not in list:
            print(f'error -> {i} is missing')
        else:
            print(f'{i} -> {list[i]}') 

industry_indices = []
demographics_indices = []
socioeconomics_indices = []

industry_keys = []
demographics_keys = []
socioeconomics_keys = []

industry_dict = {}
demographics_dict = {}
socioeconomics_dict = {}

industry_patterns = [
    r'^\d{2}_.*',
    r'^sic_.*',
    r'^[a-zA-Z]_.*'
]

demographics_patterns = [
    r'^aged_.*',
    r'^all_age.*',
    r'^ethnic_.*',
    r'^fert_.*',
    r'^gfr',
    r'^live_.*',
    r'^over_.*',
    r'^tfr',
    r'^white_.*'
]

socioeconomics_patterns = [
    r'^alevel_.*',
    r'^annual_.*',
    r'^apprentice_.*',
    r'^are_.*',
    r'^at_.*',
    r'^degree_.*',
    r'^econ_.*',
    r'^emp.*',
    r'^full_.*',
    r'^gcse_.*',
    r'^gdhi_.*',
    r'^he_.*',
    r'^hour.*',
    r'^inact_.*',
    r'^job.*',
    r'^no_.*',
    r'^nvq.*',
    r'^other_.*',
    r'^part_.*',
    r'^self_.*',
    r'^total_.*',
    r'^unemp.*',
    r'^weekly_.*',
    r'^work_.*'
]

industry_compiled = [re.compile(pattern) for pattern in industry_patterns]
demographics_compiled = [re.compile(pattern) for pattern in demographics_patterns]
socioeconomics_compiled = [re.compile(pattern) for pattern in socioeconomics_patterns]

for key, value in indexed_variables.items():
    for pattern in industry_compiled:
        if pattern.match(key):
            industry_indices.append(value)
            industry_keys.append(key)
            break
    for pattern in demographics_compiled:
        if pattern.match(key):
            demographics_indices.append(value)
            demographics_keys.append(key)
            break
    for pattern in socioeconomics_compiled:
        if pattern.match(key):
            socioeconomics_indices.append(value)
            socioeconomics_keys.append(key)
            break

# for i in range(len(industry_keys)):
#     industry_dict[i] = industry_keys[i]

# for i in range(len(demographics_keys)):
#     demographics_dict[i] = demographics_keys[i]

# for i in range(len(socioeconomics_keys)):
#     socioeconomics_dict[i] = socioeconomics_keys[i]

demographics_order = remove_duplicates([7,1,*range(0,7+1),*range(23,30+1),9,19,20,*range(13,20+1),22,21,31,*range(8,12+1),*range(32,36+1)])
demographics_final_order_dict = {k: demographics_keys[k] for k in demographics_order}
demographics_final_order_list = [*demographics_final_order_dict.values()]
