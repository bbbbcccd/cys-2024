from flask import Flask, request
from ssir import check_ssir
from message_parser import filter_url,check_grammar
from phishing import predict_phishing_probabilities
app = Flask(__name__)

@app.route('/')


@app.route('/verify-sender-id/<sender_id>', methods=['POST', 'GET'])
def verify_sender_id(sender_id):
    is_registered = check_ssir(sender_id)

    return {
        "sender_id": sender_id,
        "is_registered": is_registered
    }

@app.route('/verify-message', methods=['POST'])
def verify_message():
    data = request.get_json()
    msg = data.get("msg") #get input text as a string
    
    # Check grammar
    grammarChecked = check_grammar(msg) #will return a True or False

    # Predict phishing probability for each url
    urls = filter_url(msg) # should return an array of URLs
    urls = predict_phishing_probabilities(urls)

    return {
        "msg": msg,
        "links": urls, # array of url: phishing website likelihood
        "grammar": grammarChecked # Grammar of message
    }


# main driver function
if __name__ == '__main__':
    app.run()