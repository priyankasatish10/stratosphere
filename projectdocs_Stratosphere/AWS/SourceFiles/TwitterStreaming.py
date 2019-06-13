import boto3
import random
import time
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import re
import datetime
import sys


#This is the super secret information
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""
aws_key_id =  ""
aws_key = ""
DeliveryStreamName = 'TwitterStreaming'
client = boto3.client('firehose', region_name='us-east-1',
                          aws_access_key_id=aws_key_id,
                          aws_secret_access_key=aws_key
                          )
num_tweets=0

class PreProcessor:
    def clean_data(self,text):


        #removing hashtags
        newtext= re.sub(r'#\w*','',text);
        #removing urls
        newtext= re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))','',newtext);
        #removing mentions
        newtext= re.sub(r'@\w*','',newtext);
        #removing emojis
        newtext=re.sub(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])' , '',newtext);
        #removing smileys
        newtext=re.sub(r"(?:X|:|;|=)(?:-)?(?:\)|\(|O|D|P|S){1,}",'',newtext);
        #removing numbers
        newtext=re.sub(r"(^|\s)(\-?\d+(?:\.\d)*|\d+)",'',newtext);
        #removing resreved words
        newtext=re.sub(r'^(RT|FAV)','',newtext);

        newtext = re.sub(r':', '', newtext);
        # replace consecutive non-ASCII characters with a space
        newtext = re.sub(r'[^\x00-\x7F]+', ' ', newtext);

        return newtext
#This is a basic listener that just prints received tweets and put them into the stream.
class StdOutListener(StreamListener):

    def on_data(self, data):


       global num_tweets
       global numberofTweets

       if(num_tweets>=numberofTweets):
          sys.exit()



       p=PreProcessor();
       twitter_data = json.loads(data);
       text=twitter_data["text"];


       if 'extended_tweet' in twitter_data:
           text = twitter_data['extended_tweet']['full_text'];

       cleantext=p.clean_data(text);

       created_at=twitter_data["created_at"];


       created_date = datetime.datetime.strptime(created_at, '%a %b %d %H:%M:%S %z %Y').date();
       created_date_text=created_date.strftime("%m/%d/%Y");

       if twitter_data["place"] is not None:
           location = (twitter_data["place"]["country"]);
       else:
           location = "Unknown";




       data={"created_at":created_date_text,"text":cleantext,"location":location}



       client.put_record(DeliveryStreamName=DeliveryStreamName, Record={'Data':json.dumps(data)})

       num_tweets+=1

       print(str(num_tweets) + cleantext);

       return True

    def on_error(self, status):
        print (status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    keyword = input("Please enter keyword to search tweets: ");
    numberofTweets=int(input("Please enter number of tweets to be searched: "));
    stream = Stream(auth, l)
    stream.filter(track=[keyword],languages=["en"])
