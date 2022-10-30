import requests

"""
this is specifically for testing the API.
"""



url = 'http://127.0.0.1:5000/'
text1 = input('Enter text1...')
text2 = input('Enter text2....')
params = {'text1': {text1}, 'text2': {text2}}
response = requests.get(url, params)
print(response.json())