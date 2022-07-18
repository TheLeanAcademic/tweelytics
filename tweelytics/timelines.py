import json
import tweepy
import time

from tweelytics.perspectives import CommentAnalyzer
from config import GCP_API_KEY



class Timeline:
    def __init__(self, bearer_token):
        self.client = tweepy.Client(bearer_token=bearer_token)
        self.user_id = ''

    def get_users_topK_toxic_conversations(self, username):
        """
        Gets conversations

        """
        # Get conversations
        conversations = self.get_users_topK_conversations(username)

        # Create comment analyzer
        analyzer = CommentAnalyzer(GCP_API_KEY)

        #for
        #for conversation in conversations:
        #    for tweet in conversation['replies']:
        #        print(tweet)

        conversations = [[analyzer.get_tweet_toxicity(tweet) for tweet in conv['replies']] for conv in conversations]

        print(json.dumps(conversations, indent=4))

    def get_users_topK_conversations(self, username):
        """
        Gets the top-K conversations sorted by some criteria
        PARAMETERS:
        - sort_func: a function for sorting the conversations
        """

        kwargs = {
            'exclude' : 'retweets',
            'tweet_fields' : ['id','text','public_metrics'],
            'max_results' : 5,
        }

        # Truncate the timeline
        timeline_max_len = 5

        users_timeline = self.get_users_timeline(username, kwargs, timeline_max_len)

        # Move "up"
        sort_func = lambda d: d['public_metrics']['reply_count']

        sorted_tweets = sorted(users_timeline, key=sort_func, reverse=True)

        # Move "up"
        topK = 1

        # Store them in a sensible way!!!
        return([self.get_tweet_replies(tweet) for tweet in sorted_tweets[:topK]])


    def get_tweet_replies(self, tweet):
        # Get the conversation ID of a tweet
        conversation_id = tweet['id']

        # Use the conversation_id to create the query
        query = f'conversation_id:{conversation_id}'

        # Max number of replies per conversation
        replies_max_num = 10

        # Get the conversation
        tweet['replies'] = [tweet.data for tweet in
                        tweepy.Paginator(self.client.search_all_tweets,
                        query=query, tweet_fields=['id','text','conversation_id','public_metrics'],
                        max_results=10).flatten(limit=replies_max_num)]

        # Full-archive (search_all_tweets) has a 1 request / 1 second limit
        time.sleep(1)
        return(tweet)

    def get_users_timeline(self, username, kwargs, limit):

        # Get user_id from username
        kwargs['id'] = self.client.get_user(username=username, user_fields=['id']).data.id


        # Setup Paginator arguments (https://docs.tweepy.org/en/latest/v2_pagination.html)
        method = self.client.get_users_tweets

        # Get timeline (without retweets) (CAN MAKE THIS A PARAM)
        users_timeline = [tweet.data for tweet in
                        tweepy.Paginator(method,**kwargs).flatten(limit=limit)]

        return(users_timeline)
