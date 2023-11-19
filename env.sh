#!/bin/bash
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
echo enter your openai api key:
read OPENAI_API_KEY
export OPENAI_API_KEY=$OPENAI_API_KEY
echo setup done