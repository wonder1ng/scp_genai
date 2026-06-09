import os
from transformers import pipeline

def full_path(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), filename)

MODEL_DIR = full_path("my_local_model")

classifier = pipeline("sentiment-analysis", model=MODEL_DIR, tokenizer=MODEL_DIR)

test_sentences = [
    "I love using my own AI model!",
    "This is the worst experience ever.",
    "This is the best experience ever.",
    "I feel so bad..."
]

for text in test_sentences:
    r = classifier(text)[0]
    print(r)
    print(f"문장: {text}, 결과: {r['label']}, 점수: {r['score']:.3f}")