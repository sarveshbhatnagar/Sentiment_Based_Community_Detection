import json
import os,sys
from crawler import Crawler
from sentiment import Sentiment
from associate import Associate
from community import Community

try:
	inp = open("config.json","r")
	config = json.load(inp)
except OSError as e:
	print('error locating file',e)
	sys.exit()
except json.JSONDecodeError as e:
	print('error reading JSON',e)
	sys.exit()

if config["getData"]:
	try:
		crawler = Crawler(config)
		#crawler.crawl()
		print('crawled')
	except:
		print('Issue with web crawler', sys.exc_info())
		sys.exit()
	try:
		classifier = Sentiment(config)
		classifier.classify()
		print('classified')
	except:
		print('Issue with sentiment analyser', sys.exc_info())
		sys.exit()
	try:
		associator = Associate(config)
		associator.associate()
		print('associated')
	except:
		print('Issue with association', sys.exc_info())
		sys.exit()
	try:
		community = Community(config)
		community.communities()
		print('communities stored')
	except:
		print('Issue with community detection', sys.exc_info())
		sys.exit()
	


