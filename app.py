from flask import Flask, request

app = Flask(__name__)

@app.route('/verify-sender-id/<sender_id>', methods=['POST'])
def verify_sender_id(sender_id):
    return {
        "sender_id": sender_id,
        "is_registered": True
    }

@app.route('/verify-message', methods=['POST'])
def verify_message():
    data = request.get_json()
    msg = data.get("msg")

    return {
        "msg": msg,
        "links": [], # array of url: phishing website likelihood
        "grammar": True # Grammar of message
    }


# main driver function
if __name__ == '__main__':
    app.run()