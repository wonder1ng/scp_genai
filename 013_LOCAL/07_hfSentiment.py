from transformers import pipeline

sentiment_analyzer = pipeline("sentiment-analysis", 
"distilbert/distilbert-base-uncased-finetuned-sst-2-english")
            # 아키텍쳐-크기-전처리방식-학습방식-데이터셋-언어
result = sentiment_analyzer("I'm hungry")
print(result)
result = sentiment_analyzer("I'm tired")
print(result)
result = sentiment_analyzer(["I'm happy", "I'm unhappy"])
print(result)
print(result[0]["label"])