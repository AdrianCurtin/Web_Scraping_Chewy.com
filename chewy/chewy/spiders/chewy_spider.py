from scrapy import Spider, Request
from chewy.items import ChewyItem
import re, time
import math
from time import sleep
from termcolor import colored

i = 0

class ChewySpider(Spider):
	name='chewy_spider'  #This name will be used for generating files??
	allowed_urls=['https://www.chewy.com']

	#start with the all the cat food
	start_urls=['https://www.chewy.com/b/food-387']
#
	print ("#"*50,'in the start url',"#"*50)




	def parse(self, response):
		# Find number_pages
		
		text=response.xpath('//p[contains(text()," Results")]/text()').extract_first()
		_, items_per_page, total_items=re.findall('\d+', text)
		number_pages = math.ceil(int(total_items) / int(items_per_page))

		# all urls for top food pages
		start_url=['https://www.chewy.com/b/food-387']
		
		result_urls=['https://www.chewy.com/b/food_c387_p'+ str(i) for i in range(2,number_pages+1 )]
		result_urls=start_url+result_urls
		
		#Just One
		
		#test_url='https://www.chewy.com/tiny-tiger-pate-seafood-recipes/dp/168782'
		#yield Request(url=test_url, callback=self.parse_detail_page)
		#return


		#TEST FIRST PAGE
		url_num=0
		for url in result_urls:
			
			#if(url_num==1):
			#	break
				
			url_num=url_num+1
			
			print('#'*100)
			print('\n Scanning  page {} of {}:\t{}'.format(url_num,number_pages,url))
			
			sleep(0.1)	
			headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

			yield Request(url=url, callback=self.parse_result_page)
			

	def parse_result_page(self, response):

		print('parsing details...')
		detail_urls=response.xpath("//div[@class='kib-product-card__canvas']/a/@href").extract()		
						 
		productCountOfPage=1
		num_products=len(detail_urls)

		#Test first 2 products on each catalog page
		for url in detail_urls:   
			if '/' in url[0]:
				print('')
			else:
				#print(url)
				sleep(0.1)	
				#print('#'*50,'\n', 'parsing product ', productCountOfPage, 'of ',num_products,'\n' )
				yield Request(url=url, callback=self.parse_detail_page)
				productCountOfPage=productCountOfPage+1

	def parse_detail_page(self, response):
		global i
			#parse product page
		try: 
		
			print('Parsing {}...\n'.format(response.url))
			
			item=ChewyItem()
			item['url']=response.url	
			
			try:
				print('Parsing product details...\n')
				
				prodInfoXML= [string for string in response.xpath('/html/head/script').extract() if 'categoryId:' in string]
				attributes=[string for string in re.split(':|,|\n',prodInfoXML[0]) if len(string)>1]
				#Top product info
				brandName=attributes[6].strip()
				productID=(attributes[4].strip())
				productName=(response.xpath('//div[@id="product-title"]/h1/text()').extract()[0]).strip()
				price=float(response.xpath('//span[@class="ga-eec__price"]/text()').extract()[0].strip().split('$')[1])

				print(brandName)
				print(productName)
				
				
				item['productName']=productName
				item['brandName']=brandName
				item['price']=price
				item['productID']=productID
				
			except Exception as e:
				print(colored(e,'red'))
			
			try:
				print('Parsing review details...\n')
				
				num_of_reviews=int(response.xpath('//div//span[@class="hide-large"]/text()').extract_first())
				
				percentRec=((re.findall('\d+', response.xpath('//div[@class="ugc-list__recap__recommend"]/p/span').extract()[0]))[0])
				
				ratingText=response.xpath('//div[@class="product-header-extras"]//img//@aria-label').extract()[0]
				ratingVal=ratingText.split(' ')[1]

				
				item['num_of_reviews']=num_of_reviews
				item['percentRec']=percentRec
				
				item['rating']=ratingVal
				
			except Exception as e:
				print(colored(e,'red'))
				
			
			try:
				print('Parsing calorie information...\n')
				
				nutritionInfo=response.xpath('//article[@id="Nutritional-Info"]//section[@class="cw-tabs__content--left"]//p').extract()
				item['ingredients']=re.sub('<[^<]+?>', '', nutritionInfo[0]).strip()
				
				
				calorieInfo=[re.sub('<[^<]+?>', '', string).strip().lower() for string in nutritionInfo if 'kcal' in string.lower()]
				
				if(len(calorieInfo)>0):
					item['numVarieties']=len(calorieInfo)
					
					if(len(calorieInfo)>1 and len(item['ingredients'])<30):
						item['ingredients']=re.sub('<[^<]+?>', '', nutritionInfo[1]).strip()
					
					calorieInfo=calorieInfo[0].replace(' or ',', ')
					
					calorieParts=re.split(':|, |;',calorieInfo)
					
					item['cal_kg']=[string.replace(',','').strip() for string in calorieParts if '/kg' in string]
					item['cal_package']=calorieParts[-1]
						
					if(len(calorieParts)>2):
						item['varietyName']=calorieParts[0]
					else:
						item['varietyName']='NA'
						
						
					packageParts=re.split('/',item['cal_package'])
					item['package_type']=packageParts[-1].strip()
						
				else:
					item['numVarieties']=-1;
					item['varietyName']='';
					item['cal_kg']='';
					item['cal_package']='';
					item['package_type']='';
					
			except Exception as e:
				print(colored(e,'red'))
				
			try:
				print('Parsing nutrition content information...\n')
				
				nutritionContentAll=response.xpath('//article[@id="Nutritional-Info"]//section[@class="cw-tabs__content--right"]//table').extract()
					
				nutritionContent=[re.sub('<[^<]+?>', '', string.replace('align="right">','align="right">:').replace('</td><td>',':')).strip().lower() for string in nutritionContentAll if 'guaranteed analysis' in string.lower()]
				

				if(len(nutritionContent)>0):
					nutritionContent=nutritionContent[0]
				
					nutritionContentParts=re.split('\n',re.sub('\n\n','\n',nutritionContent))
					
					nutritionContentParts_2=[string for string in nutritionContentParts if ':' in string]
				
					somethingFilled=False
					
					for part in nutritionContentParts_2:
						parts=part.split(':')
						firstParts=parts[0].split('(')
						firstPart=firstParts[0].strip().replace(' ','_').replace('-','_').replace('*','')
						secondPart=parts[-1].strip()
						
						if(len(firstParts)>1):
							secondPart='{} {}'.format(secondPart,firstParts[-1])
							secondPart=secondPart.replace(')','')
							
						if 'phosphorous' in firstPart:
							firstPart = 'phosphorus'
						if 'crude_ash' in firstPart:
							firstPart = 'ash'
						if 'omega_3' in firstPart:
							firstPart = 'omega_3_fatty_acids'
						if 'omega_6' in firstPart:
							firstPart = 'omega_6_fatty_acids'
						if 'fiber' == firstPart:
							firstPart = 'crude_fiber'
						if 'protein' == firstPart:
							firstPart = 'crude_protein'

						if 'fat' == firstPart:
							firstPart = 'crude_fat'
						if 'ascorbic' in firstPart or 'asboric' in firstPart or 'vitamin_c'	 in firstPart:
							firstPart = 'ascorbic_acid'
						
						if 'guaranteed_analysis' in firstPart:
							if(somethingFilled):
								break
							else:
								continue
						else:
							item[firstPart]=secondPart.replace('(','').replace(')','')
							somethingFilled=True
					else:
						print('No nutrition info found!\n')
			except Exception as e:
				print(colored(e,'red'))
			
			i=i+1
			
			print('{} records imported'.format(i))
			
			
			yield(item)

			#bottom review section, go to review_page and pass top product info
			
			#for url1 in review_urls: #test first 1
			#	new_url='https://www.chewy.com' + url1

			
			#	yield Request(url= new_url, meta={'brandName': brandName, 'productName':productName, "price":price, "num_of_reviews":num_of_reviews, 'percentRec':percentRec}, callback = self.parse_review_page)
				#yield Request(url = new_url, callback=self.parse_review_page )
				# print('hello!')


		except Exception as e:
			print(colored(e,'red'))
			return

			 

	def parse_review_page(self, response):
		#parse the review pages
		

		print('IN THE PARSE REVIEW PAGE')
		
		print ("####"*50)
		productName=response.meta['productName']
		brandName=response.meta['brandName']
		price=response.meta['price']
		num_of_reviews=response.meta['num_of_reviews']
		percentRec=response.meta["percentRec"]

		#extract all review tags
		reviews=response.xpath('//li[@class="js-content"]')


		for review in reviews:  #test review
			
			date=review.xpath('.//span/@content').extract()
			reviewRating=int(review.xpath('.//@alt').extract()[0].split()[0])
			reviewTitle=(review.xpath('.//h3/text()').extract())[0].strip()
			reviewContent=review.xpath('.//span[@class="ugc-list__review__display"]/text()').extract()
					

			item=ChewyItem()
			item['productName']=productName
			item['brandName']=brandName
			item['price']=price
			item['num_of_reviews']=num_of_reviews

			item['date']=date
			item['reviewRating']=reviewRating
			item['reviewTitle']=reviewTitle
			item['reviewContent']=reviewContent
			item['percentRec']=percentRec

	
			print('\n\n\n')
			print('*'*25,'  collected total review count:  ',i,'	','*'*25)
		# 	print('\n\n\n')
		# 	time.sleep(0.5)
			yield item
		i = i + 1




