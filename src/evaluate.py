"""
evaluate.py — Baseline Evaluation on HotPotQA
===============================================

PURPOSE:
    Measure how well your agent performs on real multi-hop questions.
    This gives you a concrete accuracy number for your prompting-only baseline.
    Every future improvement (SFT, RL) gets compared against this number.

WHAT THIS FILE SHOULD DO:
    1. Load questions and ground truth answers from HotPotQA
    2. Run your agent on each question
    3. Compare the agent's final answer to the ground truth
    4. Compute and print accuracy metrics
    5. Save results to experiments/ for later comparison

DATA SOURCE:
    HotPotQA via HuggingFace datasets library
    - Load with: from datasets import load_dataset
    - dataset = load_dataset("hotpot_qa", "distractor")
    - Each example has:
        "question": the question string
        "answer": the ground truth answer string
    - Use the "validation" split for evaluation

IMPLEMENTATION CHECKLIST:
    [x ] Import load_dataset from datasets
    [x ] Import your agent_loop from agent.py
        - You'll need to MODIFY agent_loop to RETURN the final answer as a string
          instead of just printing it. Add a return statement in the finish branch.
          Keep the prints for debugging but also return the answer.
    [x ] Load HotPotQA validation split
    [ x] Select a small subset to start (first 20 questions)
    [ x] For each question:
        a. Run agent_loop(question)
        b. Get the agent's answer
        c. Compare to ground truth
        d. Track if it was correct
    [ x] Scoring method — use simple string matching to start:
        - Lowercase both the agent answer and ground truth
        - Check if the ground truth appears IN the agent's answer
          (e.g., ground truth "Paris" should match agent answer
          "The capital of France is Paris")
        - This is called "answer containment" — not perfect but good enough
          for a baseline. You can add F1 token overlap scoring later.
    [ x] Print results:
        - Total questions
        - Number correct
        - Accuracy percentage
        - List of wrong answers with the question, expected answer, and agent answer
    [ ] Save results to a JSON file in experiments/

IMPORTANT CHANGES NEEDED IN agent.py:
    Your current agent_loop() prints the answer but doesn't return it.
    Modify it so it returns the final answer string. Something like:
    - In the finish branch: return action[1]
    - If the loop ends without finishing: return None
    - If parse fails: return None
    This way evaluate.py can capture the answer programmatically.

THINGS TO WATCH FOR:
    - This will be SLOW on CPU. 20 questions × ~3 search steps × 30-60 sec
      per generation = potentially 30-60 minutes. That's fine for a baseline run.
      Start with 5 questions to verify everything works, then scale to 20.
    - Some questions will timeout (agent loops 6 times without finishing).
      Count these as wrong.
    - The accuracy will likely be low (maybe 20-40%). That's expected and GOOD —
      it gives you room to show improvement with SFT and RL.
    - Save the full traces (question + reasoning chain + answer) not just the
      score. You'll want these for qualitative analysis in your README.

NOTES:
    - Run with: python src/evaluate.py
    - Start with 5 questions, verify it works, then do 20
    - Commit the results file to experiments/
    - This same script will be reused to evaluate your SFT and RL models later
"""
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