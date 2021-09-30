import json
import os

class Associate:
	def __init__(self, config):
		self.config = config	

	def associate(self):
		try:
			fileNames = os.listdir(os.path.join(self.config['classifiedFolderPath'], self.config['subreddit']))
			if not os.path.exists(os.path.join(self.config['associatedFolderPath'], self.config['subreddit'])):
				os.makedirs(os.path.join(self.config['associatedFolderPath'], self.config['subreddit']))
		except OSError as e:
			print(e)
			raise

		temp = {}
		
		for fileName in fileNames:
			try:
				f1 = open(
						os.path.join(self.config['classifiedFolderPath'], self.config['subreddit'], fileName),
						'r') 
				post = json.load(f1)

				for comment in post['comments']:
					#print(comment['body'])
					if comment['body'] and abs(comment['body'][0][1][0])>=0.2:
						if (comment['author'],post['author']) in temp:
							temp[(comment['author'],post['author'])] += comment['body'][0][1][0]
						else:
							temp[(comment['author'],post['author'])] = comment['body'][0][1][0]
				f1.close()
			except OSError as e:
				print(e)
				continue

		temp2 = sorted(temp.items(), key = lambda item: item[1])

		percentiles = [5.0, 10.0, 20.0, 50.0]
		for percentile in percentiles:
			final = {}
			final[str(temp2[len(temp2)-1][0])] = 1
			for i in range(len(temp2)-2,-1,-1):
				if temp2[i][1]==temp2[i+1][1] or i/len(temp) >= percentile/100:
					final[str(temp2[i][0])] = 1
					continue	
				break
			try:
				f2 = open(
					os.path.join(self.config['associatedFolderPath'], self.config['subreddit'], 'res'+str(percentile)),
					'w') 
				json.dump(final, f2)
				f2.close()
			except OSError as e:
				print(e)
				raise
		f1.close()
		
