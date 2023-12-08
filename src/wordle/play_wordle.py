from src.wordle.agent import WordleAgent
from src.general.error import error_handler

@error_handler
def play_wordle():
    wc = WordleAgent()
    state = False
    while not state:
        wc.turn()
        state = wc.check_wordle_state()
    print(f"solved in {wc.total_turns} turns")
