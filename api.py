from urllib.request import urlopen
import json

def getResults(searchTerm:str, resultsAmount:int):
    try:
        url = f'http://127.0.0.1:8090/yacysearch.json?query={searchTerm}&resource=global&urlmaskfilter=.*&prefermaskfilter=all&maximumRecords={resultsAmount}'
        response = urlopen(url)
        finalData = json.loads(response.read())
        return finalData["channels"][0]["items"]
    except Exception as e:
        print(e)    
        return {"error":"No result was found"}