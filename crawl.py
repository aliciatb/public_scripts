import re, sys, urllib, string
# http://docs.python.org/2/library/re.html

def basicCrawler(url, domain):
  """ 03042014 - code provided by http://null-byte.wonderhowto.com/inspiration/basic-website-crawler-python-12-lines-code-0132785/ """
  """ 03052014 - added i/o error handling and passing url as parameter """
  print 'domain=', domain
  filename = domain+'.txt'
  print 'filename', filename
  textfile = file(filename,'wt')
  pageContents = ""
  try:
    pageContents = urllib.urlopen(url).read()
    for i in re.findall('''href=["'](.[^"']+)["']''', pageContents, re.I):
      print i
      linkPageContents = ""
      try:
        linkPageContents = urllib.urlopen(i).read()
        for ee in re.findall('''href=["'](.[^"']+)["']''', linkPageContents, re.I):
          print ee
          textfile.write(ee+'\n')
      except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)        
  except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
      
  textfile.close()
  return filename

def main():
  basicCrawler(sys.argv[1])

if __name__ == '__main__':
  main()