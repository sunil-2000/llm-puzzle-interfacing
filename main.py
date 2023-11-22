from src.llm import llmAgent

agent = llmAgent()

while True:
  agent.turn()