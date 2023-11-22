## wrapper over llm
import os
import requests
from src.controller import WordleController
from src.util import encode_image
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
from src.prompts import wordle_prompt

class llmAgent(WordleController):
  """
  wordle-LLM agent
  """
  def __init__(self) -> None:
    super().__init__()

  def response(self, prompt: str, image_path: str) -> str:
    """
    prompt: str
    image: str
    """
    encoded_image = encode_image(image_path)
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
                    {"type": "text", "text": prompt},
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
    return response.json()["choices"][0]["text"].strip()
  
  def interpret(self) -> None:
    """
    interpret image 
    """
    pass
  
  def turn(self) -> None:
    """
    1. screenshot page
    2. send page + prompt to llm
    3. get action back and take action (by entering 5 letter word)
    4. repeat until game is over
    """
    print("capturing")
    self.capture()
    image_path = (f"{self.image_dir}/turn-{self.total_turns-1}.png")
    llm_decisions = list(self.response(wordle_prompt, image_path).strip())
    print(llm_decisions)
    # upload word
    [self.keyboard(char.lower()) for char in llm_decisions]
    self.keyboard("enter")
    print("submitted LLM response")