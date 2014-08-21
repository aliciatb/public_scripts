import os
import sys
import urllib
import json
import re
from datetime import datetime

aggie = ['12thmanfoundation','a&m','aggie','aggies','aggiefootball','aggieland','aggielandticket','aggies','caneck','cfb','coachsumlin','college station','college','em','gig','gigem','hookemhorns','houston','hullabaloo','infringement','infringements','jason_cook','jmanziel2','johnny','johnnyfootball','kyle','kylefield','manziel','maroon','midnight','reveille','sec','secfamily','secnetwork','sumlin','tamu','texas','trademark','tm','licensingtamuedu','whoop','yell']
seahawk = ['12s','206','48','49ers','9er','9ers','beastmode','blue','bluefriday','broncos','carroll','century','centurylink_fld','clink','dangeruss','dangerusswilson','dougbaldwinjr','denver','fieldgulls','flag','gohawks','harbaugh','hak','hawk','hawknation','hawks','legionofboom','link','lob','lombardi','lynch','malcsmitty','money','moneylynch','nfc','nfl','nfltrainingcamp','niner','pete','pnw','pst','russ','rsherman_25','sb48','seagals','seahawk','seahawks','seattle','sherman','sounders','super','superbowl','superbowlchamps','trainingcamp','vmac','west','whiner','whiners','whynotus','wilson','world','wsdot_traffic']

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
  if re.search(r'206|alaska|washington|wa|seahawk|seattle|north|west|pnw', loc) <> None:
    return "Seahawk"
  elif re.search(r'aggie|aggieland|college|station|tx|texas|brazos|bryan|college station|houston', loc) <> None:
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
      #print tweet
      if 'text' in tweet:
        tweet_text = tweet["text"]
        words = {}  # initialize list of words in the tweet
        words = tweet["text"].split()
        aggieTerms = 0
        seahawkTerms = 0
        for w in words:
          scrubbed_word = scrubWord(w)
          if scrubbed_word in aggie or re.search(r'aggie|btho|tamu', scrubbed_word) <> None:
            aggieTerms += 1
          if scrubbed_word in seahawk or re.search(r'hawk|12s|boom|seattle', scrubbed_word) <> None:
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
        
    except Exception as e:
      #print e
      exList.append(tweet)
  return fanTweet

def saveTeamTweets(team, tweets):
  teamTweets = team.lower() + "_tweets.txt"
  f = open("output/" + teamTweets,"w")
  i = 0
  while i < len(tweets):
    f.write(tweets[i].encode('utf-8'))
    i +=1
  f.close()
  print teamTweets,"created with",i,"tweets"

def saveResults(results):
  """
  output to csv for analysis
  """
  f = open("output/output.csv", "w")
  f.write('location' + "," + 'stamp' + "," + 'team' + "," + 'user_name' + "," + 'tweet_id' + "," + 'tweet' + "\n")
  # track records
  n = 0
  # group team tweets for wordcloud
  aggie_tweets = []
  seahawk_tweets = []
  other_tweets = []
  for key in results.keys():    
    id = key
    col = results[key].split("|")
    location = col[0]
    location = re.sub(r'[,]',' ', location)
    stamp = col[1]  
    team = col[2]
    user_name = col[3]
    # use reg ex to filter out line breaks and commas before creating csv file
    text = re.sub(r'[\n]',' ', col[4])
    text = re.sub(r'[,]',' ', text)
    f.write(location.encode('utf-8') + "," + stamp.encode('utf-8') + "," + team.encode('utf-8') + "," + user_name.encode('utf-8') + "," + id.encode('utf-8') + "," + text.encode('utf-8') + "\n")
#   print results[key], key
    if team == "Aggie":
      aggie_tweets.append(text)
    if team == "Seahawk":
      seahawk_tweets.append(text)
    if team == "Other":
      other_tweets.append(text)
    n += 1
  f.close()
  print "{:,}".format(n),"total tweets!"
  saveTeamTweets("Aggie",aggie_tweets)
  saveTeamTweets("Seahawk",seahawk_tweets)
  saveTeamTweets("Other",other_tweets)

def main():
  """
  load the tweets file
  """
  dir = sys.argv[1]
  all = {}
  print "Processing files..."
  for fn in os.listdir(dir):
    # match only tweets files 
    if re.search(r'^tweets', fn):
      tweet_file = open(dir+'/'+fn)
      i = 0
      results = parseTweets(tweet_file)
      for key in results.keys():
        i +=1
        all[key] = results[key]
      print fn,"contains",i,"tweets"
  
  saveResults(all)

#  for key in all.keys():
#    print all[key], key

if __name__ == '__main__':
    main()