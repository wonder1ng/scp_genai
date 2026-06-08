from transformers import pipeline

sentiment_analyzer = pipeline("sentiment-analysis", "distilbert/distilbert-base-uncased-finetuned-sst-2-english")
# 아키텍쳐
result = sentiment_analyzer("I'm hungry")
print(result)