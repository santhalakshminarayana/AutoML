import pandas as pd
import csv

import category_encoders as ce

from sklearn.preprocessing import StandardScaler

from utils.update_logs import update_pass, update_fail

def data_preprocess(file_name, data_type = 'train', encoder = None):
	'''
	Params:
	------
		file_name (str) : path to dataset file
		data_type : train or test
		encoder : category_encoder used in training phase

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

	# get values into X
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

	# feature scaling
	logs.append('Standardizing data.')
	sc = StandardScaler()
	X = sc.fit_transform(X)

	data_dict['X'] = X

	status = 'pass'
	return status, logs, data_dict

def dimension_dataset(dataset_files):
	# pre-processing data files
	train_status, train_logs, train_data_dict = data_preprocess(dataset_files['train_file'], 
										data_type = 'train', encoder = None)
	if train_status == 'pass':
		update_pass('Train', train_logs)
		return train_data_dict
	else:
		update_fail('Train', train_logs)
		return None