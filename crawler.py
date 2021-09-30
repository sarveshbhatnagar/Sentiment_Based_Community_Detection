import praw
import json
import os
from praw.models import MoreComments

class Crawler:
	def __init__(self, config):
		try:
			self.config = config
			if self.config['source'] == 'reddit':
				self.reddit = praw.Reddit(client_id=self.config['user'],
					 client_secret=self.config['key'],
					 user_agent='linux:CrawlerByMors:v0.1 (by u/MorsCertumEst)')
			else:
				raise Exception('unavailable source')
		except praw.exceptions.PRAWException as e:
			print(e)
			raise Exception()
	
	def crawl(self):
		if not os.path.exists(os.path.join(self.config['dataFolderPath'], self.config['subreddit'])):
			os.makedirs(os.path.join(self.config['dataFolderPath'], self.config['subreddit']))
		try:
			for submission in getattr(
					self.reddit.subreddit(self.config['subreddit']),self.config['order'])(
							limit=self.config['limit']):
				temp = {}
				
				try:
					temp['id'] = submission.id
					temp['title'] = submission.title
					temp['url'] = submission.url
					temp['subreddit'] = submission.subreddit.display_name
					temp['author'] = submission.author.name
					temp['text'] = submission.selftext
					temp['comments'] = []
				except:
					continue
				for i in submission.comments:
					if isinstance(i, MoreComments):
						continue
					if not i.author:
						continue
					#print('hr')
					temp2 = {}
					temp2['id'] = i.id
					temp2['author'] = i.author.name
					temp2['body'] = i.body
					temp['comments'].append(temp2)
					
				#print(json.dumps(temp, indent=4),'\n\n')
				#print(submission.subreddit)
				#print('asd')
				try:
					f = open(
						os.path.join(self.config['dataFolderPath'], self.config['subreddit'], submission.id+".json"),
						'w') 
					json.dump(temp, f)
					f.close()
				except OSError as e:
					print('OS error',e)
					raise Exception()
		except praw.exceptions.PRAWException as e:
			print('PRAW error',e)
			raise Exception()

"""
inp = open("config.json","r")
config = json.load(inp)
crawler = Crawler(config)
crawler.crawl()"""
