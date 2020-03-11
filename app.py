import eel
import utils
from utils.check_file import is_file_valid
from utils.data_preprocess_regression import data_preprocess_regression

eel.init('web')

@eel.expose
def check_file_exists(file_name):
	return is_file_valid(file_name)

@eel.expose
def get_parameters(model_type, model_name, dataset_files,
				   para = None):
	'''
	Param:
	------
		model_type (str) : ML model classification

		model_name (str) : ML model name

		dataset_files (dict) : path to train and test dataset files

		para (dict) : parameters for model
					  keys and values are type str where
					  values may separate by ','
	'''

	if model_type == 'regression':
		# pre-processing data files
		train_status, train_logs, train_data_dict = data_preprocess_regression(dataset_files['train_file'])
		train_logs = '\n'.join(train_logs)
		test_status, test_logs, test_data_dict = None, None, None
		if train_status == 'pass':
			eel.update_pass_logs(train_logs)
			test_status, test_logs, test_data_dict = data_preprocess_regression(dataset_files['test_file'], 
																				'test', train_data_dict['pca'])
			test_logs = '\n'.join(test_logs)
		else:
			print(train_logs)
			eel.update_fail_logs('Train', train_logs)

		if test_status == 'pass':
			eel.update_pass_logs(test_logs)

		else:
			eel.update_fail_logs('Test', test_logs)

		# apply model on data files	
		if model_name == 'regression_nearest':
			pass

		if model_name == 'linear':
			pass

		if model_name == 'svr':
			pass

		if model_name == 'regression_random':
			pass

	if model_type == 'classification':
		pass

	if model_type == 'anomaly':
		pass

	if model_type == 'dimension':
		pass

eel.start('index.html', size = (600, 500))