from src.llm import wordleAgent
from src.controller import WordleController



wa = wordleAgent()
while True:
  wa.guess()
