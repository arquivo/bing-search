
# bing-search
Script bing search API

### Setup

```
git clone https://github.com/arquivo/bing-search.git
cd bing-search
pip install --upgrade virtualenv
virtualenv -p python3 venv
source venv/bin/activate
```
### Run

```
python bing_search.py
```

### Parameters script

<pre>
-q or --queries_list_file --> File (.TXT) with list of queries to be performed. (e.g., "lisboa" or "fishing site:fishing.contoso.com").
-r or --results_file      --> File (.TSV) to write out results.
-k or --key               --> Environment variable with Bing Service Subscription Key.
</pre>

### Parameters bing api

<pre>
-s or --safeSearch        --> Off, Moderate, or Strict.
-l or --setLanguage       --> Boolean to force language. True (PT-PT), False (All languages)
-t or --freshness         --> Day, Week, or Month.
-n or --results_number    --> Number of results returned. The default is 20 and the maximum is 50. If you want more than 50 results use multiples of 20.
-o or --offset            --> Indicates the number of search results to skip before returning results. Only use if results_number is less than 50.
</pre>

### Explication of the parameters and relations between them

If none of the parameters are defined, for example, "freshness", we will assume the default values of the bing, that is, it would be the same as a simple query without time range. So just set the parameters if you wanted to override.

#### "safeSearch"

The parameter is used to filter webpages, images, and videos for adult content. The following are the possible filter values:

Off — Returns content with adult text and images but not adult videos.<br>
Moderate — Returns webpages with adult text, but not adult images or videos.<br>
Strict — Does not return adult text, images, or videos.<br>
The default is Moderate. For video results, if safeSearch is set to Off, Bing ignores it and uses Moderate. If you use the site: query operator, there is a chance that the response may contain adult content regardless of what the safeSearch query parameter is set to. Use site: only if you are aware of the content on the site and your scenario supports the possibility of adult content.

#### "setLanguage"

The parameter is used to filter the language of the webpages, images, and videos. Since in our case only matters PT (True) or all language (False).

True - we will set the parameter "setLang" = "pt-PT" and the parameter "cc" = "PT".<br>
False - It is the default and will search for all languages including PT.<br>

In the case of Portugal, the parameter "mkt" or "Market" is not available.

#### "freshness" 

Filter search results by the following case-insensitive age values:

Day — Return webpages\image\news\videos that Bing discovered within the last 24 hours.<br>
Week — Return webpages\image\news\videos that Bing discovered within the last 7 days.<br>
Month — Return webpages\image\news\videos that Bing discovered within the last 30 days.<br>

To get articles discovered by Bing during a specific timeframe, specify a date range in the form, YYYY-MM-DD..YYYY-MM-DD. or to limit the results to a single date set this parameter to a specific date YYYY-MM-DD.

#### "results_number"
The number of search results to return in the response. The actual number delivered may be less than requested. The defaults:

Webpage - The default is 10 and the maximum is 50.<br>
Image - The default is 35 and the maximum is 150.<br>
News - The default is 10 and the maximum is 100.<br>
Video - The default is 35 and the maximum is 105.<br>

Due to the difference between the previous numbers and the fact that the maximum value is low for our case. <br>
We set a maximum of 50, but if you want more than 50 it is possible, it just has to be a number that is possible to divide by 20 (e.g., 100). In this case, we will use automatically the "offset" parameter. For example, if you want 100 results, we will automatically set count to 20 and offset to 0 to get the first results, and then increment offset by 20 (for example, 0, 20, 40...). NOTE: Multiple pages can include some overlap in results.

#### "offset"
The offset indicates the number of search results to skip before returning results. The default is 0. Use this parameter along with the results_number parameter jump between page results. However, do not use the parameter offset if results_number is greater than 50.

### Example

Example and default parameters:

```
python bing_search.py
```

### Authors

- [Pedro Gomes](pedro.gomes@fccn.pt)
