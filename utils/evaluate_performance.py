from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.metrics import classification_report
import math

import matplotlib.pyplot as plt
import base64
from io import BytesIO

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
	metrics_dict['MAE'] = mean_absolute_error(y_true, y_pred)
	metrics_dict['MSE'] = mean_squared_error(y_true, y_pred)
	metrics_dict['RMSE'] = math.sqrt(metrics_dict['MSE'])
	metrics_dict['R**2'] = r2_score(y_true, y_pred, multioutput = 'variance_weighted')
	metrics_dict['Adj. R**2'] = 1 - (1 - metrics_dict['R**2'])  * ((n - 1) / (n - p - 1))
	return metrics_dict

def classification_metrics(y_true, y_pred):
	'''
		Param:
		------
			y_true, y_pred(list) ; actual, predicted values

		Return:
		-------
			metrics_dict (dict) : metrics related to classification
	'''
	metrics_dict = dict()
	metrics_dict['report'] = classification_report(y_true, y_pred)
	y_true, y_pred = y_true.tolist(), y_pred
	labels = list(set(y_true).union(y_pred))
	label_index = dict()
	for i in range(len(labels)):
		label_index[labels[i]] = i
	conf_matrix = [[0 for _ in range(len(labels))] for _ in range(len(labels))]
	for i,j in zip(y_true, y_pred):
		true_ind, pred_ind = label_index[i], label_index[j]
		if i == j:
			conf_matrix[true_ind][pred_ind] += 1
		else:
			conf_matrix[true_ind][pred_ind] += 1
			conf_matrix[pred_ind][true_ind] += 1

	metrics_dict['labels'] = labels
	metrics_dict['confusion_matrix'] = conf_matrix
	return metrics_dict

def base64_regression_metrics(metrics):
	'''
		Param:
		------
			metrics (dict) : metrics related to regression

		Return:
		-------
			plot_data (base64) : base64 string format of evaluation metrics
	'''
	fig, ax = plt.subplots()

	cols = ['Metric', 'Value']
	rows = list(metrics.items())

	cell_colors = [["#5BC0DE", '#E1B16A']] * 5
	col_colors = ['#F35A4A', '#F35A4A']

	the_table = ax.table(cellText=rows, colWidths=[0.1, 0.2], cellColours = cell_colors, 
	                     colLoc = 'left', cellLoc = 'left', colColours = col_colors,
	                     colLabels=cols, loc = 'center', edges = 'closed')
	the_table.set_fontsize(16)
	the_table.scale(3, 3)

	ax.axis('tight')
	ax.axis('off')

	buf = BytesIO()
	fig.savefig(buf, format="png")
	plot_data = 'data:image/png;base64, ' +  base64.b64encode(buf.getbuffer()).decode("utf-8")
	return plot_data

def base64_classification_metrics(metrics):
		'''
		Param:
		------
			metrics (dict) : metrics related to classification

		Return:
		-------
			plot_data (base64) : base64 string format of evaluation metrics
	'''
	rep = metrics['report']
	rep = [i for i in rep.split('\n') if len(i) > 1 ]

	report = []
	for line in rep:
	    report.append(line.strip().replace(' ', ' ').split())
	    
	report[0].insert(0, 'class')
	report[-1][0] = report[-1][0] + '_' + report[-1][1]
	del report[-1][1]
	report[-2][0] = report[-2][0] + '_' + report[-2][1]
	del report[-2][1]
	report[-3] = [report[-3][0], ' ', ' ', report[-3][1], report[-3][2]]

	report.insert(-3, [''] * 5)

	fig,(ax) = plt.subplots(figsize=(5,6), ncols=1)

	cols = report[0]
	rows = report[1:]

	cell_colors = [['#5BC0DE', '#E1B16A', '#E1B16A', '#E1B16A', '#E1B16A']] * (len(report) - 1)
	col_colors = ['#F35A4A'] * 5

	the_table = ax.table(cellText=rows, colWidths=[0.1, 0.07, 0.07, 0.07, 0.07 ], cellColours = cell_colors, 
	                     colLoc = 'left', cellLoc = 'left', colColours = col_colors,
	                     colLabels=cols, loc = 'center', edges = 'closed')
	the_table.set_fontsize(16)
	the_table.scale(3, 3)

	ax.axis('tight')
	ax.axis('off')
	fig.tight_layout()


	buf = BytesIO()
	fig.savefig(buf, format="png")
	plot_data = 'data:image/png;base64, ' +  base64.b64encode(buf.getbuffer()).decode("utf-8")
	return plot_data

def base64_confusion_matrix(metrics):
		'''
		Param:
		------
			metrics (dict) : metrics related to regression

		Return:
		-------
			plot_data (base64) : base64 string format of confusion matrix
	'''
	labels = metrics['labels']
	confusion_matrix = metrics['confusion_matrix']

	fig, (ax) = plt.subplots(figsize = (6,6), ncols = 1)
	im = ax.imshow(confusion_matrix, cmap = 'magma_r')

	ax.set_xticks(range(len(labels)))
	ax.set_yticks(range(len(labels)))
	ax.set_xticklabels(labels)
	ax.set_yticklabels(labels)
	plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
	         rotation_mode="anchor")

	max_value, min_value = 99999, 0
	for i in range(len(labels)):
	    for j in range(len(labels)):
	        max_value = min(max_value, confusion_matrix[i][j])
	        min_value = max(min_value, confusion_matrix[i][j])
	        
	th = (max_value + min_value) / 2 
	for i in range(len(labels)):
	    for j in range(len(labels)):
	        text = ax.text(j, i, confusion_matrix[i][j],
	                       ha="center", va="center", color= 'w' if confusion_matrix[i][j] > th else 'k')

	ax.set_title("Confusion Matrix", fontsize = 20)
	plt.xlabel('Predicted Class', fontsize = 16)
	plt.ylabel('True Class', fontsize = 16)
	fig.tight_layout()

	buf = BytesIO()
	fig.savefig(buf, format="png")
	plot_data = 'data:image/png;base64, ' +  base64.b64encode(buf.getbuffer()).decode("utf-8")
	return plot_data