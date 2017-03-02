import urllib
import csv
from bs4 import BeautifulSoup
from urllib import request, error, parse
import pymongo
from pymongo import MongoClient
import re

# DB
client = MongoClient()
db = client['obrasjalisco']

url = 'http://201.144.40.96/secip/obrastransparencia'

# Create http request
request = urllib.request.Request(url)
request.add_header('User-agent', 'Mozilla/5.0 (Linux i686)')
html = urllib.request.urlopen(request)
soup = BeautifulSoup(html ,  "html.parser")


rows = soup.find(id="tabla_scroll").find("tbody").find_all("tr",recursive=False)

count = 0
for row in rows:
	cells = row.find_all("td",recursive=False)

	current_year = int(cells[0].get_text().strip())

	year_collection = db['year'+str(current_year)]
	data = {}
	
	contrato_id = cells[1].find('a')['data-idobra']
	data['id_obra'] = str(contrato_id)
	data['contrato'] = str(cells[1].get_text()).strip()
	data['obra'] = str(cells[2].get_text()).strip()
	data['descripcion'] = str(cells[3].get_text()).strip()
	presupuesto = cells[4].get_text().strip()
	price = re.sub('[$,]', '', presupuesto)
	data['presupuesto'] = float(price)
	data['estatus'] = str(cells[5].get_text()).strip()
	
	year_collection.insert(data)


	
	
