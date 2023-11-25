## wrapper over llm
import os
import time
import requests
from wordle_controller import WordleController
from src.util import gpt4_v_wordle_payload, gpt4_wordle_payload
from src.prompts import wordle_prompt_gpt4_v, wordle_prompt_gpt4


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class wordleAgent(WordleController):
    """
    wordle-LLM agent
    """

    def __init__(self, vision: bool = False) -> None:
        self.vision = vision
        self.board_sequence = []
        self.guesses = []
        super().__init__()

    def turn(self) -> None:
        """
        execute one turn of wordle (ie. submit 1 5-letter-word guess)
        """
        if self.vision:
            self.vision_guess()
        else:
            self.guess()
        pass

    def vision_response(self, prompt: str, image_path: str) -> str:
        """
        send image of wordle board + prompt to gpt-4-vision-preview
        """
        request = gpt4_v_wordle_payload(image_path, prompt, OPENAI_API_KEY)
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=request["headers"],
            json=request["payload"],
        )
        return response.json()["choices"][0]["message"]["content"]

    def vision_guess(self) -> None:
        """
        1. screenshot page
        2. send page + prompt to llm
        3. get action back and take action (by entering 5 letter word)
        4. repeat until game is over
        """
        print("capturing")
        self.capture()
        image_path = f"{self.image_dir}/turn-{self.total_turns-1}.png"
        guess = list(self.vision_response(wordle_prompt_gpt4_v, image_path).strip())
        self._submit_guess(guess)

    def response(self, prompt: str) -> str:
        request = gpt4_wordle_payload(prompt, OPENAI_API_KEY)
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=request["headers"],
            json=request["payload"],
        )
        print(response.json())
        return response.json()["choices"][0]["message"]["content"]

    def guess(self) -> None:
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

    def action(self) -> bool:
        """
        Have llm perform action on game, return current state of game
        * convert turn method into this function (abstraction over any game)
        """
        pass

    def _submit_guess(self, guess: str) -> None:
        """
        submit guess to wordle
        """
        [self.keyboard(char.lower()) for char in guess]
        self.keyboard("enter")
        print("submitted LLM response")
