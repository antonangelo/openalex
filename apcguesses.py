'''
Using pyalex to guess how much we pay in APCs

anton.angelo@canterbury.ac.nz
Software is unlicensed: https://unlicense.org/
'''

import pprint
from pyalex import config, Works, Authors, Sources, Institutions, Concepts, Publishers, Funders
import pyalex
from itertools import chain
from collections import Counter
import time
import csv
import os

timestr = time.strftime("%Y%m%d-%H%M")
yearstr = time.strftime("%Y")

def pretty_to_file(toprint, filename):
    with open(filename, "w", encoding="utf8") as output:
        pprint.pprint(toprint, output)

config.email = "anton.angelo@canterbury.ac.nz" # set this to your own email.  It puts you in the openalex polite queue
config.max_retries = 0
config.retry_backoff_factor = 0.1
config.retry_http_codes = [429, 500, 503]

institution_ror = "https://ror.org/03y7q9t39"
institution_name = "canterbury"
results_filename =  timestr +".csv"

results_directory = "results/"+timestr+"_"+institution_name+"_apc_guesses/"
if not os.path.exists(results_directory):
    os.makedirs(results_directory)

publication_years = range(2000,2025)

fields_to_report = ["apc_paid","doi","type","authorships","open_access"] # list of data fields to get from open alex

with open(results_directory+results_filename, "w",encoding="utf8", newline='') as resultsfile:
    resultswriter = csv.writer(resultsfile, quotechar='"')
    resultswriter.writerow(["year", "number_of_works", "output_type","oa_status","number_of_authors","doi","usd_value"]) # fieldnames for the CSV file

    for year in publication_years:
        print(year)
        works = Works() \
                .filter(authorships={"institutions": {"ror": institution_ror}}) \
                .filter(is_oa =True) \
                .filter(publication_year=year) \
                .select(fields_to_report) \
                .paginate(per_page=10)

        works_list = []
        for item in chain(*works):
            works_list.append(item)
            
        pretty_to_file(works_list, "results\guess-full"+timestr+".py")

        number_of_works = len(works_list)

        print(number_of_works)



        for research_output in works_list:
            output_type = research_output["type"]
            doi = research_output["doi"]
            number_of_authors = str(len(research_output["authorships"]))
            oa_status = research_output['open_access']['oa_status']
            if research_output["apc_paid"] != None:
                usd_value = str(research_output["apc_paid"]["value_usd"])
            else:
                usd_value = "0"

            result_list=[year, number_of_works, output_type,oa_status,number_of_authors,doi,usd_value]
            print(result_list)
            resultswriter.writerow(result_list)


