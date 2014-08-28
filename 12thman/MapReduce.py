import sys
import re
import collections
import json

# retain the full name since they are meaningful
fullNames = ['12th man','blue friday','can''t hold us','century link field','coach sumlin','johnny football','kenny hill','kyle field',
            'fightin texas aggies','fightin'' texas aggies','gig em','go hawks','legion of boom','pete carroll','russell wilson',
            'super bowl','super bowl 48','texas a&m university','training camp','wrecking crew'
            ]
            
def scrub(doc):
    """
    remove non-words like date ranges, punctuation, asterisks
    todo: retain single quote in Calloway's Nursery properly (regex)
    """
    cleaned_doc = doc
    cleaned_doc = cleaned_doc.lower()
    cleaned_doc = re.sub(r'--',' ',cleaned_doc)                    # --
    cleaned_doc = re.sub(r'\.\s',' ',cleaned_doc)                  # period at end of sentence
    cleaned_doc = re.sub(r'\"',' ',cleaned_doc)                    # " at end of sentence
    cleaned_doc = re.sub(r'amp;','',cleaned_doc)                   # & that has been saved as amp;
    return cleaned_doc

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
                      
class MapReduce:
    def __init__(self):
        """
        intermediate dictionary object to store the word and count that it occurs
        results in list
        """
        self.intermediate = {}
        self.result = []

    def emit_intermediate(self, key, value):
        self.intermediate.setdefault(key, [])
        self.intermediate[key].append(value)

    def emit(self, value):
        self.result.append(value) 

    def execute(self, data, mapper, reducer):
        """
        1st, reads each line in the file and passes it to Mapper
        and Mapper identifies key as the first item and values as the 2nd item
        and then spits the values into individual words and passes to emit_intermediate(word,1)
        which appends the number 1 into intermediate dict object
        
        2nd, loops through all words that were added to intermediate dict object
        and passes the word and list of occurrences to Reducer
        which loops through the values and adds them up
        and then emits the word and word count which gets added to results list
        
        3rd, the item in result list is printed out
        """
        doc = data.read()
        doc = doc.lower()
        doc = keepLongNamesIntact(doc,fullNames)
        doc = scrub(doc)
        mapper(doc)
        
        for key in self.intermediate:
            reducer(key, self.intermediate[key])

        i = 0
        # header
        print "word,count"
        while i < len(self.result):
            results = self.result[i]
            # replace ~ with space for words kept intact
            term = results[0].replace("~"," ")
            count = results[1]
            values = term+","+str(count)
            print values.replace(" , ",",")
            i += 1