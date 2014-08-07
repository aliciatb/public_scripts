import os
import sys
import urllib
import json
import re
from datetime import datetime

aggie = ['a&m','aggie','aggiefootball','aggieland','aggielandticket','aggies','cfb','college station','college','em','gig','gigem','houston','hullabaloo','johnny','kyle','manziel','midnight','sec','secnetwork','tamu','texas','licensingtamuedu','whoop','yell']
seahawk = ['12s','48','49ers','beastmode','broncos','carroll','century','clink','dangeruss','dougbaldwinjr','denver','gohawks','harbaugh','hak','hawk','hawknation','hawks','legionofboom','link','lob','lynch','malcsmitty','money','moneylynch','nfc','nfl','nfltrainingcamp','pete','pnw','pst','russ','rsherman_25','sb48','seagals','seahawk','seahawks','seattle','sherman','sounders','super','superbowl','superbowlchamps','trainingcamp','vmac','west','whynotus','wilson','world']

aggieTweets = []
seahawkTweets = []
otherTweets = []

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
  if re.search(r'washington|wa|seattle|north|west|#pnw', loc):
    return "Seahawk"
  elif re.search(r'college|station|tx|texas|bryan|college station|houston', loc):
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
  # scrubbed = re.sub(r'[^\x00-\x7F]','', scrubbed)
  # scrubbed = re.sub(r'[^\x20-\x7F]','', scrubbed)
  return scrubbed

def scrubDate(dt):
  # twitter format = Sat Mar 17 18:21:20 +0000 2012
  # slice dataparts
  y = dt[-4:]
  m = dt[4:7]
  d = dt[8:10]
  # Mar 30 2014
  slicedDt = str(m) + " " + str(d) + " " + str(y)
  result = datetime.strptime(slicedDt, "%b %d %Y")
  # print result
  return result

def parseTweets(tweets):
  """
  analyze description to determine fan allegiance
  """
  fanTweet = {}     # capture tweet and fan affiliation
  exList = []       #capture exceptions
  tweet = ""
  for line in tweets:
    try:
      tweet = json.loads(line)
      if 'text' in tweet:
        tweet_text = tweet["text"]
        words = {}  # initialize list of words in the tweet
        words = tweet["text"].split()
        aggieTerms = 0
        seahawkTerms = 0
        for w in words:
          scrubbed_word = scrubWord(w)
          re_aggie = r'aggie'
          if scrubbed_word in aggie or re.search(re_aggie, scrubbed_word):
            aggieTerms += 1
          re_seahawk = r'hawk|12s|boom|seattle'
          if scrubbed_word in seahawk or re.search(re_seahawk, scrubbed_word):
            seahawkTerms += 1
        team = getTeam(aggieTerms, seahawkTerms)
        # location of tweeter
        location = "none"
        if tweet["user"]["location"] <> "":
          location = tweet["user"]["location"]
          if team == "Other":
            team = getTeamByLocation(location)
        stamp = "none"
        if tweet["created_at"] <> "":
          stamp = tweet["created_at"]
          stamp = str(scrubDate(stamp))
        if tweet["id_str"] <> "":
          tweet_id = tweet["id_str"]
        if tweet["user"]["screen_name"] <> "":
          user_name = tweet["user"]["screen_name"]
        
        # add the tweet info and derived fan affiliation
        fanTweet[tweet_id] =  location + "|" + stamp + "|" + team + "|" + user_name + "|" + tweet_text
        
    except:
      exList.append(tweet)
  return fanTweet

def saveResults(results):
  """
  output to csv for analysis
  """
  f = open("output.csv", "w")
  f.write('location' + "," + 'stamp' + "," + 'team' + "," + 'user_name' + "," + 'tweet_id' + "," + 'tweet' + "\n")
  for key in results.keys():    
    id = key
    col = results[key].split("|")
    location = col[0]
    location = re.sub(r'[,]',' ', location)
    stamp = col[1]  
    team = col[2]
    user_name = col[3]
    text = re.sub(r'[\n]',' ', col[4])
    text = re.sub(r'[,]',' ', text)
    f.write(location.encode('utf-8') + "," + stamp.encode('utf-8') + "," + team.encode('utf-8') + "," + user_name.encode('utf-8') + "," + id.encode('utf-8') + "," + text.encode('utf-8') + "\n")
#   print results[key], key
  f.close()
  
def main():
  """
  load the tweets file
  """
  dir = sys.argv[1]
  all = {} 
  for fn in os.listdir(dir):
    # match only tweets files
    if re.search(r'^tweets', fn):
      tweet_file = open(dir+'/'+fn)
      results = parseTweets(tweet_file)
      for key in results.keys():
        all[key] = results[key]
  
  saveResults(all)

#  for key in all.keys():
#    print all[key], key

if __name__ == '__main__':
    main()