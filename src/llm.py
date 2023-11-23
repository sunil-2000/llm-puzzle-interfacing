## wrapper over llm
import os
import requests
from src.controller import WordleController
from src.util import gpt4_v_wordle_payload
from src.prompts import wordle_prompt_gpt4_v as wordle_prompt

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class wordleAgent(WordleController):
  """
  wordle-LLM agent
  """
  def __init__(self, vision:bool=False) -> None:
    self.vision = vision
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
        "https://api.openai.com/v1/chat/completions", headers=request["headers"], json=request["payload"]
    )
    return response.json()["choices"][0]["message"]["content"].strip()

  def vision_guess(self) -> None:
    """
    1. screenshot page
    2. send page + prompt to llm
    3. get action back and take action (by entering 5 letter word)
    4. repeat until game is over
    """
    print("capturing")
    self.capture()
    image_path = (f"{self.image_dir}/turn-{self.total_turns-1}.png")
    llm_decisions = list(self.vision_response(wordle_prompt, image_path).strip())
    print(llm_decisions)
    [self.keyboard(char.lower()) for char in llm_decisions]
    self.keyboard("enter")
    print("submitted LLM response")

  def guess(self) -> None:
    """
    1. extract current state of game
    2. send state to llm
    3. get action back and execute
    4. repeat until game is over
    """
    pass
  def extract_state(self) -> None:
    pass

  def action(self) -> bool:
    """
    Have llm perform action on game, return current state of game
    * convert turn method into this function (abstraction over any game)
    """
    pass