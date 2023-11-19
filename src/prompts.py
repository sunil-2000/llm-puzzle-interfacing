prompt_basic = """
Your job is to solve a Wordle, which is a puzzle in which you have to guess the hidden five letter word in six or fewer attempts.
In each attempt, you will receive an image representing the state of the game and supply a valid five-letter word. 
Each letter has a colored background tile that will change color upon submitting your guess to let you know whether that letter is correct or not. 
If the tile is green, that letter is in the word and is in the correct position. If the tile is yellow, that letter is in the word but is in the wrong position. 
Finally, if the tile is gray, that letter is not in the word. You will be shown this response in the next image you receive to inform your next guess. 
In order to win, you have to guess the correct word within six attempts. The goal is to guess the correct word in the least amount of guesses.

Here is an example of the gameplay, with five colored tiles below each word guessed representing the correctness of each letter, as specified above:
⬛️ = not guessed yet
🟨 = in word but in wrong position
🟩 = in word and in correct position
⬜ = not in word

guess 0: ALIEN
⬜⬜🟩⬜🟨
⬛️⬛️⬛️⬛️⬛️
⬛️⬛️⬛️⬛️⬛️
⬛️⬛️⬛️⬛️⬛️
⬛️⬛️⬛️⬛️⬛️

guess 1: COUGH
⬜⬜🟩⬜🟨
⬜⬜⬜⬜🟨
⬛️⬛️⬛️⬛️⬛️
⬛️⬛️⬛️⬛️⬛️
⬛️⬛️⬛️⬛️⬛️

guess 2: DRINK
⬜⬜🟩⬜🟨
⬜⬜⬜⬜🟨
⬜⬜🟩🟩🟩
⬛️⬛️⬛️⬛️⬛️
⬛️⬛️⬛️⬛️⬛️

guess 3: CHINK
⬜⬜🟩⬜🟨
⬜⬜⬜⬜🟨
⬜⬜🟩🟩🟩
🟨🟩🟩🟩🟩
⬛️⬛️⬛️⬛️⬛️

guess 4:THINK
⬜⬜🟩⬜🟨
⬜⬜⬜⬜🟨
⬜⬜🟩🟩🟩
🟨🟩🟩🟩🟩
🟩🟩🟩🟩🟩

In this example, it took five guesses to get the correct word “THINK”.

Example game (where the game state is derived from an image):

game state: <image>
ALIEN

game state: <image>
COUGH

game state: <image>
DRINK

game state: <image>
CHINK

game state: <image>
THINK

You will be given a picture of an image reflecting the wordle game state and will respond with only 5 letter words.
"""

prompt0 = """
Here is an example of the gameplay, with five colored tiles below each word guessed representing the correctness of each letter, as specified above:
⬛️ = not guessed yet
🟨 = in word but in wrong position
🟩 = in word and in correct position
⬜ = not in word

guess 0: ALIEN
⬜⬜🟩⬜🟨
⬛️⬛️⬛️⬛️⬛️
⬛️⬛️⬛️⬛️⬛️
⬛️⬛️⬛️⬛️⬛️
⬛️⬛️⬛️⬛️⬛️

guess 1: COUGH
⬜⬜🟩⬜🟨
⬜⬜⬜⬜🟨
⬛️⬛️⬛️⬛️⬛️
⬛️⬛️⬛️⬛️⬛️
⬛️⬛️⬛️⬛️⬛️

guess 2: DRINK
⬜⬜🟩⬜🟨
⬜⬜⬜⬜🟨
⬜⬜🟩🟩🟩
⬛️⬛️⬛️⬛️⬛️
⬛️⬛️⬛️⬛️⬛️

guess 3: CHINK
⬜⬜🟩⬜🟨
⬜⬜⬜⬜🟨
⬜⬜🟩🟩🟩
🟨🟩🟩🟩🟩
⬛️⬛️⬛️⬛️⬛️

guess 4:THINK
⬜⬜🟩⬜🟨
⬜⬜⬜⬜🟨
⬜⬜🟩🟩🟩
🟨🟩🟩🟩🟩
🟩🟩🟩🟩🟩

In this example, it took five guesses to get the correct word “THINK”.

Example game (where the game state is derived from an image):

game state: <image>
ALIEN

game state: <image>
COUGH

game state: <image>
DRINK

game state: <image>
CHINK

game state: <image>
THINK

You will be given a picture of an image reflecting the wordle game state and will respond with only 5 letter words.
"""