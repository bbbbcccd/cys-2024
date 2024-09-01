from dotenv import load_dotenv
from openai import OpenAI
import os
import re

load_dotenv()

# Keeps urls from text
def filter_url(text): 
    url_pattern = r'(https?://\S+?(?=,|\s|$))'
    urls = re.findall(url_pattern, text)
    return urls

# Checks for grammar accuracy of text
def check_grammar(text):
    key = os.environ.get('GPTKEY')

    client = OpenAI(api_key=key)
    msg = text

    prompt = f"is this a grammatically correct sentence and with no spelling mistakes: '{msg}'. Only return Yes or No"

    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response += chunk.choices[0].delta.content
    
    return response.strip()