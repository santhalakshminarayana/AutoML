def process_parameters(para, model_type):
	'''
	para (dict) : parameters for model
					  keys and values are type str where
					  values may separate by ','
	'''

	single_parameter_models = ['clustering', 'anomaly', 'dimension']
	new_para = dict()
	for parameter in para.keys():
		values = []
		if model_type in single_parameter_models:
			values.append(para[parameter])
		else:
			values = para[parameter].split(',')
		
		new_values = []
		for i in range(len(values)):
			if 'None' in values[i]:
				new_values.append(None)
				continue
			if 'True' in values[i]:
				new_values.append(True)
				continue
			if 'False' in values[i]:
				new_values.append(False)
				continue
			try:
				new_values.append(int(values[i]))
			except:
				try:
					new_values.append(float(values[i]))
				except:
					new_values.append(values[i])

		if model_type in single_parameter_models:
			new_values = new_values[0]
	
		new_para[parameter] = new_values

	return new_para