from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN

class Build_Clustering_Model():
	def __init__(self, X, model_name, para):
		self.X = X
		self.para = para

		if model_name == 'kmeans':
			self.model = KMeans(**self.para)

		if model_name == 'agglomerative':
			self.model = AgglomerativeClustering(**self.para)

		if model_name == 'dbscan':
			self.model = DBSCAN(**self.para)

		self.clustered_model = None

	def fit(self):
		self.clustered_model =  self.model.fit(self.X)

	def predict(self, X):
		return self.clustered_model.predict(X)