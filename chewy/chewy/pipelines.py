# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter

from chewy.settings import FEED_EXPORT_FIELDS

# class ChewyPipeline(object):
# 	def process_item(self,)

class WriteItemPipeline(object):

	def __init__(self):
		self.filename = 'chewy_review.csv'

	def open_spider(self, spider):
		self.csvfile = open(self.filename, 'wb')
		self.exporter = CsvItemExporter(self.csvfile)
		self.exporter.fields_to_export = FEED_EXPORT_FIELDS
		self.exporter.start_exporting()

	def close_spider(self, spider):
		self.exporter.finish_exporting()
		self.csvfile.close()

	def process_item(self, item, spider):
		self.exporter.export_item(item)
		return item
