# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

  Expectation :  I expect to make guesses and use the hints to guide me through the numbers. If/When I get a number wrong, I would like to try again, I also I expect to see my score. 

  bug 1 - hints are buggy, they do not point to the correct direction
  bug 2 - new game button does not let me star a new game
  bug 3 - can't see how the score is being computed, but might need to look into it, as of now there are not guarantees of this functionality
  bug 4 - it also takes floats but it shouldn't

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

I used Claude.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

Claude identified that the hints were swapped in the try block and explained that guess > secret means the guess is too high so the hint should say "Go LOWER!" not "Go HIGHER!". I verified it by playing the game after the fix and confirming the hints pointed me in the right direction.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

Claude ran pytest from its own environment and reported all 14 tests passing, but when I ran it myself I got a ModuleNotFoundError for logic_utils. The tests weren't actually passing in my environment until Claude added the empty conftest.py file. I caught this by running the tests myself rather than trusting the output Claude reported.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I decided a bug was fixed by testing it manually in the running app and checking that the behavior matched my expectation. 

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
For the hints bug, I guessed a number I knew was too high and confirmed the message said "Go LOWER!". For testing with pytest, I ran pytest tests/ -v which ran 14 tests covering check_guess, parse_guess, and update_score. 

- Did AI help you design or understand any tests? How?
Claude helped me understand the test structure — specifically that functions returning tuples need to be unpacked (outcome, _ = check_guess(...)) before asserting on individual values.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.

The secret number kept changing because Streamlit reruns the entire script from top to bottom every time any interaction happens (a button click, a text input, anything).

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit reruns are like refreshing a page, the code runs again completely. session_state is a dictionary that survives those reruns, so values stored in it persist.


- What change did you make that finally gave the game a stable secret number?

The fix was wrapping the secret generation in if "secret" not in st.session_state, so it only runs once on the very first load.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

Asking the AI to explain what it's about to do before approving the change. Early on I approved changes without fully understanding them, but when I started asking for explanations first I caught things I would have missed.

- What is one thing you would do differently next time you work with AI on a coding task?
Run every command and test myself immediately rather than trusting the AI's reported output. Claude said the tests passed before I had a working setup, running it myself revealed the error right away.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

AI-generated code can look correct at first glance but contain subtle bugs that require actual understanding to catch, not just reading. Trusting AI output without verifying it is the same mistake as trusting any unreviewed code.
