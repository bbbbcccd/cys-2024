'''
Checks if the user input sender id is registered under SMS Registry
https://www.sgnic.sg/smsregistry/overview
'''

import requests

def _create_url_string(sender_id):
    base_url_front = "https://smsregistry.sg/web/sid-query?nolayout=1&filter=name%3A"
    base_url_end = "&view=table"
    return base_url_front + sender_id + base_url_end

def _check_registered_sender_id(response):
    txt = response.text
    
    # Process text to find string after status-content div
    start_identifier = "<div class=\"status-content\">"
    start_idx = txt.find(start_identifier)
    txt = txt[start_idx: ]

    return txt.find("Currently registered") != -1 or txt.find("Not for registration") != -1

def SSIR_checker(sender_id):
    res = requests.get(_create_url_string(sender_id))
    return _check_registered_sender_id(res)

# Test
if __name__ == "__main__":
    legit_sender_id = "NUS"
    fake_sender_id = "Nus"
    gov_sender_id = "gov.sg"
    print(SSIR_checker(legit_sender_id))
    print(SSIR_checker(fake_sender_id))
    print(SSIR_checker(gov_sender_id))
