import requests
import argparse
import json

parser = argparse.ArgumentParser(description="Web Search API v7 query parameters.")
parser.add_argument('-q', '--queries_list_file', default="queries_list.txt", 
                    help="File (.TXT) with list of queries to be performed. (e.g., \"lisboa\" or \"fishing site:fishing.contoso.com\").")
parser.add_argument('-r', '--results_file', default="query_results.tsv", 
                    help="File (.TSV) to write out results.")
parser.add_argument('-k', '--key', default="AZURE_KEY",
                    help="Environment variable with Bing Service Subscription Key. (AZURE_KEY)")
parser.add_argument('-s', '--safeSearch', default="NO", 
                    help="Off, Moderate, or Strict.")
parser.add_argument('-l', '--setLanguage', type=bool, default=False, 
                    help="Boolean to force language. True (PT-PT), False (All languages).")
parser.add_argument('-t', '--freshness', default="NO", 
                    help="Day, Week, or Month.")
parser.add_argument('-n', '--results_number', type=int, default=20, 
                    help="Number of results returned.")
parser.add_argument('-o', '--offset', type=int, default=9999, 
                    help="Indicates the number of search results to skip before returning results.")
parser.add_argument('-f', '--sortBy', default="NO", 
                    help="Date or Relevance. Only used of news and can not be used. Since is already set by default using both.")
parser.add_argument('-y', '--type_search', default="NO", 
                    help="Webpage, Image, News, or Video.")

args = vars(parser.parse_args())

headers = {"Ocp-Apim-Subscription-Key": args["key"]}

queries_list = args["queries_list_file"]
with open(queries_list, mode='r') as input_file:
    for line in input_file:
        offset_bool = False
        search_term = line.rstrip()
        range_index = 1
        #Check if results_number is bigger than 50. If so, we will increment the offset.
        if args["results_number"] > 50:
            range_index = int(args["results_number"]/20)
            offset_bool = True
        #To increment the offset. If results_number is less than 50 the range_index is 1.
        for i in range(0, range_index):
            params = {"q": search_term}
            if offset_bool:
                params["offset"] = 20*i
                params["count"] = 20
            else:
                if args["offset"] != 9999:
                    params["offset"] =args["offset"]
                params["count"] = args["results_number"]
            if args["setLanguage"]:
                params["setLang"] = "pt-PT"
                params["cc"] = "PT"
            if args["freshness"] != "NO":
                params["freshness"] = args["freshness"]
            if args["safeSearch"] != "NO":
                params["safeSearch"] = args["safeSearch"]

            ####Search Web
            #Parameters:
            #https://docs.microsoft.com/en-us/bing/search-apis/bing-web-search/reference/query-parameters
            if args["type_search"] != "Webpage":
                search_url = "https://api.bing.microsoft.com/v7.0/search"
                response = requests.get(search_url, headers=headers, params=params)
                response.raise_for_status()
                search_results = response.json()
                with open(args["results_file"], mode='a') as output_file:
                    for i,result in enumerate(search_results["webPages"]["value"]):
                        print("Writing result Web: {}".format(result["url"]))
                        output_file.write("{}\t{}\t{}\t{}\n".format(search_term, i+1, result["name"], result["url"]))
            
            ####Search Image
            #Parameters:
            #https://docs.microsoft.com/en-us/bing/search-apis/bing-image-search/reference/query-parameters
            if args["type_search"] != "Image":
                search_url = "https://api.bing.microsoft.com/v7.0/images/search"  
                response = requests.get(search_url, headers=headers, params=params)
                response.raise_for_status()
                search_results = response.json()
                with open(args["results_file"], mode='a') as output_file:
                    for i,result in enumerate(search_results["value"]):
                        print("Writing result Images: {}".format(result["hostPageUrl"]))
                        output_file.write("{}\t{}\t{}\t{}\n".format(search_term, i+1, result["name"], result["hostPageUrl"]))
            
            ####Search News
            #The parameter "category": "Politics" it not returns new news. e.g., search_term = Andre Ventura
            #Parameters:
            #https://docs.microsoft.com/en-us/bing/search-apis/bing-news-search/reference/query-parameters
            
            if args["type_search"] != "News":
                #sortBy default
                search_url = "https://api.bing.microsoft.com/v7.0/news/search"
                response = requests.get(search_url, headers=headers, params=params)
                response.raise_for_status()
                search_results = response.json()
                with open(args["results_file"], mode='a') as output_file:
                    for i,result in enumerate(search_results["value"]):
                        print("Writing result News: {}".format(result["url"]))
                        output_file.write("{}\t{}\t{}\t{}\n".format(search_term, i+1, result["name"], result["url"]))

                #if args["sortBy"] != "NO":
                #    params["sortBy"] = args["sortBy"]
                #sortBy = Relevance
                params["sortBy"] = "Relevance"
                response = requests.get(search_url, headers=headers, params=params)
                response.raise_for_status()
                search_results = response.json()
                with open(args["results_file"], mode='a') as output_file:
                    for i,result in enumerate(search_results["value"]):
                        print("Writing result News: {}".format(result["url"]))
                        output_file.write("{}\t{}\t{}\t{}\n".format(search_term, i+1, result["name"], result["url"]))

                #sortBy = Date
                params["sortBy"] = "Date"
                response = requests.get(search_url, headers=headers, params=params)
                response.raise_for_status()
                search_results = response.json()
                with open(args["results_file"], mode='a') as output_file:
                    for i,result in enumerate(search_results["value"]):
                        print("Writing result News: {}".format(result["url"]))
                        output_file.write("{}\t{}\t{}\t{}\n".format(search_term, i+1, result["name"], result["url"]))

            ####Search Videos (Including youtube, facebook, ...)
            #Parameters:
            #https://docs.microsoft.com/en-us/bing/search-apis/bing-video-search/reference/query-parameters
            if args["type_search"] != "Videos":
                search_url = "https://api.bing.microsoft.com/v7.0//videos/search"
                response = requests.get(search_url, headers=headers, params=params)
                response.raise_for_status()
                search_results = response.json()
                with open(args["results_file"], mode='a') as output_file:
                    for i,result in enumerate(search_results["value"]):
                        print("Writing result Videos: {}".format(result["hostPageUrl"]))
                        output_file.write("{}\t{}\t{}\t{}\n".format(search_term, i+1, result["name"], result["hostPageUrl"]))

            ####Search News trendingTopics
            #Only works for international news (en-us) and the query parameter is not working correctly.
            #search_url = "https://api.bing.microsoft.com/v7.0/news/trendingtopics"
            #params = {"mkt": "en-us", "q": search_term}
            #response = requests.get(search_url, headers=headers, params=params)
            #print(json.dumps(search_results, indent=4))
            