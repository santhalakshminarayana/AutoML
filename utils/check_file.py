import os

allowed_ext = ['csv', 'txt']
def is_file_valid(file_name):
	if os.path.isfile(file_name):
		head, tail = os.path.split(file_name)
		ext = tail.split('.')[-1]
		if ext not in allowed_ext:
			return f'*Provide only {allowed_ext} files'
	else:
		return '*Please enter valid file name'

	return 'exist'