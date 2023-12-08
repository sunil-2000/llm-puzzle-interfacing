# Puzzle Interfaces for Large Language Models

## About

Wiring up Selenium with LLMs to play:

-   Wordle
-   Connections

## Setup

Run `sh env.sh`. When you are prompted for an OpenAI key, create one [here](https://platform.openai.com/api-keys). After you have confirmed that the `env.sh` script has been successful, simply run `source venv/bin/activate` and once inside, run `python3 main.py`.

## Interesting Observations:

-   gpt-4-vision seemingly cannot play wordle; does not make connections between
    each row when making new guess <-- (better prompting?) <- need way to easily map char to token?

## Todo:

-   Stronger examples in prompts
-   Permutation of word ordering impacts gpt4 performance on connections

## Demo

-   https://github.com/sunil-2000/llm-puzzle-interfacing/assets/59806352/a8f46963-d80b-4a32-84f3-d6e8f901fb0a
