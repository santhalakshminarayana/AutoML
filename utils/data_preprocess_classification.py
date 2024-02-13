import pandas as pd
import csv

import category_encoders as ce

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from utils.update_logs import update_pass, update_fail

def data_preprocess_classifiation(file_name, data_type = 'train', encoder = None, pca = None):
	'''
	Params:
	------
		file_name (str) : path to dataset file
		encoder : category_encoder used to convert categorical values to numeric in training
		pca : pca used in training phase

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

	logs.append('Processing ' + data_type + ' dataset.')
	# check whether dataset contains header or not
	has_header = False
	try:
		has_header = csv.Sniffer().has_header(open(file_name).read(2048))

	except:
		logs.append('Be sure dataset file is not empty or with proper delimeters accordingly.')
		status = 'fail'
		return status, logs, None

	# read dataset file accordingly with and without header 
	df = None
	if file_type == 'csv':
		try:
			if has_header == False:
				df = pd.read_csv(file_name, sep = ",", header = None)
			else:
				df = pd.read_csv(file_name, sep = ",")
		except:
			logs.append('Error while checking dataset file. May due to delimeter, inconsistent format ...')
			status = 'fail'
			return status, logs, None

	elif file_type == 'txt':
		try:
			if has_header == False:
				df = pd.read_csv(file_name, sep = " ", header = None)
			else:
				df = pd.read_csv(file_name, sep = " ")
		except:
			logs.append('Error while checking dataset file. May due to delimeter, inconsistent format ...')
			status = 'fail'
			return status, logs, None

	if has_header == False:
		logs.append('No header found or header type mismatch.')
		logs.append('Assigning headers implicitly.')
		df.columns = ['co_' + str(i+1) for i in range(len(df.iloc[0].values))]
		logs.append(f'columns = {df.columns.tolist()}')

	# check for dtype of last column
	if data_type == 'train' and  df.dtypes[-1] == 'float':
		logs.append('Make sure that last column of dataset is not int nor float for classifaction.')
		logs.append('Try Regression model instead.')
		status = 'fail'
		return status, logs, None

	# check for null values and fill
	cols = df.columns
	cols_dtypes = df.dtypes
	is_null = df.isnull().any()
	null_cols = []
	for col in cols:
		if is_null[col] == True:
			null_cols.append(col)
			if cols_dtypes[col] == 'float':
				df[col].fillna(df[col].mean(), inplace = True)
			else:
				df[col].fillna(df[col].mode()[0], inplace = True)
	if len(null_cols) > 0:
		logs.append(f'Dataset has NULL values present at columns - {null_cols}.')
		logs.append('For these columns NULL values are replaced with MEAN or MODE of respective column.')

	# remove duplicate rows
	if data_type == 'train':
		logs.append('Removing duplicate rows if present.')
		df.drop_duplicates(inplace = True)

	# split dataframe into X and Y for training data
	X, Y = None, None 
	if data_type == 'train':
		X = df.iloc[:, :-1].values
		Y = df.iloc[:, -1].values

	else:
		X = df.values

	data_dict = dict()
	# convert categorical values to numeric applying backward-difference-encoding
	logs.append('Converting categorical columns into numeric by applying BackwardDifferenceEncoder.')
	if data_type == 'train':
		encoder = ce.BackwardDifferenceEncoder()
		_ = encoder.fit(X)
		data_dict['encoder'] = encoder
		X = encoder.transform(X)
	else:
		X = encoder.transform(X)

	X_train, X_eval, Y_train, Y_eval = None, None, None, None
	if data_type == 'train':
		# split dataset into test and train
		eval_size = 0.3
		# if datapoints less than 10000 make split ratio 8 : 2
		if X.shape[0] < 10000:
			eval_size = 0.2
		logs.append('Splitting dataset into train data and evaluation data ')
		logs.append(f'with ratio {(1 - eval_size) * 100}% : {eval_size * 100}% ')
		X_train, X_eval, Y_train, Y_eval = train_test_split(X, Y, test_size = eval_size, random_state = 42)

	# feature scaling
	logs.append('Standardizing data.')
	sc = StandardScaler()
	if data_type == 'train':
		X_train = sc.fit_transform(X_train)
		X_eval = sc.fit_transform(X_eval)
	else:
		X = sc.fit_transform(X)

	# applying PCA to reduce features
	logs.append('Applying PCA to reduce dimensions with variance 99%.')
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
		try:
			X = pca.transform(X)
			data_dict['X'] = X
		except:
			status = 'fail'

	return status, logs, data_dict

def classification_dataset(dataset_files):
	# pre-processing data files
	train_status, train_logs, train_data_dict = data_preprocess_classifiation(dataset_files['train_file'])
	test_status, test_logs, test_data_dict = 'fail', None, None
	if train_status == 'pass':
		update_pass('Train', train_logs)
		test_status, test_logs, test_data_dict = data_preprocess_classifiation(dataset_files['test_file'], 
												'test', train_data_dict['encoder'], train_data_dict['pca'])
	else:
		update_fail('Train', train_logs)
		return None

	if test_status == 'pass':
		update_pass('Test', test_logs)
		del train_data_dict['pca']
		return [train_data_dict, test_data_dict]
	else:
		update_fail('Test', test_logs)
		return None