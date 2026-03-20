"""
prompts.py — System Prompt and Templates for the ReAct Agent
============================================================

PURPOSE:
    Define the system prompt that tells the LLM how to behave as a ReAct agent.
    This is the most important file for the prompting-only baseline. The model's
    entire behavior — whether it uses tools correctly, formats outputs parsably,
    and reasons well — depends on how well this prompt is written.

WHAT THE SYSTEM PROMPT MUST CONTAIN:
    1. A role description: "You are a research agent that answers questions
       by searching for information and reasoning step by step."
    2. A list of available tools with descriptions:
       - search(query): searches the web and returns results
       - finish(answer): returns your final answer
    3. The EXACT format the model should use for each step:
       Thought: <the model's reasoning about what to do next>
       Action: <tool_name>("argument")
       Observation: <this gets filled in by the system, not the model>
       ... (repeat as needed)
       Thought: I now have enough information.
       Action: finish("the final answer")
    4. One complete example showing the full cycle with a sample question
    5. Rules:
       - Always start with a Thought before every Action
       - Only use the listed tools
       - Keep search queries short and specific
       - Call finish() when you have the answer

IMPLEMENTATION CHECKLIST:
    [ ] Write the SYSTEM_PROMPT as a single multi-line string
    [ ] Include the role description
    [ ] List the tools with clear descriptions of what each does
    [ ] Define the Thought/Action/Observation format EXACTLY
    [ ] Write one complete worked example (pick a simple multi-hop question)
    [ ] Add rules/constraints for the model to follow
    [ ] Make sure the format you choose is something you can parse with Python
        string operations in agent.py (think about this carefully!)

DESIGN DECISIONS TO THINK ABOUT:
    - What delimiters will you use for tool calls? Some options:
      Action: search("query")       — function call style
      Action: [search] query        — bracket style
      Action: <tool>search</tool>   — XML style
      Pick one that's easy to parse with Python. Consider: what happens if the
      model doesn't follow the format exactly? How robust is your parsing?

NOTES:
    - The example in the prompt is critical — the model will mimic it closely
    - If the model keeps generating Observations instead of stopping for you
      to fill them in, your prompt needs clearer instructions about this
    - You may need to iterate on this prompt several times — that's normal
    - Keep it as short as possible while being unambiguous
"""