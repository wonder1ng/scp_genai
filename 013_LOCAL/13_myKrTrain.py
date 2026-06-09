import numpy as np, os
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
from datasets import Dataset

train_data = {
    "text": [
        "이게 정말 좋아요!",
        "이건 정말 끔찍해요!",
        "저는 행복해요",
        "저는 슬퍼요",
        "이 제품은 정말 훌륭해요",
        "최악의 경험이었어요.",
        "정말 환상적이에요",
        "정말 싫어요.",
        "서비스가 훌륭했어요",
        "음식이 형편없었어요",
        "정말 즐거웠어요",
        "이걸 산 것을 후회해요",
        "강력 추천합니다",
        "가격 대비 가치가 없어요",
        "모든 것이 완벽했어요",
        "매우 실망스러웠어요",
        "정말 만족합니다",
        "품질이 좋지 않아요",
        "지금까지 한 최고의 구매였어요",
        "덕분에 기분이 좋아졌어요",
        "정말 참을 수 없어요",
        "고객 지원이 훌륭했어요",
        "배송이 늦고 별로였어요",
        "기분이 정말 좋아요",
        "이건 최악의 제품이에요",
        "성능이 뛰어나요",
        "고객 서비스가 끔찍해요",
        "다시 구매할 의향이 있어요",
        "완전히 쓸모없어요",
        "별 다섯 개입니다",
        "최고의 경험 중 하나였어요",
        "하루 만에 고장 났어요",
        "결과에 매우 만족해요",
        "정말 답답해요",
        "가격 대비 훌륭한 가치가 있어요"
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
        "정말 기뻐요",
        "이건 끔찍해요",
        "매우 인상적이에요",
        "저는 불행해요",
        "이 제품은 기대 이상이었어요",
        "시간 낭비였어요",
        "품질이 훌륭해요",
        "경험이 좋지 않았어요",
        "정말 마음에 들어요",
        "전혀 만족스럽지 않아요",
        "훌륭한 작업이에요",
        "다시는 이걸 사용하지 않을 거예요",
        "최고의 경험이었어요",
        "이건 실수였어요",
        "전반적으로 꽤 좋아요"
    ],
    "label": [
        1, 0, 1, 0, 1,
        0, 1, 0, 1, 0,
        1, 0, 1, 0, 1
    ]
}

model_name = "beomi/kcbert-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)

def tokenize(batch):
    return tokenizer(batch["text"], padding="max_length", truncation=True)

train_ds = Dataset.from_dict(train_data).map(tokenize, batched=True)
eval_ds = Dataset.from_dict(eval_data).map(tokenize, batched=True)

model = AutoModelForSequenceClassification.from_pretrained(
    model_name, num_labels=2,
    id2label={0: "부정", 1: "긍정"},
    label2id={"부정": 0, "긍정": 1}
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

save_path = full_path("my_local_kr_model")

model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)

print(f"내 모델 저장 완료: {save_path}")