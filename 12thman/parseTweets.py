import sys
import urllib
import json
import re

aggie = ['a&m','aggie','aggiefootball','aggieland','aggielandticket','aggies','cfb','college station','college','em','gig','houston','hullabaloo','johnny','kyle','manziel','midnight','SECNetwork','whoop','yell']
seahawk = ['12s','48','beastmode','carroll','century','clink','dangeruss','gohawks','harbaugh','hawk','hawks','legionofboom','link','lob','money','moneylynch','nfc','nfl','pete','pnw','russ','sb48','seagals','seahawk','seahawks','seattle','sherman','super','superbowl','vmac','west','wilson']

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

def getTeamByLocation(location):
  """
  assume that northwest folks prefer the Seahawks
  """
  loc = location.lower()
  if re.search(r'washington|wa|seattle|north|west', loc):
    return "Seahawk"
  elif re.search(r'college|station|tx|texas|college station|houston', loc):
    return "Aggie"
  else:
    return "Other"

def scrubWord(word):
  """
  set all words to lowercase and reg expression to remove non alpha numeric
  """
  scrubbed = word.lower()
  scrubbed = re.sub(r'[^a-zA-Z0-9]','', scrubbed)
  # todo: emoticons!
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
          scrubbed_word = scrubWord(w)
          if scrubbed_word in aggie:
            aggieTerms += 1
          if scrubbed_word in seahawk:
            seahawkTerms += 1
        team = getTeam(aggieTerms, seahawkTerms)
        # location of tweeter
        if tweet["user"]["location"] <> "":
          location = tweet["user"]["location"]
          if team == "Other":
            team = getTeamByLocation(location)
        if tweet["user"]["created_at"] <> "":
          stamp = tweet["user"]["created_at"]
        # add the tweet and fan affiliation
        fanTweet[tweet["text"]] = team
        
    except:
      exList.append(tweet)
  return fanTweet

def saveResults(results):
  """
  output to csv for analysis
  """
  f = open("output.csv", "w")
  f.write('team'+ "," + 'tweet' + "\n")
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