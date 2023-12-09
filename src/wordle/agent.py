## wrapper over llm
import time
import requests
from src.wordle.controller import WordleController
from src.wordle.prompts import wordle_prompt_gpt4
from src.general.util import gpt4_wordle_payload
from src.general.config import OPENAI_API_KEY


class WordleAgent(WordleController):
    """
    wordle-LLM agent
    """

    def __init__(self) -> None:
        super().__init__()
        self.board_sequence = []
        self.guesses = []

    def turn(self) -> None:
        """
        1. extract current state of game
        2. send state to llm
        3. get action back and execute
        4. repeat until game is over
        """
        result = self.check_wordle_state()
        if result:
            print("game over")
            self.driver.close()
            return

        wordle_board = self.get_wordle_board()
        self.board_sequence.append(wordle_board)
        prompt = wordle_prompt_gpt4(self.board_sequence, self.guesses)
        print(prompt)
        guess = self.response(prompt).strip().strip('"')
        print(self.guesses)
        self.guesses.append(guess)
        self._submit_guess(guess)
        time.sleep(3)

    def response(self, prompt: str) -> str:
        request = gpt4_wordle_payload(prompt, OPENAI_API_KEY)
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=request["headers"],
            json=request["payload"],
            timeout=500
        )
        print(response.json())
        return response.json()["choices"][0]["message"]["content"]

    def _submit_guess(self, guess: str) -> None:
        """
        submit guess to wordle
        """
        for char in guess:
            self.keyboard(char.lower())
        self.keyboard("enter")
        print("submitted LLM response")
