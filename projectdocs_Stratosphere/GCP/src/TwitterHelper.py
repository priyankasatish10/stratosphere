import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import twitter

from google.cloud import pubsub_v1
# Code to publish tweets to pubsub


project_id = "prianalyze"
topic_name = "filtertweets"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)


def callback(message_future):
    # When timeout is unspecified, the exception method waits indefinitely.
    if message_future.exception(timeout=30):
        print('Publishing message on {} threw an Exception {}.'.format(
            topic_name, message_future.exception()))
    else:
        print('result=' + message_future.result())


def publish_to_pubsub(tweet):
    # Data must be a byte string
    tweet = tweet.encode('utf-8')
    # When you publish a message, the client returns a Future.
    message_future = publisher.publish(topic_path, data=tweet)
    message_future.add_done_callback(callback)


# We must keep the main thread from exiting to allow it to process
# messages in the background.


#######################################################################

# Below code is to read tweets from twitter api


class StdOutListener(StreamListener):
    def on_data(self, data):
        twitter_data = json.loads(data)
        twitter_text = twitter_data['text']
        if 'extended_tweet' in twitter_data:
            twitter_text = twitter_data['extended_tweet']['full_text']
        print(twitter_text)
        publish_to_pubsub(twitter_text)

        return True

    def on_error(self, status):
        print('error:' + status)


def tweets_getter():

    TWITTER_APP_KEY = ''
    TWITTER_APP_SECRET_KEY = ''
    TWITTER_ACCESS_TOKEN = ''
    TWITTER_TOKEN_SECRET = ''
    # api = twitter.Api(consumer_key=TWITTER_APP_KEY, consumer_secret=TWITTER_APP_SECRET_KEY,
    #                  access_token_key=TWITTER_ACCESS_TOKEN, access_token_secret=TWITTER_TOKEN_SECRET,
    #                  tweet_mode='extended')
    twitter_listener = StdOutListener()
    auth = OAuthHandler(TWITTER_APP_KEY, TWITTER_APP_SECRET_KEY)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_TOKEN_SECRET)
    stream = Stream(auth, twitter_listener, tweet_mode='extended')
    stream.filter(track=['#AvengersEndGame'], languages=["en"])


if __name__ == '__main__':
    tweets_getter()
