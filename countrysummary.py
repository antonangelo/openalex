'''
fwci_by_institution
Open Alex - Getting Field Weighted Citation Data For An Institution.
anton.angelo@canterbury.ac.nz
Software is unlicensed: https://unlicense.org/
'''
import pprint
from pyalex import config, Works, Authors, Sources, Institutions, Concepts, Publishers, Funders
# import pyalex
import os

import time
import csv

def pretty_to_file(toprint, filename): #function to make a nicely readable JSON file
    with open(filename, "w", encoding="utf8") as output:
        pprint.pprint(toprint, output)

# get a timestring to make a filename/directory for your results, then make the directory. 
timestr = time.strftime("%Y%m%d-%H%M")
yearstr = time.strftime("%Y")

# ISO country code that we are interested in getting data for

country_code = "us" # set this (iso two letter country code: nz/gb/au/us...)
results_filename =  country_code + "_results.csv"

results_directory = "results/"+timestr+"_country_summary_"+country_code+"/"
if not os.path.exists(results_directory):
    os.makedirs(results_directory)

#some pyalex stuff to avoid crashing at the cirst error, and get into the polite pool

config.email = "anton.angelo@canterbury.ac.nz" # set this to your own email.  It puts you in the openalex polite queue
config.max_retries = 0
config.retry_backoff_factor = 0.1
config.retry_http_codes = [429, 500, 503]

# What years are we interested in getting data for.  Expects a list.
publication_years =  range(2010,2025) # ['2020'] 



# get a list of institutions for the specific country, their RORs and overall publishing

institutions = Institutions() \
    .filter(country_code=country_code) \
    .get()

pretty_to_file(institutions, results_directory + country_code+"_institutions_full.py")

# list of unique ROR codes foir your country.  By default the top 20 institutions.

rors_dict ={}
for institution in institutions:
    rors_dict[institution["display_name"]] =institution["ror"]

pretty_to_file(rors_dict, results_directory + country_code+"_institutions_short.py")

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
