def save_result(values):
	'''
		Param:
		------
			values (list) : result of testing dataset
	'''
	with open('result.csv', 'w') as f:
		# total samples
		n = len(values)
		for i in range(n):
			if not (isinstance(values[i], str) or isinstance(values[i], int) or \
							isinstance(values[i], float)):
				val_list = list(map(str, values[i]))
				val_str = ','.join(val_list) + '\n'
				f.write(val_str)

			else:
				if isinstance(values[i], str):
					f.write(values[i] + '\n')
				else:
					f.write(str(values[i]) + '\n')