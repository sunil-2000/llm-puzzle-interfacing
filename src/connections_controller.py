import os
import time
import requests
from src.controller import BrowserController
from selenium.webdriver.common.by import By
from src.prompts import connections_prompt

from typing import List

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class ConnectionController(BrowserController):
    def __init__(self) -> None:
        super().__init__("connections")
        self.driver.get("https://www.nytimes.com/games/connections")
        self.driver.find_element(By.CLASS_NAME, "pz-moment__button").click()
        time.sleep(1)
        self.submit = self.driver.find_element(By.ID, "submit_button")
        self.word_to_buttons = {
            e.text: e for e in self.driver.find_elements(By.CLASS_NAME, "item")
        }

        self.total_turns = 0
        print("initialized")

    def turn(self) -> List[str]:
        all_words = [e.text for e in self.driver.find_elements(By.CLASS_NAME, "item")]

        correct_groups = []
        if self.driver.find_elements(By.CLASS_NAME, "correct"):
            correct_groups = [
                e.text for e in self.driver.find_elements(By.CLASS_NAME, "correct")
            ]

        words = list(set(all_words) - set(correct_groups))
        prompt = connections_prompt(words)
        guess = self.request(prompt)
        self.update(guess)
        print("done")

    def request(self, prompt: str) -> str:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}",
        }
        payload = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 50,  # change later
        }
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
        )
        return response.json()["choices"][0]["message"]["content"]

    def update(self, guess: str) -> None:
        # process response
        words = guess[1:-1].split(",")  # remove brackets, split by commas
        for word in words:
            self.word_to_buttons[word.upper()].click()
        # update
        time.sleep(1)
        self.submit.click()
        self.total_turns += 1
