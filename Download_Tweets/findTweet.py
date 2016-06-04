'''
This script find the last tweet of a specified user which has
a particular image (url_image needed)

USAGE: 

$ python3.5 findTweet.py "@user" "http://..." ""

It saves in a appropriate directory the image and the datas in a file .txt
the most important information about the tweet.
NOTE: the head of the file.txt has to be written the first time (read the code)
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
    my_user = str(sys.argv[1])
    my_image_url = str(sys.argv[2])
    topic = 'Topic_name'
    
    # Take the last 4000 twitters from the account 

    new_tweets = api.user_timeline(screen_name = my_user,count=4000,include_rts=True)

    file_to_write = open(topic+"_tweets.txt", "a")

    # The line below is the header and has to be execute just the first time
    #file_to_write.write('tweetId\ttweetText\tuserId\timageId(s)\timageUrl(s)\tusername\ttimestamp(+0000)\tlabel \n\n')

    # Create the path
    path_immagini = topic+"_images/"
    if not os.path.exists(path_immagini): os.makedirs(path_immagini)

        # Search for the tweet that contains the image with the link at the input, save the image and all the datas.
    found = 0
    for tweet in new_tweets:
        if found == 0:
            for my_media in tweet.entities.get('media', [{}]):
                if my_media.get('type', None) == 'photo':
                    if my_media.get('media_url') == my_image_url:
                        found = 1
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
                        for media in tweet.entities.get('media',[{}]):
                                if media.get('type',None) == 'photo':
                                        url_image = media.get('media_url')
                                        image_id = topic+tweet_id+'_'+str(count)
                                        images_id = images_id + space + image_id
                                        response = urllib.request.urlopen(url_image)
                                        urllib.request.urlretrieve(url_image,path_immagini+image_id+'.jpg')
                                        url_images = url_images + space +url_image
                                        count += 1
                                        space = ";"
                        file_to_write.write(tweet_id+'\t'+textTweet+'\t'+user_id+'\t'+images_id+'\t'+url_images+'\t'+user_name+'\t'+timeStamp+'\t'+"\n")

    file_to_write.close()

if __name__ == '__main__':
    main()





