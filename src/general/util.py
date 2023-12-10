import base64
from functools import wraps


def encode_image(image_path: str) -> bytes:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def gpt4_wordle_payload(prompt: str, openai_api_key: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}",
    }
    payload = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 20,  # change later
    }
    return {"headers": headers, "payload": payload}


def log_args_retval(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"{'*'*20}{func.__name__}{'*'*20}")
        print(f"args:\n")
        print(*args)
        retval = func(*args, **kwargs)
        print(f"{func.__name__} returns:\n {repr(retval)}")
        return retval

    return wrapper
