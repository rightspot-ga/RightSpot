import pprint

original_dict = {}

updated_dict = {}

for key, value in original_dict.items():
    new_value = key.replace(':','').replace(',', '').replace(')', '').replace('(', '').replace('+', 'plus').replace('-', '').replace(' ', '_').lower()
    new_value = '_'.join(word for word in new_value.split('_') if word)
    updated_dict[key] = new_value

pprint_string = pprint.pformat(updated_dict)
print(pprint_string)    