from functools import wraps


class LlmPuzzleInterfacingError(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message

    def __str__(self):
        return f"{self.__class__.__name__}(msg={self.message})"


class ApiRequestError(LlmPuzzleInterfacingError):
    """Error while making a request to the OpenAI API"""


def error_handler(play_game):
    @wraps(play_game)
    def wrapper():
        try:
            play_game()
        except ApiRequestError as error:
            print(str(error.message))

    return wrapper
