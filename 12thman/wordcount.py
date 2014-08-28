import MapReduce
import re
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
cd ~/public_scripts/12thman
python wordcount.py output/other_tweets.txt
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line
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
              'hence','her','here','hereafter','hereby','herein','hereupon','hers','him','his','how','however','hundred',
              'i','ie','if','in','inc','indeed','interest','into','is','it','its','itse','keep','last','latter','latterly',
              'least','less','ltd','made','many','may','me','meanwhile','might','mill','mine','more','moreover','most',
              'mostly','move','much','must','my','myse','name','namely','neither','never','nevertheless','next','nine','no',
              'nobody','none','noone','nor','not','nothing','now','nowhere','of','off','often','on','once','one','only','onto',
              'or','other','others','otherwise','our','ours','ourselves','out','over','own','part','per','perhaps','please',
              'put','rather','re','rt','s','same','see','seem','seemed','seeming','seems','serious','several','she','should','show',
              'side','since','sincere','six','sixty','so','some','somehow','someone','something','sometime','sometimes',
              'somewhere','still','such','system','take','ten','than','that','the','their','them','themselves','then','thence',
              'there','thereafter','thereby','therefore','therein','thereupon','these','they','thick','thin','third','this',
              'those','though','three','through','throughout','thru','thus','to','together','too','top','toward','towards',
              'twelve','twenty','two','un','under','until','up','upon','us','very','via','was','we','well','were','what',
              'whatever','when','whence','whenever','where','whereafter','whereas','whereby','wherein','whereupon','wherever',
              'whether','which','while','whither','who','whoever','whole','whom','whose','why','will','with','within','without',
              'would','yet','you','your','yours','yourself','yourselves','nursery','&']


def mapper(record):
    """
    maps all data tied to a key
    """
    # key: team identifier
    # value: tweet contents
    key = "other.txt"
    words = record.split()
    for w in words:
      mr.emit_intermediate(w, 1)

def reducer(key, list_of_values):
    """
    adds up all the instances of the key as long as word is not in stop_words or is a url
    """
    # key: word
    # value: list of occurrence counts
    total = 0
    
    if key not in stop_words and re.search(r'http:', key) == None:    
        for v in list_of_values:
          total += v
        mr.emit((key, total))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)