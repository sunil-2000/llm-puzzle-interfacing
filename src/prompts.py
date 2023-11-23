wordle_prompt_gpt4_v = """
You are playing a game of wordle. You will be provided an image of the current wordle state,
and will make an 5-letter word attempt to guess the correct word.

A letter can be in 3 wordle states.
Let "X" = letter not in word, "O" = letter in word but not in correct position,
"V" = letter in word and in correct position.

Let's say that you are given an image where the first row is
"[X][O][X][X][V]" and the word guessed is "[H][E][L][L][O]". 

This indicates that "H" and "L" is not in the word because these characters
are in positions corresponding to "X". "E" is in the word, but not at position 1. "O"
is in the word and at the correct position (position 4).

A good guess might be "CREDO" because it has "O" in the correct position, and "E" in a different position.

Now you will be a given an image of a wordle board. The same rules can be applied
if we let "X" map to a greyed out character, "O" map to a yellow highlighted character, 
"V" map to a green highlighted character.

In the following examples:
Each element of a row is a cell, encloded in brackets, that contains two elements: 
a letter and the letter's wordle state ("GR", "Y", "G") where "GR" = letter is greyed out, 
"Y" = letter is yellow highlighted, "G" = letter is green highlighted.
For example, a cell of [A,GR] = the letter "A" is not in the word. 

For example, if the following image has the first two rows as:

[C,GR][R,GR][A,GR][N,Y][E,Y] 
[M,GR][Y,GR][N,Y][E,Y][Y,Y]
[ ][ ][ ][ ][ ]
[ ][ ][ ][ ][ ]
[ ][ ][ ][ ][ ]

The image is equivalent to the following representation:
[X][X][X][O][O]
[X][X][O][O][X]

and a good next guess should contain "N" at a position that is not 2 or 3,
and "E" at a position that is not 4 or 5. Similarly, the next guess should
not include "C", "R", "A", "M", "O", or "Y".
A good next guess might be "QUEEN".

If the following image is:
[R,Y][A,GR][I,GR][S,GR][E,Y]
[C,GR][L,G][O,GR][U,GR][T,GR]
[N,GR][Y,GR][M,GR][P,GR][H,GR]
[E,G][L,G][V,GR][E,G][R,G]

From this we know that the word must contain "E" at position 0, "L" at position 1,
and "E" at position 3, and "R" at position 4. The word does not contain: 
"A", "I", "S", "C", "O", "U", "T", "N", "Y", "M", "P", "H", "V".
A good next guess might be "ELDER"

If the image contains an empty wordle board, make a 5 letter word guess.

Perform this reasoning for each image, but only respond with a 5 letter word. 
"""

verification_prompt = """"""