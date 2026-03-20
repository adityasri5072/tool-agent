from datasets import load_dataset
from agent import agent_loop


if __name__ == "__main__":
    dataset = load_dataset("hotpot_qa", "distractor", split="validation")
    count = 0
    for i in range(5):
        question = dataset[i]['question']
        truth = dataset[i]['answer']
        answer =agent_loop(question)
        if answer is not None and truth.lower() in answer.lower():
            print("Correct")
            print(f"\nQ{i + 1}: {question}")
            print(f"Expected: {truth}")
            print(f"Agent said: {answer}")
            count += 1
    print(f"\nResults: {count}/{20} correct ({count/20*100:.1f}%)")