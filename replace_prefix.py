
prefix_dict = {'cco':'cco.com'}

x = 'cco'
y = 'cco.com'

m_filepath = 'smapping.csv'

with open(m_filepath,'r')as m_file:
    m_file_reader = m_file.read()

for key, value in prefix_dict.items():
    m_file_reader = m_file_reader.replace(key,value)
print(m_file_reader)

import csv

mapping_file='smapping.csv'



with open(mapping_file, 'r') as input_file:                
    mapping_reader = csv.DictReader(input_file)
    
    for dict_row in mapping_reader:
        for k, v in dict_row.items():

            for k, v in prefix_dict.items():
                dict_row = dict(((key, value.replace(k,v)) for key, value in dict_row.items()))
    print(input_file)


#with open(mapping_file, 'r') as input_file:                
    mapping_reader = csv.DictReader(input_file)
    
    for dict_row in mapping_reader:
        for k, v in dict_row.items():

            for k, v in prefix_dict.items():
                dict_row = dict(((key, value.replace(k,v)) for key, value in dict_row.items()))
    print(mapping_file)

