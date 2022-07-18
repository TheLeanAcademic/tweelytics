from tweelytics.perspectives import CommentAnalyzer
from config import GCP_API_KEY

analyzer = CommentAnalyzer(GCP_API_KEY)

message = 'I love you!'
print(analyzer.get_toxicity(message))
