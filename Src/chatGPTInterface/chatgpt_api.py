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
print(prompt)
response = get_completion(prompt)
# print content

print(response)
