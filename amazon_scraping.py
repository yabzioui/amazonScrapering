from lxml import html
import os
import requests
import unicodecsv as csv
from time import sleep
from traceback import format_exc
import argparse
from pprint import pprint

def getAmazonPageData(url):
	#spoof Headers
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}

	response = requests.get(url, headers=headers)

	if (response.status_code != 200):
		print("Bad Response: " + response.status_code)

	print("Parsing: " + url)

	pageData = html.fromstring(response.content)

	product_listings = pageData.xpath("//div[contains(@class,'s-result-list')]")
	print("length of product_listings: ", len(product_listings))
	scraped_products = []
	for product in product_listings:
		raw_price = product.xpath('.//li[contains(@class,"s-result-item")]//div[contains(@class, "s-item-container")]//div[contains(@class,"a-row")]//a[contains(@class,"a-text-normal")]//span[contains(@class,"a-offscreen")]/text()')
		raw_title = product.xpath('.//li[contains(@class,"s-result-item")]//div[contains(@class, "s-item-container")]//div[contains(@class,"a-row")]//a[contains(@class,"a-link-normal")]//h2[contains(@class,"s-access-title")]/text()')
		#print("RawPrice: ", raw_price)
		for i in raw_price:
			try:
				raw_price.remove('[Sponsored]')
			except ValueError:
				pass
		for i in raw_title:
			try:
				raw_title.remove('[Sponsored]')
			except ValueError:
				pass
		# for x in range(0, len(raw_price)):
		# 	if(x == '[Sponsored]'):
		# 		raw_price.remove('[Sponsored]')
		price = (' '.join(raw_price).split())
		title = ' '.join(' '.join(raw_title).split())
		#print(price)
		count =0
		for x in raw_price:

			data = {
			'title':raw_title[count],
			'price':raw_price[count]
			}
			count = count +1
			scraped_products.append(data)
		# data = {
		# 	'title':title,
		# 	'price':price
		# }
		#scraped_products.append(data)
	print("Title Length: " + str(len(raw_title)))
	print("Price lenth: " + str(len(raw_price)))
	return scraped_products


def makeCsvFile(scraped_data, item):
	with open('%samazon-data.csv'%(item),'wb') as csvfile:
		fieldnames = ["title","price",]
		writer = csv.DictWriter(csvfile, fieldnames = fieldnames, quoting=csv.QUOTE_ALL)
		writer.writeheader()
		for data in scraped_data:
			writer.writerow(data)

def beginAmazonScrape(item):
	itemUrl = "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="+item
	scraped_data = getAmazonPageData(itemUrl)
	makeCsvFile(scraped_data, item)