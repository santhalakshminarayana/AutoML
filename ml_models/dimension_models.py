from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.manifold import TSNE

class Build_Dimension_Model():
	def __init__(self, X, model_name, para):
		self.X = X

		self.base_model = None
		self.para = para

		if model_name == 'pca':
			self.base_model = PCA(**self.para)

		if model_name == 'tsne':
			self.base_model = TSNE(**self.para)

		if model_name == 'svd':
			self.base_model = TruncatedSVD(**self.para)

		self.model = None

	def fit(self):
		self.model =  self.base_model.fit(self.X)

	def predict(self, X):
		try:
			return self.model.transform(X)
		except:
			return self.model.fit_transform(X)

	def explained_variance_ratio(self):
		try:
			return self.model.explained_variance_ratio_
		except:
			return None

	def kl_divergence(self):
		try:
			return self.model.kl_divergence_
		except:
			None