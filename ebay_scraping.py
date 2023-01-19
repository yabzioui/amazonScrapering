from lxml import html
import requests
from pprint import pprint
import unicodecsv as csv
from traceback import format_exc
import argparse
import sqlite3


def parse(brand):
	#Test for
	
	try:

		url = 'http://www.ebay.com/sch/i.html?_nkw={0}&_sacat=0'.format(brand)
		headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
		
		#get the page html data
		response = requests.get(url, headers=headers, verify=False)
		
		#print(type(response.status_code))
		#Check the response
		if(response.status_code != 200):
		
			print("Bad response: " + response.status_code)		
		print("Parsing: "+ url)

		pageData = html.fromstring(response.content)
		print(type(pageData))

		product_listings = pageData.xpath('//li[contains(@class,"lvresult")]')
		raw_result_count = pageData.xpath("//span[@class='rcnt']//text()")
		print(product_listings)
		result_count = ''.join(raw_result_count).strip()


		print("Found {0} results for {1}".format(result_count,brand))

		scraped_products = [] # list of scraped products
		#add parsed data to scraped_products
		for product in product_listings:
			raw_url = product.xpath('.//a[@class="vip"]/@href')
			#print(raw_url)
			raw_title = product.xpath('.//a[@class="vip"]/text()')
			#raw_price = pageData.xpath(".//span[@class='prRange']//span[@class='bold']//text()")	
			raw_price = product.xpath(".//li[contains(@class,'lvprice')]//span[@class='bold']//text()")
			#print(raw_title)
			#print(raw_price)
			title = ' '.join(' '.join(raw_title).split())
			price = ' '.join(' '.join(raw_price).split())
			print("Rawprice: ", raw_price)
			print("price: ", price)
			data = {
				
				'title':title,
				'price':price
			}
			scraped_products.append(data)
			addToDB(title, price)
		return scraped_products


	except Exception as e:
		print (e)	

def makeCsvFile(scraped_data):
	with open('%s-ebay-data.csv'%(brand),'wb') as csvfile:
		fieldnames = ["title","price",]
		writer = csv.DictWriter(csvfile, fieldnames = fieldnames, quoting=csv.QUOTE_ALL)
		writer.writeheader()
		for data in scraped_data:
			writer.writerow(data)
def addToDB(title, price):
	conn = sqlite3.connect('sellers.db')
	c = conn.cursor()

	def create_table():
		c.execute("CREATE TABLE IF NOT EXISTS amazon(item TEXT, value TEXT)")

	# def data_entry():
	# 	c.execute("INSERT INTO amazon VALUES('watches', '$19.54')")
	# 	conn.commit()
	# 	c.close()
	# 	conn.close()

	create_table()
	c.execute("INSERT INTO amazon VALUES(title, price) VALUES (?, ?)")
	conn.commit()

	c.close()
	conn.close()
