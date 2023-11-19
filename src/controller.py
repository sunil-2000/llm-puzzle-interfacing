# define functions for choosing letters and controlling ui
import os
from datetime import datetime
import requests
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from util import encode_image
from prompts import prompt0 as prompt


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class BrowserController:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            "prefs",
            {
                "profile.managed_default_content_settings.images": 2,
                "profile.default_content_setting_values.notifications": 2,
                "profile.managed_default_content_settings.stylesheets": 2,
                "profile.managed_default_content_settings.cookies": 2,
                "profile.managed_default_content_settings.plugins": 2,
                "profile.managed_default_content_settings.geolocation": 2,
                "profile.managed_default_content_settings.media_stream": 2,
            },
        )
        # eventually make clear image directory per run
        self.image_dir = f"{os.path.abspath('images')}"
        run = f"run-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
        os.mkdir(f"{os.path.abspath('images')}/{run}")
        self.image_dir = os.path.abspath(f"images/{run}")
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.nytimes.com/games/wordle/index.html")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.driver.find_element(By.CLASS_NAME, "Welcome-module_button__ZG0Zh").click()
        self.driver.find_element(By.CLASS_NAME, "Modal-module_closeIcon__TcEKb").click()

        # init keyboard controller
        self._grab_buttons()
        self.total_turns = 0

        self.prompt = prompt

    def _grab_buttons(self) -> None:
        keys = self.driver.find_elements(By.CLASS_NAME, "Key-module_key__kchQI")
        self.char_to_buttons = {key.get_attribute("data-key"): key for key in keys}
        self.char_to_buttons["enter"] = self.char_to_buttons["↵"]
        self.char_to_buttons.pop("↵")

    def keyboard(self, character: str) -> None:
        self.char_to_buttons[character].click()

    def turn(self):
        """
        1. screenshot page
        2. send page + prompt to llm
        3. get action back and take action (by entering 5 letter word)
        4. repeat until game is over
        """
        print("capturing")
        self.capture()
        llm_decisions = list(self.llm_response().strip())
        print(llm_decisions)
        # upload word
        [self.keyboard(char.lower()) for char in llm_decisions]
        self.keyboard("enter")
        print("submitted LLM response")

    def llm_response(self):
        encoded_image = encode_image(f"{self.image_dir}/turn-{self.total_turns-1}.png")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}",
        }
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": self.prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{encoded_image}"
                            },
                        },
                    ],
                }
            ],
            "max_tokens": 20,  # change later
        }
        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
        )
        print(response.json())
        return response.json()["choices"][0]["message"]["content"]

    def capture(self):
        self.driver.save_screenshot(
            os.path.abspath(f"{self.image_dir}/turn-{self.total_turns}.png")
        )
        self.total_turns += 1


# example click a
bc = BrowserController()
# bc.keyboard("a")

while True:
    bc.turn()
print("done")
