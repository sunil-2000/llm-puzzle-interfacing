wordle_prompt = """
You are playing a game of wordle. You will be provided an image of the current wordle state,
and will make an 5-letter word attempt to guess the correct word.

Let "X" = letter not in word, "O" = letter in word but not in correct position,
"V" = letter in word and in correct position.

Let's say that you are given an image where the first row is
"XOXXV" and the word guess is "HELLO". 

This indicates that "H" and "L" is not in the word because these characters
are in positions corresponding to "X". "E" is in the word, but not at position 1. "O"
is in the word and at the correct position (position 4).

A good guess might be "CREDO" because it has "O" in the correct position, and "E" in a different position.

Now you will play wordle, but will be a given an image of the board. The same rules can be applied
if we let "X" map to a greyed out character, "O" map to a yellow highlighted character, 
"V" map to a green highlighted character.

To make a guess peform the following reasoning on the given image of a wordle board. 
This will require the following reasoning:
1. Analyze the board and recognize which characters are not in the word ("X"), which characters
are in the word but incorrect position ("O"), and which characters are in the correct position ("V").
2. Make an educated guess such that the guessed word contains characters that are already in the 
correct position ("V"), contains characters that are in the word but at different positions from previous
attempts ("O"), and does not contain characters that are not in the word ("X").

Perform this reasoning for each image, but only respond with a 5 letter word. 
"""

verification_prompt = """"""