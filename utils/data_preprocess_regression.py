import numpy as numpy
import pandas as pd
import csv
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def data_preprocess_regression(file_name, data_type = 'train', pca = None):
	'''
	Params:
	------
		file_name (str) : path to dataset file

	Returns:
	--------
		status (str) : fail or pass of data pre-processing
		logs (list) : running logs of data pre-processing
		data_dict (dict) : dictionary of data arrays 

	TODO: 
	-----	
		Ask user to select predict column.
		Pre-processing for date-time columns.
	'''
	file_type = file_name.split('.')[-1]

	logs = []
	status = 'pass'

	logs.append('Processing ' + data_type + 'dataset')
	# check whether dataset contains header or not
	try:
		has_header = csv.Sniffer().has_header(open(file_name).read(2048))
	except:
		logs.append('Be sure dataset file is not empty or with proper delimeters accordingly.')
		status = 'fail'
		return status, logs, None

	# read dataset file accordingly with and without header 
	df = None
	if file_type == 'csv':
		if has_header == False:
			df = pd.read_csv(file_name, sep = ",", header = None)
		else:
			df = pd.read_csv(file_name, sep = ",")

	elif file_name == 'txt':
		if has_header == False:
			df = pd.read_csv(file_name, sep = " ", header = None)
		else:
			df = pd.read_csv(file_name, sep = " ")

	if has_header == False:
		logs.appned('No header found or header type mismatch.')
		logs.append('Assigning headers implicitly.')
		df.columns = ['co_' + str(i+1) for i in range(len(df.iloc[0].values))]
		logs.append(f'columns = {df.columns.tolist()}')

	# check for dtype of last column
	if data_type == 'train' and  df.dtypes[-1] == 'O':
		logs.append('Make sure that last column of dataset is either int or float for regression.')
		logs.append('Try Classification model instead.')
		status = 'fail'
		return status, logs, None

	# check for null values and fill
	cols = df.columns
	cols_dtypes = df.dtypes
	is_null = df.isnull().any()
	null_cols = []
	for col in cols:
		if is_null[col] == True:
			null_cols.appned(col)
			if cols_dtypes[col] == 'float':
				df[col].fillna(df[col].mean(), inplace = True)
			else:
				df[col].fillna(df[col].mode()[0], inplace = True)
	if len(null_cols) > 0:
		logs.appned(f'Dataset has NULL values present at columns - {null_cols}')
		logs.append('For these columns NULL values are replaced with MODE of respective column.')

	# remove duplicate rows
	if data_type == 'train':
		logs.append('Removing duplicate rows if present.')
		df.drop_duplicates(inplace = True)

	# convert categorical values to one-hot encoding
	logs.append('Converting categorical columns into numeric.')
	df = pd.get_dummies(df, prefix_sep = '_', drop_first = True)
	if df.columns.shape[0] > 200:
		logs.append('Too many categorical columns or categorical values.')
		logs.append('Cannot proceed furthur.') 
		logs.append('Please re-check datasets to have non-categorical columns if possible.')
		status = 'fail'
		return status, logs, None
	else:
		logs.append(f'After converting columns are {df.columns.tolist()}')

	X, Y = None, None 
	# split dataframe into X and Y for training data
	if data_type == 'train':
		X = df.iloc[:, :-1].values
		Y = df.iloc[:, -1].values

	else:
		X = df.values

	X_train, X_eval, Y_train, Y_eval = None, None, None, None
	if data_type == 'train':
		# split dataset into test and train
		eval_size = 0.3
		# if datapoints less than 10000 make split ratio 8 : 2
		if X.shape[0] < 10000:
			eval_size = 0.2
		logs.append('Splitting dataset into train data and evaluation data.')
		logs.append(f'With ratio {(1 - eval_size) * 100}% : {eval_size * 100}% ')
		X_train, X_eval, Y_train, Y_eval = train_test_split(X, Y, test_size = eval_size, random_state = 42)

	# feature scaling
	logs.append('Standardizing data.')
	sc = StandardScaler()
	if X_train != None:
		X_train = sc.fit_transform(X_train)
		X_eval = sc.fit_transform(X_eval)
	else:
		X = sc.fit_transform(X)

	data_dict = dict()
	# applying PCA to reduce features
	logs.append('Applying PCA to reduce dimensions with variance 99%')
	if data_type == 'train':
		pca = PCA(.99)
		pca = pca.fit(X_train)
		X_train = pca.transform(X_train)
		X_eval = pca.transform(X_eval)
		data_dict['X_train'] = X_train
		data_dict['X_eval'] = X_eval
		data_dict['Y_train'] = Y_train
		data_dict['Y_eval'] = Y_eval
		data_dict['pca'] = pca

	else:
		X = pca.transform(X)
		data_dict['X'] = X

	return status, logs, data_dict