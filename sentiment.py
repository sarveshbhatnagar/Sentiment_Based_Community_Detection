import json
import os
from textblob import TextBlob

import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from textblob import TextBlob
from joblib import load
import nltk
from nltk.stem import WordNetLemmatizer

class SVM_model:
	def __init__(self, config):
		self.config = config
		self.cv = load('cv1.joblib')
		self.final_model = load('model1.joblib')
		self.REPLACE_NO_SPACE = re.compile("[#$%<=>@.;:!\'?,\"()\[\]]")
		self.REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
		self.lemmatizer = WordNetLemmatizer()

	def cleanInput(self,r):
		r = re.compile('\\u2019').sub("'", r)
		r = self.REPLACE_NO_SPACE.sub("", r.lower())
		r = self.REPLACE_WITH_SPACE.sub(" ", r)
		r = ' '.join([self.lemmatizer.lemmatize(w) for w in r.split(' ')])
		return r

	def classify(self, t):
		return self.final_model.predict(self.cv.transform([self.cleanInput(t)]))[0]

class WE_model:
	def __init__(self, config):
		self.config = config
		self.w_e = {}
		for l in open('glove.6B.300d.txt','r'):
			temp = l.split()
			temp2 = [float(temp[i]) for i in range(1, len(temp))]
			self.w_e[temp[0]] = temp2
		self.REPLACE_NO_SPACE = re.compile("[#$%<=>@.;:!\'?,\"()\[\]]")
		self.REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
		self.final_model = load('model2.joblib')

	def SentToVec(self, s):
		tmp = s.split()
		total_v = [0.0 for j in range(300)]
		n_present = 0
		for j in tmp:
		  if j in self.w_e:
		    for k in range(300):
		      total_v[k] += self.w_e[j][k]
		    n_present+=1
		return [j/n_present for j in total_v]

	def cleanInput(self,r):
		r = re.compile('\\u2019').sub("'", r)
		r = self.REPLACE_NO_SPACE.sub("", r.lower())
		r = self.REPLACE_WITH_SPACE.sub(" ", r)
		return r

	def classify(self, t):
		return self.final_model.predict([self.SentToVec(self.cleanInput(t))])[0]
	

class Sentiment:
	def __init__(self, config):
		self.config = config
		self.REPLACE_NO_SPACE = re.compile("[#$%<=>@.;:!\'?,\"()\[\]]")
		self.REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
		if self.config['classifier'] == 'svm':
			self.svm_model = SVM_model(self.config)
		elif self.config['classifier'] == 'we':
			self.we_model = WE_model(self.config)

	def cleanInput(self,r):
		r = re.compile('\\u2019').sub("'", r)
		r = self.REPLACE_NO_SPACE.sub("", r.lower())
		r = self.REPLACE_WITH_SPACE.sub(" ", r)
		return r

	def classify(self):
		try:
			fileNames = os.listdir(os.path.join(self.config['dataFolderPath'], self.config['subreddit']))
			if not os.path.exists(os.path.join(self.config['classifiedFolderPath'], self.config['subreddit'])):
				os.makedirs(os.path.join(self.config['classifiedFolderPath'], self.config['subreddit']))
		except OSError as e:
			print(e)
			raise

		for fileName in fileNames:
			try:
				f1 = open(
				os.path.join(self.config['dataFolderPath'], self.config['subreddit'], fileName),
				'r')
				post = json.load(f1)
				try:
					text = TextBlob(self.cleanInput(post['text']))
					if self.config['classifier'] == 'default':
						post['text'] = [(i, text.sentiment) for i in text.noun_phrases]
						for i in range(len(post['comments'])):
							try:
								text2 = TextBlob(self.cleanInput(post['comments'][i]['body']))
								post['comments'][i]['body'] = [(i, text2.sentiment) for i in text2.noun_phrases]
							except:
								del post['comments'][i]
					elif self.config['classifier'] == 'svm':
						t = [2.0*self.svm_model.classify(post['text']) - 1.0, 0.0]
						post['text'] = [(i, t) for i in text.noun_phrases]
						for i in range(len(post['comments'])):
							try:
								text2 = TextBlob(self.cleanInput(post['comments'][i]['body']))
								t2 = [2.0*self.svm_model.classify(post['comments'][i]['body']) - 1.0, 0.0]
								post['comments'][i]['body'] = [(i, t2) for i in text2.noun_phrases]
							except:
								del post['comments'][i]
					elif self.config['classifier'] == 'we':
						t = [2.0*self.we_model.classify(post['text']) - 1.0, 0.0]
						post['text'] = [(i, t) for i in text.noun_phrases]
						for i in range(len(post['comments'])):
							try:
								text2 = TextBlob(self.cleanInput(post['comments'][i]['body']))
								t2 = [2.0*self.we_model.classify(post['comments'][i]['body']) - 1.0, 0.0]
								post['comments'][i]['body'] = [(i, t2) for i in text2.noun_phrases]
							except:
								del post['comments'][i]
				except:
					f1.close()
					continue
				try:
					f2 = open(
						os.path.join(self.config['classifiedFolderPath'], self.config['subreddit'], fileName),
						'w') 
					json.dump(post, f2)
					f2.close()
				except OSError as e:
					print(e)
					
				f1.close()
			except OSError as e:
				print(e)
				raise
"""
a = Sentiment(json.load(open("config.json","r")))
a.classify()"""

