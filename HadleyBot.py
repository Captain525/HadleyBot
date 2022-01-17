import tweepy
import constants

seenHadleyYet = False

def makeAPIRequest():
    """
    Make a request to the twitter api using tweepy. The access token links it to the account i want to tweet from.
    Get authentication using the consumer and secret keys, then get the access using the access and secret tokens. Then, you can access
    the tweepy api with this authentication thing.
    """
    # my api key from twitter developer
    consumer_key = constants.CONSUMER_KEY
    # my secret key from twitter developer.
    consumer_secret = constants.CONSUMER_SECRET;
    # authenticate .
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret);
    access_token = constants.ACCESS_TOKEN
    access_secret = constants.ACCESS_SECRET
    # gets access to the 
    auth.set_access_token(access_token, access_secret)
    # get the api. .
    api = tweepy.API(auth, wait_on_rate_limit=True)
    # me removed from api, use verifyCredentials instead
    return api


def searchForMentions(api):
    """
    Searches through the mention timeline and returns a list of the statuses(tweets) which
    @ the bot. Then, for each, it generates a text response with teh runHadleyBot method, which
    includes the username of the person replying to in it. Then, it calls api.update_status() to
    post a tweet onto twitter.

    Initializing newest id to the id of the bot's most recent tweet makes it so that it doesn't respond to old messages,
    just the new ones.
    """
    # get the most recent tweet by the bot. Don't want any things on timeline from before this most recent tweet, since this is the last time the bot was active.
    timeline = api.user_timeline(screen_name=constants.BOT_USERNAME, count=1)
    newestTweet = None
    #avoids case where the timeline length is 0 so out of bounds error.
    if len(timeline)>0:
        newestTweet = timeline[0]

    newestID = None
    # if there is a newest tweet, get its id.
    if newestTweet != None:
        newestID = newestTweet.id

    while True:
        #  only fetch mentions NEWER than "newestID" meaning mentions which happened sooner than the most recent tweet.
        mentions = api.mentions_timeline(since_id=newestID)
        #  need this to break out of the loop.
        if len(mentions) == 0:
            print("no mentions")
            break
        #loop through statuses in the mentions
        for status in mentions:
            reply = runHadleyBot(status)
            #  need to include the username in the tweet itself.
            newTweet = api.update_status(status=reply, in_reply_to_status_id=status.id)
        # update the newestID once done all the previous mentions, to get the new mentions AFTER this tweet.
        newestID = newTweet.id


def runHadleyBot(status):
    """
    This method uses the data for the tweet sent at the bot and develops a response using
    the "bot" algorithm. Then, it makes sure to put the username of the person it's responding to in
    the tweet, at the beginning, with the @ symbol. This, along with in_reply_to_status_id = status.id,
    allow it to reply to the original tweet.
    """
    # not sure if this should be name or screen name.SCREEN NAME IS THE @ one.
    # need to put the @ at the beginning to reply properly.

    userName = "@" + status.user.screen_name;
    message = chooseMessage(status)
    tweetText = userName + " " + message
    return tweetText;


def chooseMessage(status):
    """
    This method picks the specific message which is sent by the bot based on the input text. Status is the tweet
    itself as a tweepy object, you can use status.text to get the text string itself.

    IF the screenname of the user is equal to hadley's screen name(hidden), and you haven't responded to hadley yet on
    this run of the program, it sends a response to her.
    """
    global seenHadleyYet
    from numpy.random import randint
    if status is None:
        return None
    # if the original hadley tweets the bot for the first in this program, run response using the hadleyResponses list
    if status.user.screen_name == constants.INSPIRATION_TWITTER and not seenHadleyYet:
        randomChoice = randint(0, len(constants.hadleyResponses) - 1)
        seenHadleyYet = True
        return constants.hadleyResponses[randomChoice]

    # check for the format "you're _______"
    wordList = status.text.split()
    #wordList[0] is the @
    #keeping the word list 1 thing because only want to do this if you're is at the beginning.
    if len(wordList) != 0 and wordList[1].lower() == "you're":
        #get the stuff we want from beginning of tweet to the period.
        a = len(status.text)
        b = len(status.text)
        c = len(status.text)
        d = len(status.text)
        if '.' in status.text:
            a = status.text.index(".")
        if '!' in status.text:
            b = status.text.index("!")
        if '?' in status.text:
            c = status.text.index("?")
        if ',' in status.text:
            d = status.text.index(",")

        minVal = min(a,b,c,d)
        if minVal == len(status.text):
            endText = status.text
        elif minVal == a:
            endText = status.text.partition('.')[0] + '.'
        elif minVal == b:
            endText = status.text.partition('!')[0] + '!'
        elif minVal == c:
            endText = status.text.partition('?')[0] + '?'
        elif minVal == d:
            endText = status.text.partition(',')[0] + '.'
        print(endText)
        #cut out the @ and the you're
        finalText = endText.lower().partition("you're")[2]
        return "No YOU'RE" + finalText

    #ash mentioned, so have ash response.
    if "ash" in status.text.lower():
        randomChoice = randint(0, len(constants.ashList) - 1)
        return constants.ashList[randomChoice]
    #train mentioned, so have train response
    elif "train" in status.text.lower():
        randomChoice = randint(0, len(constants.trainList) - 1)
        return constants.trainList[randomChoice]
    #randomizer mentioned, so do the randomizer.
    elif "randomizer" in status.text.lower():
        """
            this section generates statements in the form of: i want ash to _______ my ________ where the first blank is a
            randomly generated verb, and the second is a randomly generated noun. This response is made when you type in randomizer
            in your tweet to the bot.
        """
        randomVerbChoice = randint(0, len(constants.verbList) - 1)
        randomNounChoice = randint(0, len(constants.nounList) - 1)
        return "I want ash to " + constants.verbList[randomVerbChoice] + " my " + constants.nounList[randomNounChoice]

    # adds hadley specific tweets to the list of possible tweets. This has nothing to do with it always occuring the first time.
    elif status.user.screen_name == constants.INSPIRATION_TWITTER:
        randomChoice = randint(0, len(constants.hadleyList)-1)
        return constants.totalList[randomChoice]
    # for any tweet which doesn't fit the previous categories.
    else:
        # minus 1 since inclusive.
        randomChoice = randint(0, len(constants.totalList) - 1)
        return constants.totalList[randomChoice]

def deleteAllTweets(api):
    """
    This function deletes all of the bot's tweets.
    """
    timeline = api.user_timeline(screen_name = constants.BOT_USERNAME)
    for status in timeline:
        api.destroy_status(status.id)
    print("all tweets deleted!")

def main():
    api = makeAPIRequest()
    searchForMentions(api)
    #deleteAllTweets(api)
    return 0


if __name__ == "__main__":
    main()


def makeListFromFile(fileName):
    """
    makes the list from the file. Called from hidden constants.py file.
    """
    try:
        # need the encoding to allow apostrophes.
        with open(fileName, "r", encoding='utf-8') as file:
            # gets rid of the extra characters like newline. This gets the list of all the lines in the given file.
            list = [line.strip() for line in file.readlines()]
            return list
    except Exception as e:
        print(str(e))
        return None
