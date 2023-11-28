import time
import requests
from src.controller import BrowserController
from selenium.webdriver.common.by import By
from src.prompts import connections_prompt
from src.config import OPENAI_API_KEY

from typing import List


class ConnectionController(BrowserController):
    def __init__(self) -> None:
        super().__init__("connections")
        self.driver.get("https://www.nytimes.com/games/connections")
        self.driver.find_element(By.CLASS_NAME, "pz-moment__button").click()
        time.sleep(2)
        self.driver.find_element(By.ID, "close-help").click()
        self.word_to_buttons = self._get_word_html_elements()
        self.all_guesses = []
        self.previous_guesses = []
        self.total_turns = 0

    def _get_word_html_elements(self) -> List[str]:
        # call after each submission because DOM refreshes each submit
        return {e.text: e for e in self.driver.find_elements(By.CLASS_NAME, "item")}

    def _get_correct_groups(self) -> List[str]:
        correct_groups = []
        if self.driver.find_elements(By.CLASS_NAME, "correct"):
            correct_groups = [
                e.text for e in self.driver.find_elements(By.CLASS_NAME, "correct")
            ]
        return correct_groups

    def turn(self) -> bool:
        print(f"turn: {self.total_turns}")
        all_words = self.word_to_buttons.keys()
        correct_groups = self._get_correct_groups()
        words = list(set(all_words) - set(correct_groups))
        # check if only one grouping left (winner)
        if len(words) == 4:
            self.submit_group(all_words)
            return True

        prompt = connections_prompt(words, self.previous_guesses)
        guess = self.request(prompt)
        # process response
        print(f"GPT guess: {guess}")
        words = [
            word.strip().upper() for word in guess[1:-1].split(",")
        ]  # remove brackets, split by commas
        self.submit_group(words)
        print("submitted")
        # if correct, flush previous_guesses, else append previous guesses
        if self.check_guess(words):
            self.previous_guesses = []
            self.all_guesses.append(
                {"words": words, "correct": True, "turn": self.total_turns}
            )
        else:
            self.previous_guesses.append(words)
            self.all_guesses.append(
                {"words": words, "correct": False, "turn": self.total_turns}
            )

        # update new bindings, clear board
        self.word_to_buttons = self._get_word_html_elements()
        print('updated new bindings')
        time.sleep(2)
        for word in self.word_to_buttons.values():
            if "selected" in word.get_attribute("class"):
                # deselect and update css class
                self.driver.execute_script(
                    f"let pointerCancel = new Event('pointercancel'); let wordButton = document.getElementById('{word.get_attribute('id')}'); wordButton.dispatchEvent(pointerCancel); wordButton.class = '{word.get_attribute('class').rstrip(' selected')}'",
                    word,
                )
        self.total_turns += 1
        return False

    def request(self, prompt: str) -> str:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}",
        }
        payload = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 50,
        }
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
        )
        return response.json()["choices"][0]["message"]["content"]

    def submit_group(self, words: List[str]) -> None:
        for word in words:
            word_button = self.word_to_buttons[word]
            self.driver.execute_script(
                f"let pointerDown = new Event('pointerdown'); let wordButton = document.getElementById('{word_button.get_attribute('id')}'); wordButton.dispatchEvent(pointerDown); wordButton.class = '{word_button.get_attribute('class')} selected'",
                word_button,
            )
            time.sleep(1)
        time.sleep(3)
        # submit guess; submit is span element -> dispatch pointerdown event
        self.driver.execute_script(
            "let pointerDown = new Event('pointerdown'); let submitButton = document.getElementById('submit-button'); submitButton.dispatchEvent(pointerDown)"
        )
        time.sleep(3)

    def check_guess(self, words: List[str]) -> bool:
        correct_groups = self._get_correct_groups()
        return len(set(words) - set(correct_groups)) == 0
