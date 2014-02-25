import pprint
import sys
import urllib
from datetime import datetime
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

def lookupAuthor(api_key, query):
  # returns an instance of an API service
  service = build('books', 'v1', developerKey=api_key)
  
  # encode the search terms
  q_terms = urllib.quote_plus(query)
  
  # build the request object with parameters
  request = service.volumes().list(source='public',
  q='inauthor:' + q_terms,
  orderBy='newest',
  maxResults='5',
  printType='books',
  projection='full')
  
  # make the api call to google books
  response = request.execute()

#  pprint.pprint(response)
#  print 'Found %d books:' % len(response['items'])
  titles = {}

  for book in response.get('items', []):
    if book['volumeInfo']['language'] == 'en':
      for a in book['volumeInfo']['authors']:
        # make sure it's correct author
        if a == urllib.unquote_plus(q_terms):
#         print 'Author: %s' % (urllib.quote_plus(a))
          publishedDate = book['volumeInfo']['publishedDate']
          publishedDate = datetime.strptime(publishedDate, '%Y-%m-%d')
          # check to see if date is in the future
          if publishedDate > datetime.today():
            titles[book['volumeInfo']['title']] = book['volumeInfo']['publishedDate']
#           print 'Title: %s, Date: %s, Lang: %s' % (book['volumeInfo']['title'],
#           book['volumeInfo']['publishedDate'],
#           book['volumeInfo']['language'])

  return titles
	
def addAuthorAlert(author, title, publishedDate):
  print 'Title: %s, By: %s, Publish Date: %s' % (title, author, publishedDate)	
	
def main():
	"""Get the author to check if there are any upcoming releases"""
	api_key = sys.argv[1]
	#sample = sampleCall(api_key)
	author = sys.argv[2]
	results = lookupAuthor(api_key, author)
	if len(results) > 0:
	  for key in results:
	    #print key, results[key]
	    addAuthorAlert(author, key, results[key])
	else:
	  print 'No upcoming books found for ' + author

if __name__ == '__main__':
	main()	