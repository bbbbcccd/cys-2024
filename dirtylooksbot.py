from dotenv import load_dotenv
import os

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler

# Get tele bot key
load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Define states for the conversation
ASK_FEELING, WAITING_FOR_USER_ID, WAITING_FOR_TEXT, ASK_SCAMMY = range(4)

# Dictionary to store user data
user_data = {}

# Command handler function for /start command
async def start(update: Update, context: CallbackContext) -> int:
    # Define the custom keyboard with emojis
    keyboard = [['😊 Happy', '😞 Unhappy']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    # Send the initial message with the custom keyboard
    await update.message.reply_text('Hi! How are you feeling today?', reply_markup=reply_markup)
    return ASK_FEELING

# Function to handle button clicks for "happy" and "unhappy"
async def handle_feeling(update: Update, context: CallbackContext) -> int:
    text = update.message.text.lower()
    
    if 'happy' in text:
        await update.message.reply_text('Good day! 😊')
        await update.message.reply_text('Input your User ID (Case Sensitive):')
        return WAITING_FOR_USER_ID
    
    elif 'unhappy' in text:
        await update.message.reply_text('Bad day! 😞')
        await update.message.reply_text('Input your User ID (Case Sensitive):')
        return WAITING_FOR_USER_ID
    
    else:
        await update.message.reply_text('Please select either "😊 Happy" or "😞 Unhappy".')
        return ASK_FEELING

# Function to handle User ID input
async def receive_user_id(update: Update, context: CallbackContext) -> int:
    user_id = update.message.text
    user_data[update.message.from_user.id] = {'user_id': user_id}
    
    await update.message.reply_text('Thank you! Now, input your text message:')
    return WAITING_FOR_TEXT

# Function to handle Text message input
async def receive_text_message(update: Update, context: CallbackContext) -> int:
    text_message = update.message.text
    user_id = user_data[update.message.from_user.id]['user_id']
    
    # Save the text message in the user_data
    user_data[update.message.from_user.id]['text_message'] = text_message
    
    await update.message.reply_text(f'User ID: {user_id}\nText Message: {text_message}')
    await update.message.reply_text('How scammy is it? (Enter a float between 0 and 100):')
    return ASK_SCAMMY

# Function to handle Scammy input
async def handle_scammy(update: Update, context: CallbackContext) -> int:
    try:
        scammy_value = float(update.message.text)
        print(f"Received scammy value: {scammy_value}")  # Debugging statement

        if scammy_value < 0 or scammy_value > 100:
            await update.message.reply_text('Please enter a value between 0 and 100.')
            return ASK_SCAMMY
        
        if 0 <= scammy_value <= 30:
            await update.message.reply_text(
                'Warning: This is a scam!'  # Removed parse_mode for testing
            )
            await update.message.reply_text(
                'Please do not continue further.',
            )
        elif 30 < scammy_value <= 70:
            await update.message.reply_text(
                'This is likely a scam!'  # Removed parse_mode for testing
            )
            await update.message.reply_text(
                'Please proceed with caution.',
            )
        elif 70 < scammy_value <= 100:
            await update.message.reply_text(
                'You are safe!'  # Removed parse_mode for testing
            )
            await update.message.reply_text(
                'This is secured and is not a scam.',
            )

        # Clear the user data after use
        del user_data[update.message.from_user.id]
        return ConversationHandler.END

    except ValueError:
        await update.message.reply_text('Invalid input. Please enter a valid float number.')
        return ASK_SCAMMY


def main():
    # Create the Application and pass it your bot's token
    application = Application.builder().token(BOT_TOKEN).build()

    # Create a ConversationHandler for the user interaction
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ASK_FEELING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_feeling)],
            WAITING_FOR_USER_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_user_id)],
            WAITING_FOR_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_text_message)],
            ASK_SCAMMY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_scammy)],
        },
        fallbacks=[]
    )

    # Register the conversation handler
    application.add_handler(conversation_handler)

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
