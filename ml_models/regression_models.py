from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor

class Build_Regression_Model():
	def __init__(self, X, Y, model_name, para):
		self.X = X
		self.Y = Y

		self.base_model = None

		if model_name == 'regression_nearest':
			self.base_model = KNeighborsRegressor()

		if model_name == 'linear':
			self.base_model = LinearRegression()

		if model_name == 'svr':
			self.base_model = SVR()

		if model_name == 'regression_random':
			self.base_model = RandomForestRegressor()

		self.para = para

		self.model = None
		if self.para != None:
			self.model = GridSearchCV(self.base_model, para)
		else:
			self.model = self.base_model

	def fit(self):
		self.model.fit(self.X, self.Y)

	def predict(self, X):
		return self.model.predict(X)

	def best_params(self):
		if self.para == None:
			return None
		return self.model.best_params_

	def best_estimator(self):
		if self.para == None:
			return None
		return self.model.best_estimator_