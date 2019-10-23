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
file = open('11_20_2019 PB Tax Deed Auction List__scraped.csv', 'a')
writer = csv.writer(file, dialect='myDialect1')
writer.writerow(['Location', 'Location Street', 'Location Municipality', 'Owner', 'Mailing Address', 'Mailing Street', 'Mailing City', 'Mailing State', 'Mailing Zipcode', 'SaleDate', 'SalePrice','SaleType', 'parcel control number'])

address_list = []
if input_data:
	addresslist = input_data

session = requests.Session()

session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
	'Cookie': '_ga=GA1.2.990083083.1567017963; _gid=GA1.2.953115123.1567017963; BIGipServer~external~www.pbcgov.com_papa=rd102o00000000000000000000ffff978433b0o80; ASP.NET_SessionId=oluqmbqiyhhts22tefyfix4e; _gat_gtag_UA_117168590_1=1; _gat_gtag_UA_70407948_1=1'
})
session = requests.Session()

for address in address_list:
	url = 'https://pbcgov.org/papa/Asps/GeneralAdvSrch/NewSearchResults.aspx?srchType=MASTER&proptype=RE&srchVal={}&srchPCN='
	# 1009%20BIG%20TORCH%20ST
	r = session.get(url.format(address.replace(' ', '%20')))
	soup = BeautifulSoup(r.text, features="html.parser")
	# f = open('1.html', 'a')
	# f.write(r.text)
	# f.close()
	# print(soup.find('div', {'id': 'ownerInformationDiv'}).find('table').findAll('table')[0])
	if soup.find('div', {'id': 'ownerInformationDiv'}):
		owner = soup.find('div', {'id': 'ownerInformationDiv'}).find('table').findAll('table')[0].findAll('td', class_='TDValueLeft')[0].text
		mailing = (soup.find('div', {'id': 'ownerInformationDiv'}).find('table').findAll('table')[1].findAll('td', class_='TDValueLeft')[0].text + soup.find('div', {'id': 'ownerInformationDiv'}).find('table').findAll('table')[1].findAll('td', class_='TDValueLeft')[2].text).strip().replace('\n\n', ',')
		mstreet = mailing.split(',')[0]
		mcity = ''
		mzipcode = ''
		mstate = ''
		if len(mailing.split(',')) >=2:
			scount = len(mailing.split(',')[1].split(' '))
			mcity = mailing.split(',')[1].replace(mailing.split(',')[1].split(' ')[scount - 3] + ' ' + mailing.split(',')[1].split(' ')[scount - 2] + ' ' + mailing.split(',')[1].split(' ')[scount - 1], '').strip()
			mzipcode = mailing.split(',')[1].split(' ')[scount - 2] + ' ' + mailing.split(',')[1].split(' ')[scount - 1].strip()
			mstate =  mailing.split(',')[1].split(' ')[scount - 3]
			# if mailing.split(',')[1].split('FL')[0]:
			# 	mcity = mailing.split(',')[1].split('FL')[0].strip()
			# if len(mailing.split(',')[1].split('FL')) >= 2:
			# 	mzipcode = mailing.split(',')[1].split('FL')[1].strip()
			# else:
			# 	if mailing.split(',')[1].split('NY')[0]:
			# 		mstate = 'NY'
			# 		mcity = mailing.split(',')[1].split('NY')[0].strip()
			# 	if len(mailing.split(',')[1].split('NY')) >= 2:
			# 		mstate = ''
			# 		mzipcode = mailing.split(',')[1].split('NY')[1].strip()

		location = (soup.find('div', {'id': 'propertyDetailDiv'}).findAll('td', class_='TDValueLeft')[0].text + ',' + soup.find('div', {'id': 'propertyDetailDiv'}).findAll('td', class_='TDValueLeft')[1].text).strip().replace('\n', '')

		lstreet = soup.find('div', {'id': 'propertyDetailDiv'}).findAll('td', class_='TDValueLeft')[0].text.strip().replace('\n', '')
		lmunicipality = soup.find('div', {'id': 'propertyDetailDiv'}).findAll('td', class_='TDValueLeft')[1].text.strip().replace('\n', '')
		pcn = soup.find('div', {'id': 'propertyDetailDiv'}).findAll('td', class_='TDValueLeft')[2].text.strip()
		saledate = ''
		saleprice = ''
		saletype = ''
		if soup.find('table', {'id': 'MainContent_tblSalesInfo'}):
			saleinfo = soup.find('table', {'id': 'MainContent_tblSalesInfo'}).findAll('tr', class_='gridrow')[0]
			saledate = saleinfo.findAll('td')[0].text
			saleprice = saleinfo.findAll('td')[1].text
			saletype = saleinfo.findAll('td')[3].text.strip()
		lastsaledate = soup.find('div', {'id': 'propertyDetailDiv'}).findAll('td', class_='TDValueLeft')[5].text.strip()
		print(location, lstreet, lmunicipality, owner, mailing, mstreet, mcity, mstate, mzipcode, saledate, saleprice, saletype, pcn)
		writer.writerow([location, lstreet, lmunicipality, owner, mailing, mstreet, mcity, mstate, mzipcode, saledate, saleprice, saletype, pcn])

# print(r.text)