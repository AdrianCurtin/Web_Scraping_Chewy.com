# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ChewyItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	
	#Product Info
	
	productName = scrapy.Field() #individual rating, need to calculate individual rate by myself
	productID = scrapy.Field()
	brandName = scrapy.Field()
	url = scrapy.Field()
	
	price = scrapy.Field()
	rating = scrapy.Field()
	num_of_reviews = scrapy.Field()
	percentRec=scrapy.Field()
	
	numVarieties = scrapy.Field()
	varietyName = scrapy.Field()
	
	package_type = scrapy.Field()
	cal_kg = scrapy.Field()
	cal_package = scrapy.Field()
	
	crude_protein = scrapy.Field()
	crude_fat = scrapy.Field()
	crude_fiber = scrapy.Field()
	moisture = scrapy.Field()
	ash = scrapy.Field()
	carbohydrates = scrapy.Field()
		
	calcium = scrapy.Field()
	linoleic_acid = scrapy.Field()
	taurine = scrapy.Field()
	phosphorus= scrapy.Field()
	potassium = scrapy.Field()
	ascorbic_acid  = scrapy.Field()
	selenium = scrapy.Field()
	iron = scrapy.Field()
	arachidonic_acid = scrapy.Field()
	zinc = scrapy.Field()
	vitamin_a = scrapy.Field()
	vitamin_e = scrapy.Field()
	beta_carotene = scrapy.Field()
	omega_3_fatty_acids = scrapy.Field()
	omega_6_fatty_acids = scrapy.Field()
	steak_frites = scrapy.Field()
	l_carnitine = scrapy.Field()
	l_cartinine = scrapy.Field()
	magnesium = scrapy.Field()
	docosahexaenoic_acid = scrapy.Field()
	total_lactic_acid_microorganisms = scrapy.Field()
	glucosamine = scrapy.Field()
	dha = scrapy.Field()
	methionine_custime = scrapy.Field()
	niacin = scrapy.Field()
	methionine=scrapy.Field()
	chondroitin_sulfate=scrapy.Field()
	
	
	ingredients = scrapy.Field()
	
	