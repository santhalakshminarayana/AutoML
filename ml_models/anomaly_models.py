import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.ensemble import IsolationForest

from scipy.stats import multivariate_normal

class Build_Anomaly_Model():
	def __init__(self, X, model_name, para, Y = None):
		self.X = X
		self.Y = Y

		self.model_name = model_name
		self.para = para

		if model_name == 'multivariate':
			self.classes, self.counts = np.unique(self.Y, return_counts = True)
			self.k = self.classes.size
			self.d = self.X.shape[1]
			self.mu = np.zeros((self.k, self.d))
			self.sigma = np.zeros((self.k, self.d, self.d))
			self.pi = np.zeros(self.k)
			self.threshold = self.para['threshold']

		if model_name == 'dbscan':
			self.model = DBSCAN(**self.para)

		if model_name == 'isolation':
			self.model = IsolationForest(**self.para)

		self.anomaly_model = None

	def fit(self):
		if self.model_name  == 'multivariate':
			for label in range(0, self.k):
				indices = (self.Y == label)
				self.mu[label] = np.mean(self.X[indices, :], axis = 0)
				self.sigma[label] = np.cov(self.X[indices, :], rowvar = 0, bias = 0)
				self.pi[label] = self.counts[label] / (len(self.Y))
		else:
			self.anomaly_model =  self.model.fit(self.X)

	def predict(self, X):
		if self.model_name == 'multivariate':
			all_prob = np.zeros((len(X), self.k))
			for label in range(0, self.k):
				rv = multivariate_normal(mean = self.mu[label], cov = self.sigma[label], 
													allow_singular = True)
				for i in range(0, len(X)):
					all_prob[:, label] = rv.logpdf(X[:, :]) + np.log(self.pi[label])
			pred_label = np.max(all_prob, axis = 1) * -1
			pred_class = np.argmax(all_prob, axis = 1)
			pred_label[pred_label < self.threshold] = -1
			return np.squeeze(pred_label).tolist()

		else:	
			return self.anomaly_model.predict(X)