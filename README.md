HADLEY BOT
A bot made for my friend hadley, which will respond to any @'s with 
something hadley herself will say. This was made with her consent, 
although she might regret it. Many of these are original quotes by her, some paraphrased or made up by me. All are 
things that she could say. The way it works is: 

You tweet the bot @HadleyTheBot
Once you run the program, the bot gets a list of all the tweets mentioning it, and responds to each according to 
the chooseMessage method. 

If "ash" is in the tweet, it uses an ash response. If "train" is in the tweet, it uses a train response. If 
"randomizer" is in the tweet, it does the randomizer response. If hadley herself(twitter handle hidden in 
ignored constants file) @s the bot, on the first tweet it sees from her it will do a hadley response. If it's the second
or more, it will either use a hadley response or any of the other normal responses. Otherwise, it just uses a default response. 

Have phrases loaded into the ignored files ashResponses, defaultresponses, gollumResponses, trainResponses, and hadleyResponses. 
Randomizer nouns and verbs are also in seperate files. All of these files line's are loaded into lists contained in the 
constants file, which is also hidden. 

This bot uses the tweepy package and twitter api to communicate with the account. 

Note in the code "screen_name" is the @_______ username on twitter, not the name. 
