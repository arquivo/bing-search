import argparse
import os
import time
import requests

parser = argparse.ArgumentParser(description="Web Search API v7 query parameters.")
parser.add_argument('-q', '--queries_list_file', default="queries_list.txt", 
                    help="File (.TXT) with list of queries to be performed. (e.g., \"lisboa\" or \"fishing site:fishing.contoso.com\").")
parser.add_argument('-r', '--results_file', default="query_results.tsv", 
                    help="File (.TSV) to write out results.")
parser.add_argument('-k', '--key', default="AZURE_KEY",
                    help="Environment variable with Bing Service Subscription Key. (AZURE_KEY)")
parser.add_argument('-n', '--results_number', type=int, default=10, 
                    help="Number of results returned.")

args = vars(parser.parse_args())

queries_list = args["queries_list_file"]
results_file = args["results_file"]

list_urls = []
with open(queries_list, mode='r') as input_file, open(results_file, mode='a') as output_file:

    output_file.write("{}\t{}\t{}\t{}\n".format("Query", "Type Search", "Title Result", "URL"))
    list_lines = input_file.readlines()
    
    for line in list_lines:
        search_term = line.rstrip()
        try:
            params = {"q": search_term}
            params["count"] =  args["results_number"]
            
            headers = {"Ocp-Apim-Subscription-Key": args["key"]}

            search_url = "https://api.bing.microsoft.com/v7.0/search"
            response = requests.get(search_url, headers=headers, params=params)
            response.raise_for_status()
            search_results = response.json()

            for i,result in enumerate(search_results["webPages"]["value"]):
                if result["url"] not in list_urls:
                    output_file.write("{}\t{}\t{}\t{}\n".format(search_term, "Webpage", result["name"], result["url"]))
                    list_urls.append(result["url"])

        except Exception as err:
            print("Exception {}".format(err))
            
        time.sleep(1)