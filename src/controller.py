import os
from datetime import datetime
from selenium import webdriver
from src.config import selenium_browser_prefs


class BrowserController:
    def __init__(self, game: str) -> None:
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", selenium_browser_prefs)
        # init data dump dir
        self.data_dir = f"{os.path.abspath('images')}"
        run = f"run-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
        if not os.path.exists(f"{os.path.abspath(game)}"):
            os.mkdir(f"{os.path.abspath(game)}")
        os.mkdir(f"{os.path.abspath(game)}/{run}")
        self.data_dir = os.path.abspath(f"{game}/{run}")

        # init game
        self.driver = webdriver.Chrome()
