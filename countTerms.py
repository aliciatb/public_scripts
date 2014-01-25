import sys

data_file_path = "../../data/"
# words to ignore
stop_words = ['a','about','above','across','after','afterwards','again','against','all','almost','alone','along','already','also','although','always','am','among','amongst','amoungst','amount','an','and','another','any','anyhow','anyone','anything','anyway','anywhere','are','around','as','at','back','be','became','because','become','becomes','becoming','been','before','beforehand','behind','being','below','beside','besides','between','beyond','bill','both','bottom','but','by','call','can','cannot','cant','co','computer','con','could','couldnt','cry','de','describe','detail','do','done','down','due','during','each','eg','eight','either','eleven','else','elsewhere','empty','enough','etc','even','ever','every','everyone','everything','everywhere','except','few','fifteen','fify','fill','find','fire','first','five','for','former','formerly','forty','found','four','from','front','full','further','get','give','go','had','has','hasnt','have','he','hence','her','here','hereafter','hereby','herein','hereupon','hers','him','his','how','however','hundred','i','ie','if','in','inc','indeed','interest','into','is','it','its','itse','keep','last','latter','latterly','least','less','ltd','made','many','may','me','meanwhile','might','mill','mine','more','moreover','most','mostly','move','much','must','my','myse','name','namely','neither','never','nevertheless','next','nine','no','nobody','none','noone','nor','not','nothing','now','nowhere','of','off','often','on','once','one','only','onto','or','other','others','otherwise','our','ours','ourselves','out','over','own','part','per','perhaps','please','put','rather','re','same','see','seem','seemed','seeming','seems','serious','several','she','should','show','side','since','sincere','six','sixty','so','some','somehow','someone','something','sometime','sometimes','somewhere','still','such','system','take','ten','than','that','the','their','them','themselves','then','thence','there','thereafter','thereby','therefore','therein','thereupon','these','they','thick','thin','third','this','those','though','three','through','throughout','thru','thus','to','together','too','top','toward','towards','twelve','twenty','two','un','under','until','up','upon','us','very','via','was','we','well','were','what','whatever','when','whence','whenever','where','whereafter','whereas','whereby','wherein','whereupon','wherever','whether','which','while','whither','who','whoever','whole','whom','whose','why','will','with','within','without','would','yet','you','your','yours','yourself','yourselves']

# Number of occurrences of a term to create word cloud 
def calcFrequency(file):
  doc = file.read()
  doc = doc.lower()
  
  # remove some punctuation
  doc = cleanPunctuation(doc)
  doc = cleanContractions(doc)
  
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
      exList.append(tweet)
  
    f = open(data_file_path + "output.txt", "w")
    for key in sorted(termFrequency.keys()):
      if key not in stop_words:
        f.write(key + "\t" + str(termFrequency[key]) + "\n")
        # print key, float(termFrequency[key])
    f.close()
      
def cleanPunctuation(doc):
  cleaned_doc = doc.replace("."," ")
  cleaned_doc = cleaned_doc.replace("."," ")
  cleaned_doc = cleaned_doc.replace(","," ")
  cleaned_doc = cleaned_doc.replace(";"," ")
  cleaned_doc = cleaned_doc.replace("-"," ")
  return cleaned_doc

def cleanContractions(doc):
  #todo: expand this
  cleaned_doc = doc.replace("\'"," ")
  return cleaned_doc

def main():
    # open the file as read-only
    termFile = open(data_file_path + sys.argv[1],'r')
    calcFrequency(termFile)
    termFile.close()

if __name__ == '__main__':
    main()