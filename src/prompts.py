from typing import List

# **************************Wordle**********************************************

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


def wordle_prompt_gpt4(wordle_boards: List[str], guesses: List[str]) -> str:
    return """
  You are playing wordle. The goal is to guess the correct 5 letter english word. 
  
  If a row is a previously guessed word, each cell is defined as tuple, (letter, letter state) 
  where letter is the letter in that word at the position, and letter state can 
  be one of three values: "X", "O", "V".
  "X" means the letter is not in the word, "O" means the letter is in the word but not at the correct position,
  "V" means the letter is in the word and at the correct position. A letter can occur multiple times in a word.

  If the row is a blank row, the cell will be empty and indicated by (-,-).
  
  Example 1:
  [[('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')]]
  guess: "HELLO"
  
  [[('H', 'X'), ('E', 'O'), ('L', 'X'), ('L', 'X'), ('O', 'X')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')]]
  guess: "NUKES"
  
  [[('H', 'X'), ('E', 'O'), ('L', 'X'), ('L', 'X'), ('O', 'X')],
  [('N', 'O'), ('U', 'V'), ('K', 'X'), ('E', 'V'), ('S', 'X')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')]]
  guess: "QUEEN"

  [[('H', 'X'), ('E', 'O'), ('L', 'X'), ('L', 'X'), ('O', 'X')],
  [('N', 'O'), ('U', 'V'), ('K', 'X'), ('E', 'V'), ('S', 'X')],
  [('Q', 'V'), ('U', 'V'), ('E', 'V'), ('E', 'V'), ('N', 'V')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')]]
  QUEEN was the correct word!

  Example 2:
  [[('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')]]
  guess: "STRAP"

  [[('S', 'X'), ('T', 'X'), ('R', 'X'), ('A', 'V'), ('P', 'X')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')]]
  guess: "GLEAM"
  
  [[('S', 'X'), ('T', 'X'), ('R', 'X'), ('A', 'V'), ('P', 'X')],
  [('G', 'O'), ('L', 'O'), ('E', 'X'), ('A', 'V'), ('M', 'X')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')]]
  guess: "LOCAL"

  [[('S', 'X'), ('T', 'X'), ('R', 'X'), ('A', 'V'), ('P', 'X')],
  [('G', 'O'), ('L', 'O'), ('E', 'X'), ('A', 'V'), ('M', 'X')],
  [('L', 'X'), ('O', 'X'), ('C', 'X'), ('A', 'V'), ('L', 'V')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')]]
  guess: "BANAL"

  [[('S', 'X'), ('T', 'X'), ('R', 'X'), ('A', 'V'), ('P', 'X')],
  [('G', 'O'), ('L', 'O'), ('E', 'X'), ('A', 'V'), ('M', 'X')],
  [('L', 'X'), ('O', 'X'), ('C', 'X'), ('A', 'V'), ('L', 'V')],
  [('B', 'V'), ('A', 'V'), ('N', 'V'), ('A', 'V'), ('L', 'V')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')],
  [('-', '-'), ('-', '-'), ('-', '-'), ('-', '-'), ('-', '-')]]
  BANAL was the correct word!

  Your task is to perform this reasoning on a given wordle game state to make the best 5-letter word guess.
  Only respond with a valid 5 letter english word.

  Example 3:
  {previous_examples}

  {next_state}
  """.format(
        previous_examples="\n".join(
            [
                extract_example(wordle_board, guess)
                for wordle_board, guess in zip(wordle_boards[:-1], guesses)
            ]
        ),
        next_state=extract_example(wordle_boards[-1]),
    )


def extract_example(wordle_board, guess="") -> str:
    res = (
        "["
        + "\n".join(
            ["[" + ", ".join([str(char) for char in row]) + "]" for row in wordle_board]
        )
        + "]"
    )

    res += "\nguess: "
    if guess:
        res += '"' + guess + '"'
    return res


# **************************Connections*****************************************


def connections_prompt(words: List[str], previous_attempts: List[List]) -> str:
    return """
    You are playing the popular game "connections". You will be given a multiple of 4
    words up to 16 words, and your task is to find a grouping of 4 words that share
    something in common. The grouping are words that share a common thread. 
    You can only submit a group with words that are contained in the words array and the group
    must not be a group in the previous attempts array.

    Example 1:
    words: [JOHN, CUB, STAR, SILVER, KNEE, THRONE, JOEY, JELLY, CALF, ANKLE, CRAY, HEAD, SHIN, CAN, KID, THIGH]
    previous_attempts: []
    group: [ANKLE, SHIN, KNEE, THIGH]

    Example 2:
    words: [JOHN, CUB, STAR, SILVER, THRONE, JOEY, JELLY, CALF, CRAY, HEAD, CAN, KID]
    previous_attempts: [[JOHN, CUB, STAR, JELLY], [JELLY, CALF, CRAY, HEAD]]
    group: [CALF, CUB, JOEY, KID]

    Example 3:
    words: [CHAD, GEORGIA, JORDAN, TOGO, FISH, GOAT, SCALES, TWINS]
    previous_attempts: [[CHAD, TOGO, FISH, GOAT]]
    group: [FISH, GOAT, SCALES, TWINS]

    Example 4:
    words: {words}
    previous_attempts: {previous_attempts}
    group: 
    """.format(
        words="[" + ", ".join(words) + "]",
        previous_attempts="["
        + ", ".join(["[" + ", ".join(attempt) + "]" for attempt in previous_attempts])
        + "]"
        if previous_attempts
        else "[]",
    )
