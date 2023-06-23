from .static_data.lookups import inverse_names, indexed_variables
import re

# Used to internally reorder fields for the industry variables
def reorder_numbers(indices):
    order = [13, 11, 12, 10, 9, 0, 8, 3, 4, 7, 2, 5, 6, 1]
    
    chunk_count = len(indices) // 14
    
    reordered_numbers = []
    for i in range(chunk_count):
        start = i * 14
        end = start + 14
        chunk = indices[start:end]
        reordered_chunk = [chunk[i] for i in order]
        reordered_numbers.extend(reordered_chunk)
    
    return reordered_numbers

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

def check_order(keys):
    for i in range(len(keys)):
        print(f"{i} -> {keys[i]}")

def check_names(dict):
    for i in range(len(industry_dict)):
        print(f"{i} -> {industry_dict[i]}")                     

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

for index, key in enumerate(industry_keys):
    industry_dict[index] = key

for index, key in enumerate(demographics_keys):
    demographics_dict[index] = key

for index, key in enumerate(socioeconomics_keys):
    socioeconomics_dict[index] = key

demographics_order = remove_duplicates([7,1,*range(0,7+1),*range(23,30+1),19,20,*range(13,20+1),22,21,31,*range(8,12+1),*range(32,36+1)])
demographics_final_order_dict = {k: demographics_keys[k] for k in demographics_order}
demographics_final_order_list = [*demographics_final_order_dict.values()]

industry_order = remove_duplicates([*range(530,539+1),*range(0,263+1),*reorder_numbers(range(264,529+1)),*reorder_numbers(range(540,567+1))])
industry_final_order_dict = {k: industry_keys[k] for k in industry_order}
industry_final_order_list = [*industry_final_order_dict.values()]

socioeconomics_order = remove_duplicates([183,127,*range(80,84+1),*range(58,65+1),67,40,182,66,*range(7,32+1),*range(192,204+1),*range(92,104+1),*range(68,72+1),*range(177,181+1), *range(205,208+1), *range(105,117+1), *range(184,191+1), *range(118,126+1),*range(51,57+1),*range(85,91+1),*range(0,6+1),*range(73,79+1),*range(41,50+1),*range(142,162+1),*range(163,176+1),*range(33,39+1),*range(128,141+1)])
socioeconomics_final_order_dict = {k: socioeconomics_keys[k] for k in socioeconomics_order}
socioeconomics_final_order_list = [*socioeconomics_final_order_dict.values()]