import sys
import time
import urllib2
from urllib2 import Request, urlopen, URLError, HTTPError
# http://docs.python.org/2/howto/urllib2.html

def getResponseTime(page):
  """ time from request to response.read """
  try:
    response = urllib2.urlopen(page)
    start = time.time()
    html = response.read()
    end = time.time()
    response.close
    return end - start
  except HTTPError as e:
    print e.code
    print e.read()
  except URLError as e:
    print e.reason
      
def main():
  page = sys.argv[1]
#   print page + ": " + str(getResponseTime(page))

if __name__ == '__main__':
  main()

