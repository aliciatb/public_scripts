import pprint
import sys
import urllib
from apiclient.discovery import build

def sampleCall(api_key):
	""" Sample code kindly provided by google, https://developers.google.com/api-client-library/python/samples/simple_api_cmd_line_books.py """
	# The apiclient.discovery.build() function returns an instance of an API service
	# object that can be used to make API calls. The object is constructed with
	# methods specific to the books API. The arguments provided are:
	#   name of the API ('books')
	#   version of the API you are using ('v1')
	#   API key
	service = build('books', 'v1', developerKey=api_key)

	# The books API has a volumes().list() method that is used to list books
	# given search criteria. Arguments provided are:
	#   volumes source ('public')
	#   search query ('android')
	# The method returns an apiclient.http.HttpRequest object that encapsulates
	# all information needed to make the request, but it does not call the API.
	request = service.volumes().list(source='public', q='amazon')

	# The execute() function on the HttpRequest object actually calls the API.
	# It returns a Python object built from the JSON response. You can print this
	# object or refer to the Books API documentation to determine its structure.
	response = request.execute()
	pprint.pprint(response)

	# Accessing the response like a dict object with an 'items' key returns a list
	# of item objects (books). The item object is a dict object with a 'volumeInfo'
	# key. The volumeInfo object is a dict with keys 'title' and 'authors'.
	print 'Found %d books:' % len(response['items'])
	for book in response.get('items', []):
	  print 'Title: %s, Authors: %s' % (
		book['volumeInfo']['title'],
		book['volumeInfo']['authors'])

def lookupAuthor(author, api_key):
	author_terms = urllib.quote_plus(author)
	print author_terms
	service = build('books', 'v1', developerKey=api_key)
	# book['volumeInfo']['publishedDate']
	

def main():
	"""Get the author to check if there are any upcoming releases"""
	api_key = sys.argv[1]
	sample = sampleCall(api_key)
	# author = sys.argv[2]
	# results = lookupAuthor(author, api_key)

if __name__ == '__main__':
	main()	