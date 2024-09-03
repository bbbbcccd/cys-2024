from dotenv import load_dotenv
import os
import requests

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler

# Get tele bot key
load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')
API_BASE_URL = os.environ.get('API_BASE_URL')

# Define states for the conversation
WAITING_FOR_SENDER_ID, WAITING_FOR_TEXT, OUTPUT_RESULTS = range(3)

# Dictionary to store user data
user_data = {}

# Command handler function for /start command
async def start(update: Update, context: CallbackContext) -> int:
    chat_id = update.message.chat_id
    await context.bot.send_message(chat_id, text=('Hi! Welcome to PhishZilla! Use this bot to verify the legitimacy of SMS messages'))
    await update.message.reply_text('Step 1. Verify sender ID. Now, input the sender ID (Case Sensitive):')
    return WAITING_FOR_SENDER_ID

# Function to handle sender ID input
async def receive_sender_id(update: Update, context: CallbackContext) -> int:
    sender_id = update.message.text

    # Make API Call to verify sender id
    sender_id_api_url = API_BASE_URL + 'verify-sender-id/' + sender_id
    res = requests.post(sender_id_api_url)
    if res.status_code == 200:
        data = {
            "sender_id": res.json()
        }
        user_data[update.message.from_user.id] = data
        
    await update.message.reply_text('Step 2, verify the message! Now, input your text message:')
    return WAITING_FOR_TEXT

# Function to handle Text message input
async def receive_text_message(update: Update, context: CallbackContext) -> int:
    text_message = update.message.text

    # Waiting message
    chat_id = update.message.chat_id
    await context.bot.send_message(chat_id, text=('Hold on, calculating likelihood of a scam message...'))
    
    # Make API Call to verify message content and links
    message_api_url = API_BASE_URL + 'verify-message'
    data = {"msg": text_message}
    res = requests.post(message_api_url, json=data)
    if res.status_code == 200:
        user_data[update.message.from_user.id]['text_message'] = res.json()


    await print_results(update)

# Function to handle Scammy input
async def print_results(update):
    user_id = update.message.from_user.id
    if user_id not in user_data or "sender_id" not in user_data[user_id] or "text_message" not in user_data[user_id]:
        update.message.reply_text("Something went wrong. Please try again with /start")
        # Clear the user data after use
        del user_data[update.message.from_user.id]
        return ConversationHandler.END
    
    results = process_results(user_id)

    # Generate text to output to users   
    output_str = []
    output_str.append("Summary of text message sent by " + user_data[user_id]["sender_id"]["sender_id"]) # TODO: format user data better
    output_str.append(get_tests_passed(results))

    if results["is_registered"]:
        output_str.append("✅ SMS sender ID is registered") 
    else:
        output_str.append("❌ SMS sender ID is not registered")
    output_str.append("\n")

    if results["good_grammar"]:
        output_str.append("✅ Grammar is good")
    else:
        output_str.append("❌ Bad grammar detected in text (Possible sign of a scam)")
    output_str.append("\n")

    links = user_data[user_id]["text_message"]["links"]
    good_links = results["good_links"]
    bad_links = results["bad_links"]
    output_str.append("Found " + str(len(links)) + " links in total and " + str(len(bad_links)) + " possible phishing links")
    if len(bad_links) > 0:
        output_str.append("❌ Listing all possible phishing links: ")
        i = 1
        for url, phishing_prob in bad_links:
            output_str.append(str(i) + ". " + url + " has a phishing probability of " + str(round(phishing_prob, 2)) + "%")
            i += 1
    output_str.append("")
    
    if len(good_links) > 0:
        output_str.append("✅ Listing all safe links: ")
        i = 1
        for url, phishing_prob in good_links:
            output_str.append(str(i) + ". " + url + " has a phishing probability of " + str(round(phishing_prob, 2)) + "%")
            i += 1
    
    output_str = "\n".join(output_str)
    
    await update.message.reply_text(output_str)

    # Clear the user data after use
    del user_data[user_id]

def process_results(user_id):
    sender_id = user_data[user_id]['sender_id']
    text_message = user_data[user_id]['text_message']
    
    SCAM_THRESHOLD = 60

    checks = {
        "good_links": [],
        "bad_links": []
    }
    checks["is_registered"] = sender_id["is_registered"]
    checks["good_grammar"] = text_message["grammar"]
    for url, phishing_prob in text_message["links"].items():
        if phishing_prob > SCAM_THRESHOLD:
            checks["bad_links"].append((url, phishing_prob))
        else:
            checks["good_links"].append((url, phishing_prob))
    
    return checks

def get_tests_passed(results):
    TOTAL_CHECKS = 3
    checks_passed = 0
    if results["is_registered"]:
        checks_passed += 1
    if results["good_grammar"]:
        checks_passed += 1
    if len(results["bad_links"]) == 0:
        checks_passed += 1
    
    return "Number of tests passed: " + str(checks_passed) + " / " + str(TOTAL_CHECKS)

def main():
    # Create the Application and pass it your bot's token
    application = Application.builder().token(BOT_TOKEN).build()

    # Create a ConversationHandler for the user interaction
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            WAITING_FOR_SENDER_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_sender_id)],
            WAITING_FOR_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_text_message)],
            OUTPUT_RESULTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, print_results)],
        },
        fallbacks=[]
    )

    # Register the conversation handler
    application.add_handler(conversation_handler)

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
