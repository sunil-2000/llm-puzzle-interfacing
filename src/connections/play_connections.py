from src.connections.controller import ConnectionsController
from src.general.error import error_handler
from src.general.states import GameState
from data_collection.publisher import write_results


@error_handler
def play_connections():
    cc = ConnectionsController()
    state = GameState.PLAYING
    while state == GameState.PLAYING:
        state = cc.turn()
    write_results(
        cc.all_guesses,
        {
            "total_turns": cc.total_turns,
            "attempts_left": cc.attempts,
            "solved": cc.attempts > 1,
        },
        "history",
    )
    print(f"solved in {cc.total_turns} turns")
