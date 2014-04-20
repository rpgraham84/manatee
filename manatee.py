#!/usr/bin/env python

from bs4 import BeautifulSoup
import re
import requests
import json

edition_regex = re.compile(r'Edition of (\d+)')
posters = []
baseurl = "http://www.mondotees.com/"
request = requests.get(baseurl)
main_soup = BeautifulSoup(request.text)
available = [baseurl+a.get("href") for a in main_soup.find("ul").findAll("a")]

for url in available:
	new_soup = BeautifulSoup(requests.get(url).text)
	poster = {
		"available": (new_soup.find(\
      id="availability").text.find("Sold Out") < 0),
		"url": url,
		"price": new_soup.find(class_="price").text,
		"title": new_soup.find(class_="page_headers").text,
	}
	try:
		poster["editionof"] = int(edition_regex.findall(\
      new_soup.find(class_="item").text)[0])
	except:
		pass
	posters.append(poster)
	
print json.dumps(posters, indent=2)