import re
import string
import sys

def filterURLs(domain,fileName):
  urls = []
#   print 'fileName=', fileName
  file = open(fileName)
  try:
    doc = file.read()
    hyperlinks = doc.split()
    for l in hyperlinks:
      # exclude duplicate links
      if l not in urls:
        if l.find('http://') == 0 or l.find('https://') == 0:
          # exclude links to external sites
          if domain in l:
            urls.append(l)

  except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror) 

  # sort list and append to new file
  file.close()
  return sorted(urls)

def main(file):
  DistinctURLs = filterURLs(file)
  for u in DistinctURLs:
    print u
  
if __name__ == '__main__':
  main(sys.argv[1])