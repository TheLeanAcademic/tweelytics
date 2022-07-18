from tweelytics.timelines import Timeline
from config import TWITTER_BEARER_TOKEN
import json


timeline = Timeline(TWITTER_BEARER_TOKEN)

timeline.get_users_topK_toxic_conversations('BBCNews')
