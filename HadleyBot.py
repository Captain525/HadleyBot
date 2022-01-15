import tweepy
import constants
seenHadleyYet = False
def makeAPIRequest():
    #my api key from twitter developer
    consumer_key = constants.CONSUMER_KEY
    # my secret key from twitter developer.
    consumer_secret = constants.CONSUMER_SECRET;
    #authenticate .
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret);
    access_token = constants.ACCESS_TOKEN
    access_secret= constants.ACCESS_SECRET
    # gets access to the 
    auth.set_access_token(access_token, access_secret)
    #get the api. .
    api = tweepy.API(auth,wait_on_rate_limit=True)
    #me removed from api, use verifyCredentials instead
    #myUserID= (api.me()).id_str;
    return api
"""
Searches through the mention timeline and returns a list of the statuses(tweets) which 
@ the bot. Then, for each, it generates a text response with teh runHadleyBot method, which
includes the username of the person replying to in it. Then, it calls api.update_status() to 
post a tweet onto twitter. 
"""
def searchForMentions(api):
    newestID = None;
    running = True
    while(running):
        mentions = api.mentions_timeline(since_id= newestID, count=20)
        if(len(mentions) == 0):
            print("no mentions")
            break
        for status in mentions:
            #need to include the user replying to in the status itself.
            reply = runHadleyBot(status)
            #need to include the username in the tweet itself.
            newTweet = api.update_status(status=reply, in_reply_to_status_id=status.id)
            #update the newestID.
            newestID = newTweet.id


def runHadleyBot(status):
    """
    This method uses the data for the tweet sent at the bot and develops a response using
    the "bot" algorithm. Then, it makes sure to put the username of the person it's responding to in
    the tweet, at the beginning, with the @ symbol. This, along with in_reply_to_status_id = status.id,
    allow it to reply to the original tweet.
    """
    #not sure if this should be name or screen name.SCREEN NAME IS THE @ one.
    #need to put the @ at the beginning to reply properly.
    userName = "@" + status.user.screen_name;
    message = chooseMessage(status)
    tweetText =  userName+ " hey";
    return tweetText;

def chooseMessage(status):
    """
    This method picks the specific message which is sent by the bot based on the input text. Status is the tweet
    itself as a tweepy object, you can use status.text to get the text string itself.

    IF the screenname of the user is equal to hadley's screen name(hidden), and you haven't responded to hadley yet on
    this run of the program, it sends a response to her.
    """
    from numpy.random import seed
    from numpy.random import randint
    #if the original hadley tweets the bot for the first time in this run of the program, it responds using the hadleyResponses list
    if status.user.screen_name == constants.INSPIRATION_TWITTER and not seenHadleyYet:
        randomChoice = randint(0, len(constants.hadleyResponses) - 1)
        return constants.hadleyResponses[randomChoice]
    #check for the format "you're _______"
    wordList = status.text.split()
    if len(wordList) != 0 and wordList[0].lower() == "you're" and len(wordList) == 2:
        return "No YOU'RE " + wordList[1]

    seed(12)
    if status !=None and "ash" in status.text.lower():
        randomChoice = randint(0, len(constants.ashList) -1)
        return constants.ashList[randomChoice]
    elif status !=None and "train" in status.text.lower():
        randomChoice = randint(0, len(constants.trainList)-1)
        return constants.trainList[randomChoice]
    elif status !=None and "randomizer" in status.text.lower():
        """
            this section generates statements in the form of: i want ash to _______ my ________ where the first blank is a
            randomly generated verb, and the second is a randomly generated noun. This response is made when you type in randomizer
            in your tweet to the bot.
        """
        randomVerbChoice = randint(0, len(constants.verbList)-1)
        randomNounChoice = randint(0, len(constants.nounList)-1)
        return "I want ash to " + constants.verbList[randomVerbChoice] + " my " + constants.nounList[randomNounChoice]
    else:
        #minus 1 since inclusive.
        randomChoice = randint(0, len(constants.totalList) - 1)
        return constants.totalList[randomChoice]


"""
makes the list from the file. 
"""
def makeListFromFile(fileName):
    try:
        with open(fileName,"r") as file:
            #gets rid of the extra characters like newline. This gets the list of all the lines in the given file.
            list = [line.strip() for line in file.readlines()]
            return list
    except Exception as e:
        print(str(e))
        return None


def main():
    api = makeAPIRequest();
    searchForMentions(api)
    return 0

if __name__ == "__main__":
    main()