import pprint

names = []

new_names = {}

for name in names:
    new_names[name] = ''

pprint_string = pprint.pformat(new_names)
print(pprint_string)