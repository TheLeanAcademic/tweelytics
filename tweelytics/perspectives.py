from time import sleep
from googleapiclient import discovery

class CommentAnalyzer:
    def __init__(self, api_key):
        self.client = discovery.build(
                        "commentanalyzer",
                        "v1alpha1",
                        developerKey=api_key,
                        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
                        static_discovery=False,
                        )

    # Can extend to support passing of parameters
    def get_toxicity(self, message):
        if(message):
            sleep(0.001)
            analyze_request = {
          		'comment': { 'text': message },
          		'requestedAttributes': {'TOXICITY': {}},
                'languages': ['en'],
                }
            response = self.client.comments().analyze(body=analyze_request).execute()
            score = response['attributeScores']['TOXICITY']['summaryScore']['value']
            return(score)
        else:
            return(0.0)


    # Can extend to 'get perspectives'
    def get_tweet_toxicity(self, tweet):
        tweet['toxicity'] = self.get_toxicity(tweet['text'])
        return(tweet)

    #def get_conversation_toxicity(self, conversation):
    #    return(get_tweet_toxicity(tweet) for tweet in conv['replies'])
