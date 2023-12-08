import sys
from src.connections.play_connections import play_connections
from src.wordle.play_wordle import play_wordle


def main():
    if sys.argv[1].lower() == "connections":
        play_connections()
    elif sys.argv[1].lower() == "wordle":
        play_wordle()


if __name__ == "__main__":
    main()
