from openai import OpenAI

client = OpenAI(api_key='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')
import os
import pandas as pd
import time
import sys


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=0)
    return response.choices[0].message.content




# read from file tempOutput.txt
prompt = ""
with open(sys.argv[1]) as f:
    prompt = f.read()
prompt = "Will components create a complete circuit that works and have no major risks? There is a Battery connected to a Wire connected to a Wire connected to a Wire connected to a Wire connected to the original Battery."
print("THIS IS THE PROMPT: " + prompt)
response = get_completion(prompt)
# print content
print(response)
