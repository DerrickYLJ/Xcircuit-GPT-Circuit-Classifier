import openai
import os
import pandas as pd
import time
import sys

openai.api_key = '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'

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages,
    temperature=0,
    )
    return response.choices[0].message["content"]




# read from file tempOutput.txt
prompt = ""
with open(sys.argv[1]) as f:
    prompt = f.read()

print("THIS IS THE PROMPT: " + prompt)
response = get_completion(prompt)
print(response)