from src.connections_controller import ConnectionController

cc = ConnectionController()
state = False 

while not state:
  print(state)
  state = cc.turn()

print(f"solved in {cc.total_turns} turns")