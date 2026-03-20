from tools import TOOLS
from prompts import SYSTEM_PROMPT
from transformers import AutoTokenizer, AutoModelForCausalLM

#Load Model and Tokenizer
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")

def parse_action(generated_text):
    generated_text = generated_text.split("\n")
    for line in generated_text:
        if line.startswith("Action:"):
            after_action = line.split("Action: ")[1]
            tool_name = after_action.split("(")[0]
            argument = after_action.split("(")[1].split(")")[0].strip('"')
            return tool_name, argument
    return None, None
def agent_loop(question):
    messages = [{"role": "system", "content": f"{SYSTEM_PROMPT}"},
                {"role": "user", "content": question}]
    for i in range(6):
        tokenized_chat = tokenizer.apply_chat_template(messages, tokenize=False)
        model_input = tokenizer([tokenized_chat],return_tensors='pt')
        generated = model.generate(model_input.input_ids, max_new_tokens=200)
        new_tokens = generated[0][model_input.input_ids.shape[1]:]
        decoded = tokenizer.decode(new_tokens, skip_special_tokens=True)
        lines = decoded.split("\n")
        kept = []
        for line in lines:
            kept.append(line)
            if line.startswith("Action:"):
                break
        decoded = "\n".join(kept)
        print(decoded)
        action = parse_action(decoded)
        print(f"DEBUG raw output: {repr(decoded)}")
        if action[0] is None:
            print("Invalid Action: ", decoded)
            break
        if action[0] == "finish":
            print(f"Final Answer: {action[1]}")
            return action[1]
        if action[0] == "search":
            tool_name, argument = action
            result = TOOLS[tool_name](argument)
            messages.append({"role": "assistant", "content": decoded})
            messages.append({"role": "user", "content": f"Observation: {result}"})
    return None
if __name__ == "__main__":
    question = "Was the director of Inception born before or after the founding of Sony?"
    agent_loop(question)
