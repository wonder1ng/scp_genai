from transformers import BertTokenizer, BertForSequenceClassification
import torch

model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

text = "이 영화 정말 재미 있었어요."

inputs = tokenizer(text, return_tensors="pt", trucation=True, padding=True)

with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = logits.argmax().item()

print(f"예측된 감정 점수: {predicted_class + 1}")

texts = ["이 식당 너무 별로였어요", "여기 서비스 정말 최고예요!", "그냥 먹을만하네요"]

inputs = tokenizer(texts, return_tensors="pt", trucation=True, padding=True)

with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = logits.argmax().item()
    predictions = torch.argmax(logits, dim=1)

for text, pred in zip(texts, predictions):
    print(f"예측 문장: {text} -> 예측된 감정 점수: {pred.item() + 1}")