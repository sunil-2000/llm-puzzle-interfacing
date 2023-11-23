import base64


def encode_image(image_path: str) -> bytes:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def gpt4_v_wordle_payload(image_path: str, prompt: str, OPENAI_API_KEY: str) -> str:
    encoded_image = encode_image(image_path)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{encoded_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 20,  # change later
    }
    return {"headers": headers, "payload": payload}


def gpt4_wordle_payload(prompt: str, OPENAI_API_KEY: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }
    payload = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 20,  # change later
    }
    return {"headers": headers, "payload": payload}
