# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start
  (for example: "the secret number kept changing" or "the hints were backwards").
number kept changing
kept saying lower on the guesses but it was 98 should have gave me hint to go higher instad
also when you change the game modes normal has the most attempts instead of easy so the difficulty was out of order for the modes
and the range is off 1 to 100 should be for hard mode
the game never resets after you click new game
ok so this game is broken the secret number changes every time you click submit the difficulty modes are not correct easy should have most attempts and lowest range compared to normal and hard modes also the hints are opposite it told me to guess lower but the answer ended up being higher when you finish the game and click new game it never resets
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- I used claude in visual studio code
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- 1. Secret number changing on Submit (lines 153-155)

The original code alternated between passing int and str versions of the secret to check_guess on every other attempt. This caused string-based comparisons ("9" > "10" = True) which made hints unpredictable and made it look like the secret was changing.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  I did not have a misleading suggestion I verified by rerunning the game and testing each feature that there was initially a bug with.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - I just manually verified that the feature was properly functioning.
- Describe at least one test you ran (manual or using pytest)
  - for the manual test it was updating correctly based on guess it would change it guess higher even though my guess was lower so I changed the code to this so that if my guess was higher but the secret was lower it would actually tell me to guess lower instead of higher
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?
  - No I did not really use AI for testing

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
  - The original code was passing both an int and a str version of the secret number to check_guess on alternating attempts. Because Python compares strings differently than numbers ("9" > "10" evaluates to True), the hints were unpredictable and it felt like the number itself was changing every time you clicked submit.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  - Streamlit app, clicking a button, typing in a box. The entire Python script reruns from the top. That means any regular variable gets reset to its starting value. Session state (st.session_state) is like a notepad that persists across those reruns, so you can store things like the secret number and have it stay the same across clicks.
- What change did you make that finally gave the game a stable secret number?
  - Storing the secret number in st.session_state once (only when it doesn't already exist) so Streamlit's reruns can't overwrite it with a new random number on every interaction.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - Manually testing each feature in isolation after a fix rather than assuming a change worked so I can confirm the specific behavior changed and didn't break something else.
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
  - I think I would use to write automated tests as well as use it more to explain why it approached a patch the way it did.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  AI-generated code can look correct at a glance but hide subtle logic bugs, so I can't treat it as a finished product I still need to run it and think critically about edge cases myself.
