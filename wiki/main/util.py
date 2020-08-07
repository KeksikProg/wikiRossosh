from datetime import datetime
from os.path import splitext

def get_timestamp_path(instance, filename):
	'''делает название для фотография (делаютя с помощью текущего времени и первоначального названия фотографии'''
	return f'{datetime.now().timestamp()}{splitext(filename)[1]}'