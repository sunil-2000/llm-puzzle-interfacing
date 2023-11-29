from src.connections_controller import ConnectionController
from data_collection.publisher import write_results

cc = ConnectionController()
state = False 

while not state:
  state = cc.turn()

write_results(cc.all_guesses, {"total_turns": cc.total_turns, "attempts_left": cc.attempts, "solved": True if cc.attempts > 0 else False}, "history")

print(f"solved in {cc.total_turns} turns")