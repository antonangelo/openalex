'''
fwci_by_institution
Open Alex - Getting Field Weighted Citation Data For An Institution.
anton.angelo@canterbury.ac.nz
Software is unlicensed: https://unlicense.org/
'''
import pprint
from pyalex import Works, Authors, Sources, Institutions, Concepts, Publishers, Funders
import pyalex
import os
import time
import csv

# set up filenames and directories for the CSV output.
timestr = time.strftime("%Y%m%d-%H%M%S")
yearstr = time.strftime("%Y")

institution = 'https://ror.org/03y7q9t39' #canterbury see https://ror.org/ for more
institution_name = 'canterbury'

results_directory = "results/"+timestr+"_fwci_"+institution_name+"/"
if not os.path.exists(results_directory):
    os.makedirs(results_directory)
results_filename = timestr+"_fwci.csv"

#Function for writing nicely formatted JSON to a file

def pretty_to_file(toprint, filename):
    with open(filename, "w", encoding="utf8") as output:
        pprint.pprint(toprint, output)

pyalex.config.email = "anton.angelo@canterbury.ac.nz" # set this to your own email.  It puts you in the openalex polite queue


publication_years =  range(2014,2024) # list of years to get results for ['2010'] 


with open( results_directory + results_filename, "w", encoding='utf8', newline='') as resultsfile:
    resultswriter = csv.writer(resultsfile, quoting=csv.QUOTE_ALL)
    resultswriter.writerow(["doi", "id", "publication_year","title", "oa_status", "fwci", "cited_by_count", "primary_topic", "subfield", "domain", "field"])


    for publication_year in publication_years:
        ror_url = institution # you could put a list of institutions here and loop through them
        
        #create an pyalex query object
        pager= Works() \
            .filter(\
                authorships={"institutions":{"ror":ror_url}}, \
                publication_year=publication_year,\
                is_retracted=False,\
                type="article" 
                ) \
            .select([\
                "doi",\
                "id",\
                "publication_year",
                "title",\
                "open_access",\
                "fwci",\
                "primary_topic",\
                "cited_by_count"\
                ]) \
            .paginate(per_page=5)
            
        for institution_works in pager: #loop though each pager object
            try:
                for work in institution_works:
                    #print(work) 
                    
                    #create a list from the JSON in order to put into csvwriter
                    line_list = [\
                        work['doi'], \
                        work['id'],
                        work['publication_year'],\
                        work['title'],
                        work['open_access']['oa_status'],\
                        work['fwci'],
                        work['cited_by_count'],\
                        work['primary_topic']['display_name'],\
                        work['primary_topic']['subfield']['display_name'],\
                        work['primary_topic']['domain']['display_name'],\
                        work['primary_topic']['field']['display_name']\
                        ]  
                    print(line_list)
                    resultswriter.writerow(line_list)
            except Exception as e: #general purpose shotgun error handling
                print("Error: ",e)
                pass


