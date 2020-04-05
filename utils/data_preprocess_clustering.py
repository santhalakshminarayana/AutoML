import pandas as pd
import csv

from utils.update_logs import update_pass, update_fail

def data_preprocess_clustering(file_name):
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

	logs.append('Processing dataset.')
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

	# check for dtype of each column
	for col_dtype in df.dtypes:
		if col_dtype == 'O':
			logs.append('Make sure that each column of dataset is either int or float for clustering / anomaly detection.')
			logs.append('It is better if data_type is int.')
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
			df[col].fillna(df[col].mean(), inplace = True)

	if len(null_cols) > 0:
		logs.append(f'Dataset has NULL values present at columns - {null_cols}.')
		logs.append('For these columns NULL values are replaced with MEAN of respective column.')

	# remove duplicate rows
	logs.append('Removing duplicate rows if present.')
	df.drop_duplicates(inplace = True)

	# get values of dataframe
	data_dict = dict()
	data_dict['X'] = df.values
	status = 'pass'

	return status, logs, data_dict

def clustering_dataset(dataset_files):
	# pre-processing data files
	train_status, train_logs, train_data_dict = data_preprocess_clustering(dataset_files['train_file'])
	if train_status == 'pass':
		update_pass('Train', train_logs)
		return train_data_dict
	else:
		update_fail('Train', train_logs)
		return None