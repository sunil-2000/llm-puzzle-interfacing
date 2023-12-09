import os
from typing import List, Tuple
from selenium.webdriver.common.by import By

from src.general.controller import BrowserController


class WordleController(BrowserController):
    def __init__(self) -> None:
        super().__init__("wordle")
        self.driver.get("https://www.nytimes.com/games/wordle/index.html")
        self.driver.find_element(By.CLASS_NAME, "Welcome-module_button__ZG0Zh").click()
        self.driver.find_element(By.CLASS_NAME, "Modal-module_closeIcon__TcEKb").click()
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # init keyboard controller
        self._grab_buttons()
        self.total_turns = 0

    def _grab_buttons(self) -> None:
        keys = self.driver.find_elements(
            By.CLASS_NAME, "Key-module_key__kchQI"
        )  # wordle specific
        self.keyboard_map = {key.get_attribute("data-key"): key for key in keys}
        self.keyboard_map["enter"] = self.keyboard_map["↵"]
        self.keyboard_map.pop("↵")

    def keyboard(self, character: str) -> None:
        self.keyboard_map[character].click()

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
        return self.driver.find_elements(By.CLASS_NAME, "Stats-module_statsContainer__g23s0")
