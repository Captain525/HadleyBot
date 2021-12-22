import tweepy
import constants
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


"""
This method uses the data for the tweet sent at the bot and develops a response using 
the "bot" algorithm. Then, it makes sure to put the username of the person it's responding to in
the tweet, at the beginning, with the @ symbol. This, along with in_reply_to_status_id = status.id, 
allow it to reply to the original tweet. 

"""
def runHadleyBot(status):
    #not sure if this should be name or screen name.SCREEN NAME IS THE @ one.
    #need to put the @ at the beginning to reply properly.
    userName = "@" + status.user.screen_name;
    tweetText =  userName+ " hey";
    return tweetText;



def main():
    api = makeAPIRequest();
    searchForMentions(api)
    return 0

if __name__ == "__main__":
    main()