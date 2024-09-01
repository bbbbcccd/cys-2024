from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
import re

# will be input from tele
input_text = "I found some great recipes at http://allrecipes.com and https://foodnetwork.com, which I think you would love to try."

def cleanup(text): # function to return url in array
    url_pattern = r'(https?://\S+)'
    urls = re.findall(url_pattern, text)
    return urls

print(cleanup(input_text))

def grammarCheck(text):
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
print(grammarCheck(input_text))