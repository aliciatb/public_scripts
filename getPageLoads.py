import datetime
from datetime import datetime
import string
import sys
# custom modules
import crawl
import pageLoad
import scrubURLs

def getDomain(url):
  """ to get filename of results """
  domain = string.replace(url,"https://www.","")
  domain = string.replace(domain,"http://www.","")
  domain = string.replace(domain,"http://","")
  domain = string.replace(domain,".com/","")
  domain = string.replace(domain,".com","")
  return domain
  
def validURL(url):
  """ todo: expand validation rules """
  validated = ''
  if 'http://www.' in url or 'https://www.' in url:
    validated = url

  return validated
  
def createPageTimeFile(pages,domain):
  """ generates URL, response in seconds, and datetime of the request to file """
  filename = domain+'_pageLoads.csv'
  textfile = file(filename,'wt')
  
  for p in pages:
    try:
      timeofrequest = datetime.today()
      load_time = str(pageLoad.getResponseTime(p))
      results = p + ',' + load_time + ',' + str(timeofrequest)
      print results
      textfile.write(results+'\n')
    except NameError:
      print 'error with URL, ' + p
  
  textfile.close()
  return filename

def main():
  url = sys.argv[1]
  url = validURL(url)
  print 'url=', url
  domain = getDomain(url)
  print 'domain=', domain
  filename = crawl.basicCrawler(url, domain)
  pages = scrubURLs.filterURLs(domain,filename)
  file = createPageTimeFile(pages,domain)
  print 'File, ' + file + ' is done!' 

if __name__ == '__main__':
  main()