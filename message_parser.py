from dotenv import load_dotenv
import os
import re
import nlpcloud

load_dotenv()

# Keeps urls from text
def filter_url(text): 
    url_pattern =r'\b(?:https?://)?(?:www\.)?[\w.-]+\.[a-zA-Z]{2,6}(?:/\S*)?\b'
    urls = re.findall(url_pattern, text)
    return urls

# Checks for grammar accuracy of text
def check_grammar(text):
    key = os.environ.get('GRAMMAR_KEY')
    client = nlpcloud.Client("finetuned-llama-3-70b", key, True)
    correction = client.gs_correction(text)
    
    # Return the corrected text
    return correction['correction'] == text
