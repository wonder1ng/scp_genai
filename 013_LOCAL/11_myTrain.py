import numpy as np, os
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
from datasets import Dataset


train_data = {
    "text": [
        "I love this!",
        "This is terrible!",
        "I am happy",
        "I am sad",
        "This product is amazing",
        "Worst experience ever.",
        "Absolutely fantastic",
        "I hate it.",
        "The service was excellent",
        "The food was awful",
        "I really enjoyed it",
        "I regret buying this",
        "Highly recommended",
        "Not worth the money",
        "Everything was perfect",
        "Very disappointing",
        "I am extremely satisfied",
        "The quality is poor",
        "Best purchase I've made",
        "This made my day",
        "I can't stand this",
        "Amazing customer support",
        "The delivery was late and bad",
        "I feel great",
        "This is the worst product",
        "Outstanding performance",
        "Terrible customer service",
        "I would buy it again",
        "Completely useless",
        "Five stars",
        "One of the best experiences",
        "It broke after one day",
        "Very happy with the results",
        "I am frustrated",
        "Excellent value for money"
    ],
    "label": [
        1, 0, 1, 0, 1, 0, 1, 0,
        1, 0, 1, 0, 1, 0, 1, 0,
        1, 0, 1, 1, 0, 1, 0, 1,
        0, 1, 0, 1, 0, 1, 1, 0,
        1, 0, 1
    ]
}

eval_data = {
    "text": [
        "I am delighted",
        "This is horrible",
        "Very impressive",
        "I am unhappy",
        "The product exceeded expectations",
        "Waste of time",
        "Great quality",
        "The experience was bad",
        "I absolutely love it",
        "Not satisfied at all",
        "Fantastic work",
        "I will never use this again",
        "Superb experience",
        "This was a mistake",
        "Pretty good overall"
    ],
    "label": [
        1, 0, 1, 0, 1,
        0, 1, 0, 1, 0,
        1, 0, 1, 0, 1
    ]
}
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

def tokenize(batch):
    return tokenizer(batch["text"], padding="max_length", truncation=True)

train_ds = Dataset.from_dict(train_data).map(tokenize, batched=True)
eval_ds = Dataset.from_dict(eval_data).map(tokenize, batched=True)

model = AutoModelForSequenceClassification.from_pretrained(
    model_name, num_labels=2,
    id2label={0: "NEGATIVE", 1: "POSITIVE"},
    label2id={"NEGATIVE": 0, "POSITIVE": 1}
)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    return {"accuracy": float((preds == labels).mean())}

def full_path(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), filename)

args = TrainingArguments(
    output_dir=full_path("results"),
    eval_strategy="epoch",
    save_strategy="epoch",
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=3,
    logging_steps=1
)

trainer = Trainer(
    model=model, args=args,
    train_dataset=train_ds, eval_dataset=eval_ds,
    compute_metrics=compute_metrics
)

trainer.train()
print("평가 결과:", trainer.evaluate())

save_path = full_path("my_local_model")

# 모델 저장
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)

print(f"내 모델 저장 완료: {save_path}")