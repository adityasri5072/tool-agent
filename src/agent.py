"""
agent.py — The ReAct Agent Loop
================================

PURPOSE:
    This is the main file that ties everything together. It loads the LLM,
    gives it a question, and runs the Thought → Action → Observation loop
    until the agent produces a final answer.

    This is the prompting-only baseline — no RL, no fine-tuning. The agent's
    behavior comes entirely from the system prompt you wrote in prompts.py.
    The performance of this baseline is what you'll later try to beat with RL.

HOW THE LOOP WORKS:
    1. Build the initial context: system prompt + user question
    2. Feed it to the model and generate output
    3. Parse the output:
       - If the model called finish() → extract the answer, we're done
       - If the model called search() → extract the query, run the search,
         append the Observation to the context
    4. Feed the updated context back to the model
    5. Repeat from step 2 (set a max of ~6 loops to prevent infinite cycling)

IMPLEMENTATION CHECKLIST:
    [ ] Import the model/tokenizer loading logic (reuse from test_model.py)
    [ ] Import tools from tools.py and SYSTEM_PROMPT from prompts.py
    [ ] Write a parse_action() function:
        - Takes the model's generated text
        - Extracts the tool name and argument from the Action line
        - Returns (tool_name, argument) tuple
        - Handle edge cases: what if the model doesn't follow the format?
    [ ] Write the main agent loop:
        - Initialize messages list with system prompt and user question
        - Loop (max ~6 iterations):
            a. Format messages with apply_chat_template
            b. Tokenize and generate
            c. Decode the new tokens only (not the whole context)
            d. Parse the output for an Action
            e. If finish → print answer and break
            f. If search → execute tool, append Observation to messages
            g. If unparseable → handle gracefully (retry or break)
    [ ] Test with a simple question first: "What is the capital of France?"
    [ ] Then test with a multi-hop question: "Who directed Inception and
        what year were they born?"
    [ ] Print the full reasoning trace so you can see Thought/Action/Observation
        at each step

THINGS THAT WILL GO WRONG (and that's fine):
    - The model might generate the Observation itself instead of waiting for you
      → Fix in your prompt (prompts.py)
    - The model might not follow your Action format exactly
      → Make your parser more flexible, or improve the prompt
    - The model might loop forever without calling finish
      → That's why you have a max iteration count
    - Search results might confuse the model
      → Try returning fewer/shorter results in tools.py
    These failure modes are EXPECTED. Document them — they become your motivation
    for why RL training is needed.

NOTES:
    - This will be slow on CPU (~30-60 sec per generation step). That's fine.
    - Print everything at each step so you can debug the agent's reasoning
    - Save a few example traces (question + full reasoning chain + final answer)
      in experiments/ — you'll compare these against the RL-trained agent later
    - The quality of this baseline depends heavily on your prompt in prompts.py
      Expect to iterate on the prompt multiple times
"""