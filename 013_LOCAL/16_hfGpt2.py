from transformers import pipeline, AutoTokenizer

model_name = "gpt2"

text_generator = pipeline("text-generation", model=model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

result = text_generator(
    "Once upon a time, ", 
    max_length=30, 
    truncation=True, 
    pad_token_id=tokenizer.eos_token_id
    )[0]

print(result["generated_text"])