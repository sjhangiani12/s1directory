import json
import urllib.request
import pandas as pd


# API Key
TOKEN = "6b2487e582e186708c492280e1638c3d7888da05699bc227fe70cbd8668fe1ad" # replace YOUR_API_KEY with the API key you got from sec-api.io after sign up
# API endpoint
API = "https://api.sec-api.io?token=" + TOKEN

def get_query(ticker):
    # Define the filter parameters
    filter = "ticker:" + ticker + " AND formType:\"S-1\""

    # Start with the first filing. Increase it when paginating. 
    # Set to 10000 if you want to fetch the next batch of filings. Set to 20000 for the next and so on.
    start = 0
    # Return 10,000 filings per API call
    size = 100
    # Sort in descending order by filedAt
    sort = [{ "filedAt": { "order": "desc" } }]

    payload = {
    "query": { "query_string": { "query": filter } },
    "from": start,
    "size": size,
    "sort": [
        {
            "filedAt": {
                "order": "desc"
            }
        }
    ]
    }

    # Format your payload to JSON bytes
    jsondata = json.dumps(payload)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes

    # Instantiate the request 
    req = urllib.request.Request(API)

    # Set the correct HTTP header: Content-Type = application/json
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    # Set the correct length of your request
    req.add_header('Content-Length', len(jsondataasbytes))

    # Send the request to the API
    response = urllib.request.urlopen(req, jsondataasbytes)

    # Read the response 
    res_body = response.read()
    # Transform the response into JSON
    filingsJson = json.loads(res_body.decode("utf-8"))

    return filingsJson['filings']    
