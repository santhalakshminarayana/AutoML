from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

class Build_Classification_Model():
	def __init__(self, X, Y, model_name, para):
		self.X = X
		self.Y = Y

		self.base_model = None

		if model_name == 'classification_nearest':
			self.base_model = KNeighborsClassifier()

		if model_name == 'logistic':
			self.base_model = LogisticRegression()

		if model_name == 'svm':
			self.base_model = SVC()

		if model_name == 'classification_random':
			self.base_model = RandomForestClassifier()

		self.para = para

		self.model = None
		if self.para != None:
			self.model = GridSearchCV(self.base_model, para)
		else:
			self.modle = self.base_model

	def fit(self):
		self.model.fit(self.X, self.Y)

	def predict(self, X):
		return self.model.predict(X)

	def predict_proba(self, X):
		return self.model.predict_proba(X)

	def best_params(self):
		if self.para == None:
			return None
		return self.model.best_params_

	def best_estimator(self):
		if self.para == None:
			return None
		return self.model.best_estimator_