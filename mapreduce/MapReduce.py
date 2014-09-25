import json

class MapReduce:
    def __init__(self):
        """
        intermediate dictionary object to store the word and number of instances that it occurs
        results in list
        """
        self.intermediate = {}
        self.result = []

    def emit_intermediate(self, key, value):
#         print "key=",key
#         print "value=",value
        self.intermediate.setdefault(key, [])
        self.intermediate[key].append(value)

    def emit(self, value):
        self.result.append(value) 

    def execute(self, data, mapper, reducer):
        """
        1st, reads each line in the file and passes it to Mapper
        and Mapper identifies key (document id) as the first item and values (all words in the document) as the 2nd item
        and then spits the values into individual words and passes to emit_intermediate(word,1)
        which appends the number 1 into intermediate dict object
        
        2nd, loops through all words that were added to intermediate dict object
        and passes the word and list of occurrences to Reducer
        which loops through the values and adds them up
        and then emits the word and word count which gets added to results list
        
        3rd, the item in result list is printed out
        """
        for line in data:
            record = json.loads(line)
            mapper(record)

        for key in self.intermediate:
            reducer(key, self.intermediate[key])

        self.result.sort()
        jenc = json.JSONEncoder()
#         for item in self.result:
#             print jenc.encode(item)