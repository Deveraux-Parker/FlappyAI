Here are example outputs from the following prompt given to a variety of currently frontier models (March 8th, 2024):
PROMPT:
Create a Flappy Bird game in Python. You must include these things:
1. You must use pygame.
2. The background color should be randomly chosen and is a light shade. Start with a light blue color.
3. Pressing SPACE multiple times will accelerate the bird.
4. The bird's shape should be randomly chosen as a square, circle or triangle. The color should be randomly chosen as a dark color.
5. Place on the bottom some land colored as dark brown or yellow chosen randomly.
6. Make a score shown on the top right side. Increment if you pass pipes and don't hit them.
7. Make randomly spaced pipes with enough space. Color them randomly as dark green or light brown or a dark gray shade.
8. When you lose, show the best score. Make the text inside the screen. Pressing q or Esc will quit the game. Restarting is pressing SPACE again.
The final game should be inside a markdown section in Python. Check your code for errors and fix them before the final markdown section.

Included are the resulting .py files. I've named them to make them easy to identify. For example, fbirdqwq32b425bpw.py is flappy bird, QwQ 32b, 4.25bpw, running locally. fbirdcgpt45.py is Chatgpt 4.5's attempt, and so on, and so forth.

I took care to ensure every generation was using the best possible settings and setup. For example, the prompt for QwQ locally was:

<|endoftext|>
<|im_start|>user
Create a Flappy Bird game in Python. You must include these things:
1. You must use pygame.
2. The background color should be randomly chosen and is a light shade. Start with a light blue color.
3. Pressing SPACE multiple times will accelerate the bird.
4. The bird's shape should be randomly chosen as a square, circle or triangle. The color should be randomly chosen as a dark color.
5. Place on the bottom some land colored as dark brown or yellow chosen randomly.
6. Make a score shown on the top right side. Increment if you pass pipes and don't hit them.
7. Make randomly spaced pipes with enough space. Color them randomly as dark green or light brown or a dark gray shade.
8. When you lose, show the best score. Make the text inside the screen. Pressing q or Esc will quit the game. Restarting is pressing SPACE again.
The final game should be inside a markdown section in Python. Check your code for errors and fix them before the final markdown section.<|im_end|>
<|im_start|>assistant
<think>

FIRST SHOT RESULTS:

QwQ running locally
4.25bpw, 32,768 context, q6 kv cache, tabbyAPI, 40 tokens/second
QwQ spent almost 14,000 tokens on its <think> step, then produced the output. The game is functional, looks good, plays smooth. Flight of the bird requires more spamming of space-bar which makes the game a bit more difficult. Everything seems to be well implemented.

ChatGPT 4.5
The game plays well, but the ground is flashing wildly and isn't correct. The bird flight feels good.

ChatGPT O1 Mini High
The game plays well, the bird moves well. Text in the death screen is going off-screen and isn't quite well centered.

ChatGPT O1 Pro
Implementation looks good. The bird requires more spacebar "clicks" to navigate (gravity feels stronger). Fully playable, looks great, follows directions, no apparent issues.

Claude 3.7 Extended Thinking
Looks and feels great. The bird flies in a predictable way that still gives some interesting feedback (going higher than usual if you tap space repeatedly, etc). Probably the best implementation of the group, although QwQ and O1 Pro did fine jobs.

Deepseek R1 (deepthink)
Broken. Pipes are overlapping and the game can't be played properly.

