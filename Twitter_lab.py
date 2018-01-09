"""
Name: Jonathan Henry
Assignment: Lab06
Title: Regular Expressions to Extract Twitter Information
Course: CSCE186
Semester: Fall 2017
Date: 11/24/17
Sources: Twitter API, RegEx Cheatsheet
Description: This program pulls a defined number of new tweets from twitter and specific characteristics of the group of tweets are described and visualized. 

*** Be sure to change the app key, app secret, token key, and token secret on lines 106, 119, 127. This can be found under your twitter developer API settings. ***
"""
import json
import unicodedata
from twython import TwythonStreamer
import re
import matplotlib.pyplot as plt

tweets = {}
count = 1
maxtweets = 1

#streamer for new tweets
class program(TwythonStreamer):
    def on_success(self,data):
        global tweets
        global count
        if 'text' in data and 'lang' in data and count <= maxtweets: 
            if data["lang"] == "en":
                tweets[count] = data
                count += 1 
        elif count > maxtweets:
            self.disconnect()
    def on_error(self,status_code,data):
        print status_code, data
        self.disconnect()

#Main Menu
def menu():
    test = 0
    while True: 
        #menu
        userInput = input("1. Get Information\n2. Extract Information\n3. Plot Information\n4. Exit\n\nEnter Choice (Please call option 1 first): ")
        
        #get tweets/open file
        if userInput == 1:
            tweetDict = info()
            test += 1
        
        #extract information
        elif userInput == 2 and test >= 1:
            extract(tweetDict)
        
        #plots tweets
        elif userInput == 3 and test >= 1:
            tweetPlot(tweetDict)
        
        #exit
        elif userInput == 4:
            break
        
        else:
            print("WRONG! Incorrect option. Please try again.")

#load file
def info():
    
    global tweets
    #menu
    userInput = input("\n1. Use file\n2. Get new data\n\nEnter Choice (Choice 2 must be selected first in order to create the file): ")
    
    #load from drive
    if userInput == 1:
        fileInput = raw_input("Enter the file name: ")
        with open(str(fileInput)+'.json', 'r') as fp:
            userFile = json.load(fp)
        print("\nSuccess!\n")
        return(userFile)
    
    #create new file
    elif userInput == 2:
        infomenu()
        userFileInput = raw_input("Enter a name for your JSON file: ")
        with open(str(userFileInput)+'.json','w') as fp:
            json.dump(tweets, fp, indent = 10)
        with open(str(userFileInput)+'.json', 'r') as fp:  
            userFile = json.load(fp)
        print("\nSuccess!\n")
        return(userFile)
        
    
    else:
        print("WRONG! Incorrect option. Please try again.")

#options to get tweets from
def infomenu():
    #menu
    global maxtweets 
    maxtweets = input("\nEnter how many tweets you'd like to use: ")
    userInput = input("\nHow would you like to collect tweets? (loading times may vary greatly depending on tweet rates of users and locations)\n1. Enter keyword\n2. Enter coordinates\n3. Enter user ID\n\nEnter choice: ")
    
    #tweets by search term
    if userInput == 1: 
        userTerm = raw_input("Enter a term to search for: ")
        print("Loading...\n")
        stream = program("app_key", "app_secret", "auth_token", "auth_token secret") #change me!
        stream.statuses.filter(track=str(userTerm))
        print("Success!\n")
    
    #tweets by geocoordinates 
    elif userInput == 2:
        print "Twitter's filter by location service works by creating a fenced area that tweets are allowed to come through in. In order to do so, please provide two coordinates.\n"
        userLocation1 = raw_input("Enter SW corner Northern coordinate: ")
        userLocation2 = raw_input("Enter SW corner Western coordinate: ")
        userLocation3 = raw_input("Enter NE Northern coordinate: ")
        userLocation4 = raw_input("Enter NE Western coordinate: ")
        userLocation = [userLocation1, userLocation2, userLocation3, userLocation4]
        print("Loading...\n")
        stream = program("app_key", "app_secret", "auth_token", "auth_token secret") #change me!
        stream.statuses.filter(locations = userLocation)    
        print("Success!\n")
    
    #tweets by user ID (not username)
    elif userinput == 3:
        userID = input("Enter a user ID (not a username) to search for: ")
        print("Loading...\n")
        stream = program("app_key", "app_secret", "auth_token", "auth_token secret") #change me!
        stream.statuses.filter(follow = userID)
        print("Success!\n")
    
    else:
         print("WRONG! Incorrect option. Please try again.")


#plots tweet data
def tweetPlot(tweetDict): 
    #menu
    userinput = input("1. Plot the number of tweets by user.\n2. Plot the number of tweets by location.\n3. Plot number of tweets by length.\n\nEnter choice: ")
    print "\n"
    
    if userinput == 1:
        #Number of tweets by user
        userDict = {}
        userKeys = []
        userVals = []
        
        for i in range(1,len(tweetDict.items())+1):
            user = unicodedata.normalize('NFKD', tweetDict[str(i)]["user"]["screen_name"]).encode('ascii','ignore')
            userDict[user] = userDict.get(i,0) + 1
        
        for k,v in userDict.items():
            userKeys.append(k)
            userVals.append(v)
        
        res1 = zip(userVals, userKeys)
        res1.sort(reverse = True)
        usernames = []
        usertweets = []
        
        for k,v in res1[0:6]:
            usertweets.append(k)
            usernames.append(v)
        
        plt.bar(range(len(usertweets)), usertweets)
        plt.title("Users who made most tweets")
        plt.xlabel("Username")
        plt.xticks(range(len(usertweets)), usernames, rotation = 'vertical')
        plt.ylabel("Number of tweets")
        plt.show()
    
    elif userinput == 2:
        #Number of tweets by location (PA, NY, Other)
        tweetsbylocation = {}
        statekeys = []
        statevals = []
        
        for i in range(1,len(tweetDict.items())+1):
            
            if tweetDict[str(i)]["user"]["location"] is not None:
                tweetsearch = unicodedata.normalize('NFKD', tweetDict[str(i)]["user"]["location"]).encode('ascii','ignore')
                location = re.compile(r"(Pennsylvania|PA|NY|New York|New York City)", re.IGNORECASE)
                res = location.search(tweetsearch)
                if res is not None:
                    g = res.group(1) 
                    if g == "PA" or g == "Pennyslvania":
                        tweetsbylocation["PA"] = tweetsbylocation.get("PA",0) + 1
                    if g == "NY" or g == "New York" or g == "New York City":
                        tweetsbylocation["NY"] = tweetsbylocation.get("NY",0) + 1
                elif res is None:
                    tweetsbylocation["Other"] = tweetsbylocation.get("Other", 0) + 1
            
            else:
                tweetsbylocation["Other"] = tweetsbylocation.get("Other", 0) + 1
        
        for k,v in tweetsbylocation.items():
            statekeys.append(k)
            statevals.append(v)
        
        res = zip(statevals, statekeys)
        res.sort(reverse = True)
        print res
        statekeys = []
        statevals = []
        
        for k,v in res:
            statekeys.append(v)
            statevals.append(k)
        
        plt.bar(range(len(statevals)), statevals)
        plt.xlabel("States")
        plt.xticks(range(len(statekeys)), statekeys, rotation = 'vertical')
        plt.ylabel("Number of tweets")
        plt.title("Tweets by Location")
        plt.show()

    elif userinput == 3:
        #Number of tweets by length
        LenTweetsDict = {}
        TweetLength = []
        NumberTweets = []
        
        for i in range(1,len(tweetDict.items())+1):
            text = unicodedata.normalize('NFKD', tweetDict[str(i)]["text"]).encode('ascii','ignore')
            if len(text) <= 50:
                LenTweetsDict["0-50"] = LenTweetsDict.get("0-50", 0) + 1
            elif len(text) <= 100 and len(text) > 50:
                LenTweetsDict["50-100"] = LenTweetsDict.get("50-100", 0) + 1
            elif len(text) > 100:
                LenTweetsDict["Greater than 100"] = LenTweetsDict.get("Greater than 100", 0) + 1
        
        for k,v in LenTweetsDict.items():
            TweetLength.append(k)
            NumberTweets.append(v)
        res2 = zip(NumberTweets, TweetLength)
        res2.sort(reverse = True)
        TweetLength = []
        NumberTweets = []
        
        for k,v in res2:
            NumberTweets.append(k)
            TweetLength.append(v)
        
        plt.bar(range(len(TweetLength)), NumberTweets)
        plt.title("Tweets by length")
        plt.xlabel("Length of tweet")
        plt.xticks(range(len(TweetLength)), TweetLength, rotation = 'vertical')
        plt.ylabel("Number of tweets")
        plt.show()

#describes various aspects of tweets
def extract(tweetDict):
    #Number of tweets with caps
    yelling = 0
    for i in range(1,len(tweetDict.items())+1):
        query = unicodedata.normalize('NFKD', tweetDict[str(i)]["text"]).encode('ascii','ignore')
        caps = re.compile(r"[A-Z]{3,} [A-Z]{3,}")
        result = caps.search(query)
        if result is not None:
            yelling += 1
    print "\nNumber of tweets with consecutive words in all caps: " + str(yelling) + "\n"
    
    #Number of tweets that are retweets
    retweets = 0
    for i in range(1,len(tweetDict.items())+1):
        search = unicodedata.normalize('NFKD', tweetDict[str(i)]["text"]).encode('ascii','ignore')
        retweet = re.compile(r"^RT @")
        res2 = retweet.search(search)
        if res2 is not None:
            retweets += 1
    print "The number of tweets that are retweets is: " + str(retweets) + "\n"

    #Most popular website tweeted
    tweetsWebsiteDict = {}
    webkeys = []
    webvals = []
    for i in range(1,len(tweetDict.items())+1):
        tweetsearch = unicodedata.normalize('NFKD', tweetDict[str(i)]["text"]).encode('ascii','ignore')
        website = re.compile(r"((https?:\/\/)?(www.)?(\w)+(\.)(\w{2,4})(\/)?(\w|\/)*)")
        res4 = website.search(tweetsearch)
        if res4 is not None:
            g = res4.group(1)    
            tweetsWebsiteDict[g] = tweetsWebsiteDict.get(g,0) + 1
    for k,v in tweetsWebsiteDict.items():
        webkeys.append(k)
        webvals.append(v)
    res3 = zip(webvals, webkeys)
    res3.sort(reverse = True)
    print "The top 5 links tweeted are: " + str(res3[0:5]) + "\n"

    #Most popular hashtag
    hashtagDict = {}
    hashtagKeys = []
    hashtagVals = []
    for i in range(1,len(tweetDict.items())+1):
        text = unicodedata.normalize('NFKD', tweetDict[str(i)]["text"]).encode('ascii','ignore')
        hashtag = re.findall(r"\#\w+", text)
        for i in hashtag:
            if i is not None:
                hashtagDict[i] = hashtagDict.get(i,0) + 1
    for k,v in hashtagDict.items():
        hashtagKeys.append(k)
        hashtagVals.append(v)
    res = zip(hashtagVals, hashtagKeys)
    res.sort(reverse = True)
    print "The top 5 hashtags are: " + str(res[0:5]) + "\n"
    
    #Most popular user mentioned
    userDict = {}
    userKeys = []
    userVals = []
    for i in range(1,len(tweetDict.items())+1):
        text = unicodedata.normalize('NFKD', tweetDict[str(i)]["text"]).encode('ascii','ignore')
        user = re.findall(r"\@\w+", text)
        for i in user:
            if i is not None:
                userDict[i] = userDict.get(i,0) + 1
    for k,v in userDict.items():
        userKeys.append(k)
        userVals.append(v)
    res1 = zip(userVals, userKeys)
    res1.sort(reverse = True)
    print "The top 5 Users mentioned are: " + str(res1[0:5]) + "\n\n"

menu()    