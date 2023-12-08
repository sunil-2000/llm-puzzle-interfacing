from typing import List
import time
import requests
from selenium.webdriver.common.by import By
from src.connections.prompts import prompt_factory
from src.general.controller import BrowserController
from src.general.config import OPENAI_API_KEY
from src.general.error import ApiRequestError


class ConnectionsController(BrowserController):
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
        self.attempts = 4

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
            time.sleep(3)
            return True

        prompt = prompt_factory(words, self.previous_guesses)
        print(prompt)
        guess = self.request(prompt)
        # process response
        print(f"GPT guess: {guess}")
        words = [
            word.strip().upper() for word in guess[1:-1].split(",")
        ]  # remove brackets, split by commas
        self.submit_group(words)
        print("submitted")
        # check if game over
        if self.attempts_left() == 1:
            return True
        # if correct, flush previous_guesses, else append previous guesses
        if self.check_guess(words):
            self.previous_guesses = []
            self.all_guesses.append(
                {"words": words, "correct": True, "turn": self.total_turns}
            )
            print("correct")
        else:
            self.previous_guesses.append(words)
            self.all_guesses.append(
                {"words": words, "correct": False, "turn": self.total_turns}
            )
            print("incorrect")

        # update new bindings, clear board
        self.word_to_buttons = self._get_word_html_elements()
        time.sleep(2)
        print("refreshing state")
        self.update_bindings()
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
            timeout=500,
        )

        if "error" in response.json():
            print(response.json())
            raise ApiRequestError("Error while making the api request")

        return response.json()["choices"][0]["message"]["content"]

    def submit_group(self, words: List[str]) -> None:
        for word in words:
            word_button = self.word_to_buttons[word]
            self.driver.execute_script(
                f"""
                let pointerDown = new Event('pointerdown');
                let wordButton = document.getElementById('{word_button.get_attribute('id')}');
                wordButton.dispatchEvent(pointerDown);
                wordButton.classList.add('selected');
                """,
                word_button,
            )
            time.sleep(0.25)
        # submit guess; submit is span element -> dispatch pointerdown event
        self.driver.execute_script(
            """
            let pointerDown = new Event('pointerdown');
            let submitButton = document.getElementById('submit-button');
            submitButton.dispatchEvent(pointerDown);
            """
        )
        time.sleep(2)

    def check_guess(self, words: List[str]) -> bool:
        correct_groups = self._get_correct_groups()
        return len(set(words) - set(correct_groups)) == 0

    def attempts_left(self) -> int:
        attempts = self.driver.find_elements(By.CLASS_NAME, "bubble")
        self.attempts = len(
            list(
                filter(
                    lambda x: "lost" not in x,
                    [attempt.get_attribute("class") for attempt in attempts],
                )
            )
        )
        return self.attempts

    def update_bindings(self) -> None:
        for word in self.word_to_buttons.values():
            if "selected" in word.get_attribute("class"):
                # deselect and update css class
                self.driver.execute_script(
                    f"""
                    let pointerCancel = new Event('pointercancel');
                    let wordButton = document.getElementById('{word.get_attribute('id')}');
                    wordButton.dispatchEvent(pointerCancel);
                    wordButton.classList.remove('selected');
                    """,
                    word,
                )
