from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

def regression_metrics(y_true, y_pred, n, p):
	'''
		Param:
		------
			y_true, y_pred (list) ; actual and predicted values
			n (int) : no.of samples
			p (int) : no.of features

		Return:
		-------
			metrics_dict (dict) : metrics related to regression
	'''
	metrics_dict = dict()
	metrics_dict['mae'] = mean_absolute_error(y_true, y_pred)
	metrics_dict['mse'] = mean_squared_error(y_true, y_pred)
	metrics_dict['rmse'] = sqrt(metrics_dict['mse'])
	metrics_dict['r2'] = r2_score(y_true, y_pred, multioutput = 'variance_weighted')
	metrics_dict['adj_r2'] = 1 - (1 - metrics_dict['r2'])  * ((n - 1) / (n - p - 1))
	return metrics_dict

def classification_metrics(y_true, y_pred, y_prob):
	'''
		Param:
		------
			y_true, y_pred, y_prob (list) ; actual, predicted and probability values

		Return:
		-------
			metrics_dict (dict) : metrics related to classification
	'''
	metrics_dict = dict()
	metrics_dict['accuracy'] = accuracy_score(y_true, y_pred)
	metrics_dict['f1_score'] = f1_score(y_true, y_pred, average = None)
	metrics_dict['roc_auc_score'] = roc_auc_score(y_true, y_prob)
	return metrics_dict