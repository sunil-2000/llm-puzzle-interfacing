# define functions for choosing letters and controlling ui
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

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
        print("initializing complete")
        time.sleep(2)
        # init keyboard controller
        self._grab_buttons()
        self.total_turns = 0

    def _grab_buttons(self) -> None:
        keys = self.driver.find_elements(By.CLASS_NAME, "Key-module_key__kchQI") # wordle specific 
        self.keyboard = {key.get_attribute("data-key"): key for key in keys}
        self.keyboard["enter"] = self.keyboard["↵"]
        self.keyboard.pop("↵")

    def keyboard(self, character: str) -> None:
        self.keyboard[character].click()

    def capture(self):
        self.driver.save_screenshot(
            os.path.abspath(f"{self.image_dir}/turn-{self.total_turns}.png")
        )
        self.total_turns += 1
