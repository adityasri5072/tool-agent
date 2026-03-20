#TEST FILE TO SEE IF THE MODEL IS WORKING
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen2.5-1.5B-Instruct"
#creating a model
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

messages = [{"role": "user", "content": "What is the capital of France?"}]
tokenized_chat =tokenizer.apply_chat_template(messages, tokenize=False)
model_input = tokenizer(tokenized_chat,return_tensors="pt")
generated = model.generate(model_input.input_ids, max_new_tokens=200)
decoded = tokenizer.decode(generated[0], skip_special_tokens=True)
print(decoded)