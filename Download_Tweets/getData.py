'''
This script take in input three arguments

USAGE: 
$ python3.5 getData.py 'topic' num_tweets 'ys'

'ys' means if you want also to save the html of the tweet, otherwise just write 'yn'
It saves the images and all the most important info about
the last num_tweets-th tweets
'''


import tweepy
from tweepy import OAuthHandler
import json
import urllib
import os
import sys

def main():

    consumer_key = #consumer_key
    consumer_secret = #consumer_secret
    access_token = #access_token
    access_secret = #acess_secret
    
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	 
	# this "api" variable is the access point for the majority of operations that the script does
	api = tweepy.API(auth)
	topic = str(sys.argv[1])
	num_tweets = int(sys.argv[2])
	print("Downloading data...\n")

	# Here I execute the search for the last "num_tweets" about the "topic"  
	public_tweets = tweepy.Cursor(api.search, q=topic).items(num_tweets) 

	# Open/Create the file where the datas will be written
	file_to_write = open(topic+"_data_tweets.txt","a")

	# The line below is the header and has to be execute just the first time
	#file_to_write.write('tweetId\ttweetText\tuserId\timageId(s)\timageUrl(s)\tusername\ttimestamp\tlabel \n\n')

	#Here I save the datas of all the tweets that I've collected.
	path_immagini = topic+"_immagini/"
	if not os.path.exists(path_immagini): os.makedirs(path_immagini)
	path_tweets = topic+"_tweets/"
	if not os.path.exists(path_tweets): os.makedirs(path_tweets)

	for tweet in public_tweets:
		tweet_id = ''
		textTweet = ''
		images_id = ''
		user_id = ''
		url_images = ''
		user_name = ''
		timeStamp = ''
		tweet_id = tweet.id_str+tweet_id
		textTweet = tweet.text.replace('\n',' ')+textTweet
		user_id = tweet.user.id_str+user_id
		user_name = tweet.user.name+user_name
		timeStamp = str(tweet.created_at)+timeStamp
		count = 0
		space = ''
		if (str(sys.argv[3]) == "ys"):
			url_tweet = 'https://twitter.com/statuses/'+ tweet_id 
			response = urllib.request.urlopen(url_tweet)
			urllib.request.urlretrieve(url_tweet,path_tweets+tweet_id+'.html')
		
		for media in tweet.entities.get('media',[{}]):
			if media.get('type',None) == 'photo':
				url_image = media.get('media_url')
				image_id = topic+tweet_id+'_' + str(count)
				images_id = images_id + space + image_id
				response = urllib.request.urlopen(url_image)
				urllib.request.urlretrieve(url_image,path_immagini+image_id+'.jpg')
				url_images = url_images + space + url_image
				count += 1
				space = ";"
		file_to_write.write(tweet_id+'\t'+textTweet+'\t'+user_id+'\t'+images_id+'\t'+url_images+'\t'+user_name+'\t'+timeStamp+"\n")

	file_to_write.close()
	print("Downloading finished.\n")



if __name__ == '__main__':
	main()

















