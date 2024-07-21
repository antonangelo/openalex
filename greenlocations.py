'''
Using pyalex to get aan institution's OA locations

anton@angelo.nz
'''

import pprint
from pyalex import Works, Authors, Sources, Institutions, Concepts, Publishers, Funders
import pyalex
from itertools import chain
from collections import Counter
import time
import os

def pretty_to_file(toprint, filename):
    with open(filename, "w", encoding="utf8") as output:
        pprint.pprint(toprint, output)
        
timestr = time.strftime("%Y%m%d-%H%M")
yearstr = time.strftime("%Y")

results_directory = timestr+"/"
if not os.path.exists(results_directory):
    os.makedirs(results_directory)

pyalex.config.email = "anton.angelo@canterbury.ac.nz" # set this to your own email.  It puts you in the openalex polite queue
publication_years =  range(2000,2024)

country_code = "nz" # set this (ISO country code)
results_filename =  country_code + timestr +"_greenworks_results.csv"
results_directory = "results/"

# get a list of institutions for the specific country, their RORs and overall publishing
#use the pyalex https://github.com/J535D165/pyalex library 
institutions = Institutions() \
    .filter(country_code=country_code) \
    .get()

pretty_to_file(institutions, results_directory + timestr+ country_code+"_institutions_full.py")

# list of unique ROR codes 

rors_dict ={}
for institution in institutions:
    rors_dict[institution["display_name"]] =institution["ror"]

pretty_to_file(rors_dict,  results_directory + country_code+"_institutions_short.py")

#https://api.openalex.org/works?filter=authorships.institutions.lineage:I185492890,type:article,open_access.is_oa:true,best_oa_location.source.type:repository&per_page=10

results = open( results_directory + results_filename, "w", encoding='utf8')
results.write("institution, ror, repository, count \n")

for institution_name in rors_dict.keys():
    ror_url = rors_dict[institution_name]
    print(institution_name)    
    greenworks = Works() \
        .filter(authorships={"institutions": {"ror": ror_url}}) \
        .filter(best_oa_location ={"source":{"type":"repository"}}) \
        .paginate(per_page=200) 

    big_repository_list = []    
    for item in chain(*greenworks):
        big_repository_list.append(item["best_oa_location"]["source"]["display_name"])

    big_repository_list_frequency = Counter(big_repository_list)


    for item in big_repository_list_frequency.items():
        resultline = '"'+ institution_name + '"'+ ','+ ror_url + ','+ '"'+  item[0]+ '"'+ ','+ str(item[1])+ ','+'\n'
        print(resultline)
        results.write(resultline)
            
results.close()
