import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor

class Linear_Regression:
	def __init__(self, X, y):
		self.X = X
		self.y = y

		self.model = LinearRegression().fit(self.X, self.y)

	def predcit(self, X_test):
		return self.model.predcit(x_test)
