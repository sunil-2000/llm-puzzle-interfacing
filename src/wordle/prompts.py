from typing import List

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

def previous_examples_factory(wordle_boards: List[str], guesses: List[str]) -> str:
    "\n".join(
        [
            extract_example(wordle_board, guess)
            for wordle_board, guess in zip(wordle_boards[:-1], guesses)
        ]
    )

def wordle_prompt_gpt4(wordle_boards: List[str], guesses: List[str]) -> str:
    return f"""
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
  {previous_examples_factory(wordle_boards, guesses)}

  {extract_example(wordle_boards[-1])}
  """
