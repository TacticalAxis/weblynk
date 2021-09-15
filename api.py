from urllib.request import urlopen
import json

def getResults(searchTerm:str, resultsAmount:int):
    try:
        url = f'http://192.168.1.19:8090/yacysearch.json?query={searchTerm}&resource=global&urlmaskfilter=.*&prefermaskfilter=all&maximumRecords={resultsAmount}'
        response = urlopen(url)
        finalData = json.loads(response.read())
        # print(finalData["channels"][0]["items"][0]["link"])
        return finalData["channels"][0]["items"]
    except Exception as e:
        print(e)    
        return {"error":"No result was found"}

# getResults("minecraft", 100)