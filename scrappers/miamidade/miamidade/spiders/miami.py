import scrapy
import urllib
import json
from miamidade.items import MiamidadeItem
import datetime
import time
import pdb
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class MiamiProperty(scrapy.Spider):
    name = "miami_prop"

    def __init__(self, input_file):
        results = []
        with open(input_file) as csvfile:
            reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
            for row in reader: # each row is a list
                results.append(row[0])
            self.input_data = results

    def start_requests(self):
        addressList = []
        if self.input_data:
            addressList = self.input_data

        for address in addressList:
            url = 'https://www8.miamidade.gov/Apps/PA/PApublicServiceProxy/PaServicesProxy.ashx?Operation=GetAddress&clientAppName=PropertySearch&from=1&myAddress={}&myUnit=&to=200'
            wild = address
            address = address.replace(' ', '+')
            address = address.replace('#', '%23')
            yield scrapy.Request(url.format(address), callback=self.parse_info, method="GET", meta={'address': wild})


        # for folio in folios:
        #     url = 'https://www8.miamidade.gov/Apps/PA/PApublicServiceProxy/PaServicesProxy.ashx?Operation=GetPropertySearchByFolio&clientAppName=PropertySearch&folioNumber={}'
        #     yield scrapy.Request(url.format(folio.replace('-', '')), callback=self.parse_detail, method="GET")

    def parse_info(self, response):
        if len(json.loads(response.body)['MinimumPropertyInfos']) == 0:
            item = MiamidadeItem()
            item['Address'] = response.meta['address']
            
            yield item
            pass
        for info in json.loads(response.body)['MinimumPropertyInfos']:
            url = 'https://www8.miamidade.gov/Apps/PA/PApublicServiceProxy/PaServicesProxy.ashx?Operation=GetPropertySearchByFolio&clientAppName=PropertySearch&folioNumber={}'

            yield scrapy.Request(url.format(info['Strap'].replace('-', '')), callback=self.parse_detail, method="GET")

    def parse_detail(self, response):
        data = json.loads(response.body)
        item = MiamidadeItem()
        item['FolioNumber'] = data['PropertyInfo']['FolioNumber']
        # item['Subdivision'] = data['PropertyInfo']['SubdivisionDescription']
        item['Address'] = data['SiteAddress'][0]['Address']
        # 945 NW 19 AVE, Miami, FL 33125-3565
        item['AStreet'] = item['Address'].split(',')[0]
        item['ACity'] = item['Address'].split(',')[1]
        item['AState'] = item['Address'].split(',')[2].split(' ')[1]
        item['AZipcode'] = item['Address'].split(',')[2].split(' ')[2]



        item['Owner'] = data['OwnerInfos'][0]['Name']
        mail_addr = "{}, {}, {} {}"
        item['MailingAddress'] = mail_addr.format(data['MailingAddress']['Address1'], data['MailingAddress']['City'], data['MailingAddress']['State'], data['MailingAddress']['ZipCode'])
        item['MStreet'] = data['MailingAddress']['Address1']
        item['MCity'] = data['MailingAddress']['City']
        item['MState'] = data['MailingAddress']['State']
        item['MZipcode'] = data['MailingAddress']['ZipCode']
        if len(data['SalesInfos']) > 0:
            item['Sale_Date'] = data['SalesInfos'][len(data['SalesInfos']) - 1]['DateOfSale']
            item['Sale_Price'] = data['SalesInfos'][len(data['SalesInfos']) - 1]['SalePrice']
            item['Sale_Type'] = data['SalesInfos'][len(data['SalesInfos']) - 1]['QualificationDescription']
        yield item
        pass
            
        
