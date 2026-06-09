from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
# MNLI = Multi-Genre Natural Language Inference

text = "I just upgraded my computer's graphics card"

candidate_labels = ["technology", "sports", "cooking", "politics"]

result = classifier(text, candidate_labels=candidate_labels)

print(f"문장: {text}")
for label, score in zip(result["labels"], result["scores"]):
    print(f"{label:12} {score:.3f}")

print(f"최종 분류: {result["labels"][0]}")

texts = [
    "The football team is using AI software to analyze player performance.",
    "The government is investing heavily in artificial intelligence research.",
    "The restaurant introduced a robot that can cook meals automatically.",
    "The government announced new regulations for professional athletes.",
    "The minister discussed food safety regulations for restaurants.",
    "The government funded a project that uses AI to improve athlete training."
]

for text in texts:
    result = classifier(text, candidate_labels=candidate_labels)
    print("\n" + text)
    for label, score in zip(result["labels"], result["scores"]):
        print(f"{label:12} {score:.4f}")