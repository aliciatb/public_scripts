import sys
import re
import collections

data_file_path = "~/data/"

# words to ignore (source = http://norm.al/2009/04/14/list-of-english-stop-words/)
stop_words = ['a','about','above','across','after','afterwards','again','against','all','almost','alone','along',
              'already','also','although','always','am','among','amongst','amoungst','amount','an','and','another',
              'any','anyhow','anyone','anything','anyway','anywhere','are','around','as','at','back','be','became',
              'because','become','becomes','becoming','been','before','beforehand','behind','being','below','beside',
              'besides','between','beyond','bill','both','bottom','but','by','call','can','cannot','cant','co','computer',
              'con','could','couldnt','cry','de','describe','detail','do','done','down','due','during','each','eg','eight',
              'either','eleven','else','elsewhere','empty','enough','etc','even','ever','every','everyone','everything',
              'everywhere','except','few','fifteen','fify','fill','find','fire','first','five','for','former','formerly',
              'forty','found','four','from','front','full','further','get','give','go','had','has','hasnt','have','he',
              'hence','her','here','hereafter','hereby','herein','hereupon','hers','him','his','how','however','http','hundred',
              'i','ie','if','in','inc','indeed','interest','into','is','it','its','itse','keep','last','latter','latterly',
              'least','less','ltd','made','many','may','me','meanwhile','might','mill','mine','more','moreover','most',
              'mostly','move','much','must','my','myse','name','namely','neither','never','nevertheless','next','nine','no',
              'nobody','none','noone','nor','not','nothing','now','nowhere','of','off','often','on','once','one','only','onto',
              'or','other','others','otherwise','our','ours','ourselves','out','over','own','part','per','perhaps','please',
              'put','rather','re','s','same','see','seem','seemed','seeming','seems','serious','several','she','should','show',
              'side','since','sincere','six','sixty','so','some','somehow','someone','something','sometime','sometimes',
              'somewhere','still','such','system','take','ten','than','that','the','their','them','themselves','then','thence',
              'there','thereafter','thereby','therefore','therein','thereupon','these','they','thick','thin','third','this',
              'those','though','three','through','throughout','thru','thus','to','together','too','top','toward','towards',
              'twelve','twenty','two','un','under','until','up','upon','us','very','via','was','we','well','were','what',
              'whatever','when','whence','whenever','where','whereafter','whereas','whereby','wherein','whereupon','wherever',
              'whether','which','while','whither','who','whoever','whole','whom','whose','why','will','with','within','without',
              'would','yet','you','your','yours','yourself','yourselves','nursery','5']

# retain the full name since they are meaningful
fullNames = ['Wells Fargo','H.D. Vest Financial Services','H.D. Vest','Home Depot','Calloway\'s Nursery','Nelson Capital','First Clearing Services','Parthenon Capital',
            'Single Sign-On','multi-factor','Finra ADV form 2 Part B',
            'Texas A&M University','Texas Christian University','University of Washington','Johns Hopkins University','Princeton University','Bachelor of Arts',
            'Masters of Business Administration','12th man','Data Science','Data Scientist',
            'Team Foundation Server','Visual Basic','Visual SourceSafe','Visual Studio','Classic ASP',
            'Test Driven Development','Pair Programming','Continuous improvement agent','2 week sprints','Certified Scrum Master',
            'Amazon Instant Video','Kindle Fire','streaming video','google books api','Tableau Public',
            'Little Free Library','Business Intelligence','R Studio'
            ]

def calcFrequency(file):
  """
  calculate number of occurrences of a term to create word cloud
  """
  doc = file.read()
  doc = doc.lower()
  addMoreStopWords(['alicia','alicia3694#','aliciabrown','aliciatb','aliciatb@gmail.com','msaliciabrown','brown','dallas','fall','summer','tx','#8702','lfl8702'])
  doc = keepLongNamesIntact(doc,fullNames)
  doc = scrub(doc)
  
  totalTerms = 0
  termFrequency = {}
  
  terms = doc.split()
  for t in terms:
    try:
      totalTerms += 1
      if t in termFrequency: 
        termFrequency[t] += 1
      else:
        termFrequency[t] = 1
    except:
      exList.append(t)
  
    # sort by count desc
    ordered = []
    ordered = collections.OrderedDict(sorted(termFrequency.items(), key=lambda t: t[1]))
    for key in reversed(ordered.keys()):
      print key, ': ', ordered[key]
 
    f = open(data_file_path + "output.txt", "w")
    for key in sorted(termFrequency.keys()):
#    for key in reversed(ordered.keys()):
      if key not in stop_words:
        # revert fullNames while writing to file
        if key == 'calloway':
          # hack because reg ex is not handling single quote
          f.write('calloway\'s nursery' + "\t" + str(termFrequency[key]) + "\n")
        else:
          f.write(key.replace("~"," ") + "\t" + str(termFrequency[key]) + "\n")
      # print key, float(termFrequency[key])
    f.close()
      
def scrub(doc):
  """
  remove non-words like date ranges, punctuation, asterisks
  todo: retain single quote in Calloway's Nursery properly (regex)
  """
  cleaned_doc = doc
  
  # date ranges, dates, phone, e-mail
  cleaned_doc = re.sub(r'\s\d\d\d\d+-\d\d\d\d','',cleaned_doc)        #date range of 4 digit years with space
  cleaned_doc = re.sub(r'\s-\s\d\d\d\d+-\d\d\d\d','',cleaned_doc)     #date range of 4 digit years
  cleaned_doc = re.sub(r'\d\d\d+-\d\d\d+-\d\d\d\d','',cleaned_doc)    #set of 3 numbers & dash (phone)
  cleaned_doc = re.sub(r'\s\d\d\d\d','',cleaned_doc)                  #4 digit year preceded by space
  cleaned_doc = re.sub(r'\(\d\d\d\d','',cleaned_doc)                  #4 digit year preceded by escaped parenthesis
  cleaned_doc = re.sub(r'\d\d\d\d\)','',cleaned_doc)                  #4 digit year followed by escaped parenthesis
  cleaned_doc =  re.sub(r'\.\s',' ',cleaned_doc)                      #period at end of sentence
  cleaned_doc =  re.sub(r'\s\&\s',' ',cleaned_doc)                    #& (and with spaces on either side)
  cleaned_doc =  re.sub(r'/',' ',cleaned_doc)                    	    #/
  cleaned_doc =  re.sub(r'\s\-\s',' ',cleaned_doc)                    #-
  cleaned_doc =  re.sub(r'[^a-zA-Z0-9\-\&\#\~\.\']',' ', cleaned_doc)   #most punctuation

  return cleaned_doc

def addMoreStopWords(words):
  """
  add resume-specific words so they are not counted, like name, places
  """
  for w in words:
    stop_words.append(w)

def keepLongNamesIntact(doc,names):
  """
  maintain all words for multi-word names, tools, schools
  """
  replacedDoc = doc
  for n in names:
    n = n.lower()
    new_name = n.replace(" ","~")
#     print new_name
    replacedDoc = replacedDoc.replace(n,new_name)
  return replacedDoc

def openFile(name):
  """
  open the document as read-only
  """
  file = open(data_file_path + name,'r')
  return file

def main():
  """
  countTerms opens text file, counts words after removing some punctuation and stop words,
  writes term and frequency to output.txt to ~/data folder
  """
  termFile = openFile(sys.argv[1])
  calcFrequency(termFile)
  termFile.close()

if __name__ == '__main__':
    main()