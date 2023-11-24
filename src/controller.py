# define functions for choosing letters and controlling ui
import os
import time
from datetime import datetime
from selenium import webdriver
from pprint import pprint
from selenium.webdriver.common.by import By

from typing import List, Tuple


class WordleController:
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
        self.driver.find_element(By.CLASS_NAME, "Welcome-module_button__ZG0Zh").click()
        self.driver.find_element(By.CLASS_NAME, "Modal-module_closeIcon__TcEKb").click()
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # init keyboard controller
        self._grab_buttons()
        self.total_turns = 0
        print("initializing complete")

    def _grab_buttons(self) -> None:
        keys = self.driver.find_elements(
            By.CLASS_NAME, "Key-module_key__kchQI"
        )  # wordle specific
        self.keyboard_map = {key.get_attribute("data-key"): key for key in keys}
        self.keyboard_map["enter"] = self.keyboard_map["↵"]
        self.keyboard_map.pop("↵")

    def keyboard(self, character: str) -> None:
        self.keyboard_map[character].click()

    def capture_screen(self) -> None:
        self.driver.save_screenshot(
            os.path.abspath(f"{self.image_dir}/turn-{self.total_turns}.png")
        )
        self.total_turns += 1

    def get_wordle_board(self) -> List[List[Tuple[str, str]]]:
        """
        extract wordle board from page
        """
        rows = self.driver.find_elements(By.CLASS_NAME, "Row-module_row__pwpBq")
        data_state_map = {
            "correct": "V",
            "present": "O",
            "absent": "X",
            "empty": "-",
            "tbd": "-",
        }
        extracted_board = [
            [
                (
                    char.text if char.text else "-",
                    data_state_map[char.get_attribute("data-state")],
                )
                for char in row.find_elements(By.CLASS_NAME, "Tile-module_tile__UWEHN")
            ]
            for row in rows
        ]
        return extracted_board

    def check_wordle_state(self) -> bool:
        """
        check if wordle is over
        """
        return (
            True
            if self.driver.find_elements(
                By.CLASS_NAME, "Stats-module_statsContainer__g23s0"
            )
            else False
        )
