import requests, json
import os
import pandas as pd


def parseWithGeoparser(text, print_output=False, print_input=False, flatten=True):
	""" Makes request to Geoparser and returns a list of features

	See https://geoparser.io/docs.html for how to parse features

	Input
		text 			String. Do not pass lists, dictionaries, etc. Basic strings only.
		print_output	print the json that is returned by geoparser.io

	Returns
		Pandas dataframe with each extracted feature
	"""

	url = 'https://geoparser.io/api/geoparser'
	headers = {'Authorization': 'apiKey %s' % _get_api_key()}
	data = {'inputText': text}
	response = requests.post(url, headers=headers, data=data)

	if print_input:
		print(text)
	if print_output:
		print(json.dumps(response.json(), indent=4))

	if response.status_code != 200:
		raise ConnectionError('Did not get successful reply from Geoparser. Status code %d' % response.status_code)

	if flatten:
		df = _flatten_into_df(response.json()["features"])
	else:
		df = pd.DataFrame(response.json()["features"])
	return df


def _get_api_key():
	key = os.environ.get('geoparserIO_key')
	if not key:
		raise PermissionError('No Geoparser IO key found. Request one on www.geoparser.io and set as environment variable.')
	return(key)


def _flatten_into_df(data_to_flatten):
    """ Takes data in list or dict format.

    Input
        data_to_flatten        a dictionary or list containing the data to end up in the dataframe. 
    """
    
    # check if data is a dictionary - if it is, make it into a list
    if isinstance(data_to_flatten, dict):
        data_to_flatten = [data_to_flatten]

    for idx, item in enumerate(data_to_flatten):
        df_element = pd.io.json.json_normalize(item)
        if idx == 0:
            df_temp = df_element
        else:
            df_temp = df_temp.append(df_element)

    return df_temp