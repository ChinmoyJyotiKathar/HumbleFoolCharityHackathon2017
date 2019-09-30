import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score


def classify_topic(user_inp,count_vect,clf):
	topic_class = (clf.predict(count_vect.transform(user_inp)))
	return topic_class
