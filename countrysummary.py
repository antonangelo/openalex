'''
Using pyalex to get a country's overall OA status

anton@angelo.nz
'''
import pprint
from pyalex import Works, Authors, Sources, Institutions, Concepts, Publishers, Funders
import pyalex
import os

import time
import csv

timestr = time.strftime("%Y%m%d-%H%M%S")
yearstr = time.strftime("%Y")

results_directory = timestr+"/"
if not os.path.exists(results_directory):
    os.makedirs(results_directory)

def pretty_to_file(toprint, filename):
    with open(filename, "w", encoding="utf8") as output:
        pprint.pprint(toprint, output)

pyalex.config.email = "anton.angelo@canterbury.ac.nz" # set this to your own email.  It puts you in the openalex polite queue
publication_years =  range(2000,2024)

# ISO country code that we are interested in getting data for

country_code = "au" # set this
results_filename =  country_code + "_results.csv"



# get a list of institutions for the specific country, their RORs and overall publishing
#use the pyalex https://github.com/J535D165/pyalex library 
institutions = Institutions() \
    .filter(country_code=country_code) \
    .get()

pretty_to_file(institutions, results_directory + country_code+"_institutions_full.py")

# list of unique ROR codes 

rors_dict ={}
for institution in institutions:
    rors_dict[institution["display_name"]] =institution["ror"]

pretty_to_file(rors_dict,  results_directory + country_code+"_institutions_short.py")

# get a breakdown of open access works for each nz institution


results = open( results_directory + results_filename, "w", encoding='utf8')
results.write("institution, ror, year, count, oa status \n")

for institution_name in rors_dict.keys():
    for publication_year in publication_years:
        ror_url = rors_dict[institution_name]
        #make an openalex query for the instituion, the specific year, and group by OA status
        institution_works_oa = Works() \
            .filter(authorships={"institutions":{"ror":ror_url}}, publication_year=publication_year) \
            .group_by("oa_status") \
            .get()
        # get a pretty wee comma delimited list and pop them in a file    
        for counts in institution_works_oa:
            resultline = '"'+institution_name+'",'+ ror_url+","+ str(publication_year)+","+str(counts['count'])+","+str(counts['key'])+"\n"
            print(resultline)
            results.write(resultline)

results.close()
