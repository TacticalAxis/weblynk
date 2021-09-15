from flask import Blueprint, render_template, request
from api import getResults
import requests
from bs4 import BeautifulSoup
import wikipedia
import random

views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("index.html")

@views.route("/search", methods=['GET', 'POST'])
def search():
    searchText = request.form.get('search')
    searchText = searchText.strip()
    data = getResults(searchText, 100)
    finalData = []
    for i in data:
        if len(i['description'].strip()) > 0:
            finalData.append(i)
    
    url = f"http://en.wikipedia.org/wiki/{searchText}"

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html5lib")
    soupImgs = soup.find_all("td", class_="infobox-image")
    imgUrl = None

    shortDesc = None
    try:
        shortDesc = wikipedia.page(searchText)
    except wikipedia.DisambiguationError as e:
        s = random.choice(e.options)
        shortDesc = wikipedia.page(s)
    
    shortDesc = wikipedia.summary(shortDesc, sentences=3)
    if len(soupImgs) > 0:
        mainImgExts = soupImgs[0].find_all_next("img")
        if len(mainImgExts) > 0:
            imgUrl = mainImgExts[0]['srcset'].replace("//", "https://").split()[0]

    if imgUrl != None:
        return render_template("search_with_image.html", resultData=finalData, searchTerm=searchText, numResults=len(finalData), preview=imgUrl, desc=shortDesc)
    else:
        return render_template("search_no_image.html", resultData=finalData, searchTerm=searchText, numResults=len(finalData), preview=imgUrl, desc=shortDesc)