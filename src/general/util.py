import base64

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
