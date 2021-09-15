
# bing-search Example

### Setup

```
git clone https://github.com/arquivo/bing-search.git
cd bing-search
pip install --upgrade virtualenv
virtualenv -p python3 venv
source venv/bin/activate
```

### Parameters

<pre>
-q or --queries_list_file --> File (.TXT) with list of queries to be performed. (e.g., "lisboa" or "fishing site:fishing.contoso.com").
-r or --results_file      --> File (.TSV) to write out results.
-k or --key               --> Environment variable with Bing Service Subscription Key.
-n or --results_number    --> Number of results returned.
</pre>

### Run default

```
python bing_search.py -k <azure_key>
```

### Authors

- [Pedro Gomes](pedro.gomes@fccn.pt)
