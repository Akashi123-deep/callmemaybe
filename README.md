*This project has been created as part of the 42 curriculum by mel-yazi*

# Description :
Call Me Maybe is an introduction to how AI can use computer functions. Normally, Large Language Models (LLMs) only talk in human text. This project turns everyday human questions into exact, computer-ready code.

Small AI models often make mistakes when trying to write code or JSON. To fix this, our project uses a trick called constrained decoding. Instead of guessing and hoping the AI gets it right, our program checks every single piece (token) the AI writes. This guarantees that the final output is always 100% correct and matches what the functions need.

# Instructions:

## Installation
Clone the project and install all required tools and packages using the Makefile:
** make install **
## Execution
Run the main program using the default settings:
** make run **

You can also run it with custom files by typing:
** uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calling_results.json **

## Checking Code Quality
To check your code for errors using linters and type checkers:
** make lint **

clean up temporary cache folders:
** make clean **

# Rsources:
LLMs from Scratch – Practical Engineering from Base Model to PPO RLHF: https://youtu.be/p3sij8QzONQ?si=-UicV9-8hb8djFdA
uv documentation : https://docs.astral.sh/uv/reference/cli/

## Algorithm explanation:
Step-by-Step How It Works
Getting the AI Ready: The code starts with the prompt you gave the AI and turns it into a list of numbers (tokens) that the computer understands.

Checking the Predictions: The AI looks at all possible next words and gives a score to each one (called a logit).

Testing the Best Guess: The code takes the AI's top choice, adds it to the text so far, and runs it through a special checker.

The Checker's Three Rules:

"Dead end.": If the AI's choice breaks the rule or ruins the format, the code crosses it off the list (gives it a score of negative infinity) so the AI cannot use it. Then it tries the next best choice.

"So far yes.": If the choice is looking good and the sentence is still being built correctly, the code keeps it and moves on to the next word.

"Full.": If the response is completely finished and correct, the code stops the AI from writing anymore.
## Design decisions:
Pydantic for Data Management: Both the response handler and validator use Pydantic (BaseModel) to keep track of variables like token lists, prompt lengths, and stop flags in a clean, organized way.

Smart Partial Regex Checking: Instead of Python's basic regex, it uses a special third-party regex library with a partial=True setting. Because AI writes text piece by piece, the text is almost always unfinished. This partial tool allows the code to look at incomplete text and check if the format still valid
## Performance analysis:
This code is very accurate because it blocks wrong words before they happen, meaning the final JSON format will always be correct, even though the AI might still write a silly number inside it. However, it is quite slow because running a text checker on every single word creates a lot of computer lag compared to professional tools. It is very reliable at keeping the AI on track without letting it chat or mess up.

## Challenges faced:
LLM Hallucination: Even though the algorithm forces the AI to follow the exact JSON layout, it cannot control what the AI thinks. The model might still make up wrong information or incorrect values inside the valid structure.

Complex Regex Syntax: Writing a partial regular expression that can handle every possible stage of an unfinished sentence—like open brackets, optional parameters, and quotes—is very difficult and easy to get wrong.

Slow and Unreliable Hardware: running and testing on CPU make way too slow 