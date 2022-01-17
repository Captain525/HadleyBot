HADLEY BOT
A bot made for my friend hadley, which will respond to any @'s with 
something hadley herself will say. This was made with her consent, 
although she might regret it. 

Phrases will soon be programmed into it, just wanted to make sure the 
twitter posting worked first. 

Have phrases loaded into the ignored files ashResponses, defaultresponses, gollumResponses, trainResponses, and hadleyResponses. 
Randomizer nouns and verbs are also in seperate files. ALl of these files line's are loaded into lists contained in the 
constants file, which is also hidden. 

ERROR - hadley bot keeps sending tweets when its not supposed to. Exponential growth, responds to its previous replies
need to make it so it won't respond to itself. Need to fix the updating latest tweet id tihng, but hard to do. 

THIS ERROR IS FIXED, there was a typo where it set newest Id only if it WASn'T a tweet by the bot, meaning it never did. 