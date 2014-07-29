import sys
import urllib
import json
import re

aggie = ['a&m','aggie','aggiefootball','aggieland','aggielandticket','aggies','cfb','college station','college','em','gig','houston','hullabaloo','johnny','kyle','manziel','midnight','SECNetwork','whoop','yell']
seahawk = ['12s','48','carroll','century','clink','dangeruss','gohawks','harbaugh','hawk','hawks','link','lob','money','moneylynch','nfc','nfl','pete','pnw','sb48','seagals','seahawk','seahawks','seattle','sherman','super','superbowl','vmac','west','wilson']

def getTeam(aggies, seahawks):
  """
  team with largest word count wins, though unlikely to be a mixed team tweet so other team should equal zero
  """
  if int(aggies) > int(seahawks):
    return "Aggie"
  elif int(seahawks) > int(aggies):
    return "Seahawk"
  else:
    return "Other"  

def scrubWord(word):
  """
  set all words to lowercase and reg expression to remove non alpha numeric
  """
  scrubbed = word.lower()
  scrubbed = re.sub(r'[^a-zA-Z0-9]','', scrubbed)
  return scrubbed

def parseTweets(tweets):
  """
  analyze description to determine fan allegiance
  """
  fanTweet = {}     # capture tweet and fan affiliation
  exList = []       #capture exceptions
  for line in tweets:
    try:
      tweet = json.loads(line)
      if 'text' in tweet:
        words = {}  # initialize list of words in the tweet
        words = tweet["text"].split()
        aggieTerms = 0
        seahawkTerms = 0
        for w in words:
          # print w
          scrubbed_word = scrubWord(w)
          if scrubbed_word in aggie:
            aggieTerms += 1
          if scrubbed_word in seahawk:
            seahawkTerms += 1
        # add the tweet and fan affiliation
        fanTweet[tweet["text"]] = getTeam(aggieTerms, seahawkTerms)  
    except:
      exList.append(tweet)
  return fanTweet

def saveResults(results):
  """
  output to csv for analysis
  """
  f = open("output.csv", "w")
  for key in results.keys():
    f.write(results[key] + "," + key.encode('utf-8') + "\n")
    print results[key], key
  f.close()

def main():
  """
  load the tweets file
  """
  tweet_file = open(sys.argv[1])
  results = parseTweets(tweet_file)
  saveResults(results)

if __name__ == '__main__':
    main()