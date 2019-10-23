# -*- coding: utf-8 -*-
import csv     
import requests
from bs4 import BeautifulSoup 
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from datetime import datetime

input_file = sys.argv[1]
input_data = []
results = []
with open(input_file) as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
    for row in reader: # each row is a list
        results.append(row[0])
    input_data = results


csv.register_dialect('myDialect1',
      quoting=csv.QUOTE_ALL,
      skipinitialspace=True)
file = open('111.csv', 'a')
writer = csv.writer(file, dialect='myDialect1')
writer.writerow(['paddress', 'pstreet', 'pcity', 'pzipcode', 'property_owner', 'mail', 'city', 'state', 'zipcode', 'sid', 'Saled_Date', 'Saled_Price', 'Saled_Type'])
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Content-Type': 'application/json; charset=UTF-8',
	'Cookie': '_ga=GA1.2.2085390563.1569865179; _gid=GA1.2.116268225.1569865179; _gat_gtag_UA_126241237_1=1',
	'Accept': 'application/json, text/javascript, */*; q=0.01',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'en-US,en;q=0.9',
	'Connection': 'keep-alive',
	'Content-Length': '70'
})

addresslist = []
if input_data:
	addresslist = input_data

for paddress in addresslist:
	url = 'https://web.bcpa.net/BcpaClient/search.aspx/PopulateInput'
	r = session.post(url, data= json.dumps({'value': paddress, 'cities':"", 'arrayOfValues': ""}))
	if 'd' not in json.loads(r.text) or len(json.loads(r.text)['d']) == 0:
		writer.writerow([paddress])
		print([paddress])
		continue
	url = 'https://web.bcpa.net/BcpaClient/search.aspx/GetData'
	print(json.loads(r.text)['d'][0])
	r = session.post(url, data= json.dumps({'value': json.loads(r.text)['d'][0],'cities': "",'orderBy': "NAME",'pageNumber':"1",'pageCount':"5000",'arrayOfValues':"", 'selectedFromList': "false",'totalCount':"Y"}))
	if 'd' not in json.loads(r.text):
		writer.writerow([paddress])
		print([paddress])
		continue
	folio = json.loads(r.text)['d']['resultListk__BackingField'][0]['folioNumber']

	url = 'https://web.bcpa.net/BcpaClient/search.aspx/getParcelInformation'
	r = session.post(url, data=json.dumps({'folioNumber': folio,'taxyear': "2019",'action': "CURRENT",'use':""}))
	data = json.loads(r.text)['d']['parcelInfok__BackingField'][0]
	saled_date = data['saleDate1']
	saled_price = data['stampAmount1']
	saled_type = data['deedType1']
	pcity = data['situsCity']
	pstreet = data['situsNoUnit']
	pzipcode = data['situsZipCode']
	mstreet = data['mailingAddress1']
	mstate = ''
	mzipcode = ''
	if len(data['mailingAddress2'].split(', ')) == 1:
		mcity = data['mailingAddress2']
	else:
		mcity = data['mailingAddress2'].split(', ')[0]
		mstate = data['mailingAddress2'].split(', ')[1].split(' ')[0]
		mzipcode = data['mailingAddress2'].split(', ')[1].split(' ')[1]
	sid = data['bookAndPageOrCin1']
	owner = data['ownerName1']

	writer.writerow([paddress, pstreet, pcity, pzipcode, owner, mstreet, mcity, mstate, mzipcode, sid, saled_date, saled_price, saled_type])


	print([paddress, pstreet, pcity, pzipcode, owner, mstreet, mcity, mstate, mzipcode, sid, saled_date, saled_price, saled_type])
	# soup = BeautifulSoup(r.text, features="html.parser")









# https://web.bcpa.net/BcpaClient/search.aspx/getParcelInformation