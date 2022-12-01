import requests
import textstat
import emoji

from config import Bearer_Token



def get_lexile_score(twitter_name):
    user_request = requests.get('https://api.twitter.com/2/users/by/username/'+ twitter_name, headers = {'Authorization' : 'Bearer ' + Bearer_Token})
    user_id = user_request.json()['data']['id']

    user_tweets_request = requests.get('https://api.twitter.com/2/users/' + user_id + '/tweets', headers = {'Authorization' : 'Bearer ' + Bearer_Token})
    user_tweets = user_tweets_request.json()['data']
    tweet_texts = [tweet_object['text'] for tweet_object in user_tweets]
    print(tweet_texts)
    tweet_texts = filter(lambda a: ('RT' not in a), tweet_texts) #remove retweets (quote tweet text doesn't have RT, instead url of quoted tweet)

    def remove_urls(tweet): #takes out urls from tweet bc they would inflate lexile scores (includes both quote tweets and images and gifs)
        words = tweet.split()
        words = filter(lambda w: ('http' not in w), words)
        words = filter(lambda w: ('@' not in w), words) #remove usernames from replies bc they inflate score
        newtweet = ''
        for word in words:
            newtweet = newtweet + word + ' '
        return(newtweet)

    def remove_emojis(tweet): #removes emojis bc they screw up score -- also  emojis differ in lexile content :)    

        allchars = [s for s in tweet]
        newchars = filter(lambda c: (emoji.is_emoji(c) == False), allchars)
        newtweet = ''
        for c in newchars:
            newtweet = newtweet + c
        return(newtweet)

    tweet_texts = [remove_urls(tw) for tw in tweet_texts]
    tweet_texts = [remove_emojis(tw) for tw in tweet_texts]
    tweet_texts = [tw for tw in tweet_texts if tw.strip()] #remove empty strings and whitespace strings
    #tweet_texts = list(filter(lambda w: (w != ''), tweet_texts))
    print(tweet_texts)

    tweet_scores = [textstat.automated_readability_index(tweet) for tweet in tweet_texts]
    tweet_scores_flesch = [textstat.flesch_kincaid_grade(tweet) for tweet in tweet_texts]
    print(tweet_scores_flesch)

    mean_tweet_scores_flesch = sum(tweet_scores_flesch) / len(tweet_scores_flesch)
    return(mean_tweet_scores_flesch)

