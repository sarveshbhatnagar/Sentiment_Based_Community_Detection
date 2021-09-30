import json
import os
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LinearSvm
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from textblob import TextBlob


