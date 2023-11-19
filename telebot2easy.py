# Dependencies: 'python-telegram-bot=13.*'

# Token for the Telegram bot
Token = "you token"

import subprocess
import logging
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

# Set up logging for debugging purposes
logging.basicConfig(filename='bot_debug.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants for conversation states
CHOOSING = 1

# Function to deploy the code-server container
def deploy_code_server(update: Update, context: CallbackContext):
    try:
        # Inform the user about the deployment
        update.message.reply_text("Deploying code-server. Please wait for the deployment to complete.")

        # Log the deployment initiation
        logger.info("Starting deployment of code-server...")

        # Open a log file to track the deployment process
        with open("deployment_logs.txt", "a") as log_file:
            log_file.write("Starting deployment of code-server...\n")

            # Run the Ansible playbook for code-server deployment and capture the output
            process = subprocess.Popen(['ansible-playbook', 'code-server.yaml'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            
            # Iterate through the playbook output
            for line in process.stdout:
                log_file.write(line + '\n')

                # Send non-empty lines from the playbook output to the user
                if line.strip():
                    update.message.reply_text(line)
                
                # Log the playbook output for debugging purposes
                logger.debug(line)

    except Exception as e:
        # Handle any errors during the deployment
        update.message.reply_text(f"Error: {str(e)}")
        logger.exception("Exception occurred: ")

# Function to display help information
def help_op(update: Update, context: CallbackContext):
    update.message.reply_text(
        """
        This is NSheth BOT 
        Send 'deploy code-server' to deploy the Code-Server container 
        Send 'help' to view this menu 
        """
    )
    # Modify this function as per the requirements of additional options

# Allowed user IDs
ALLOWED_USERS = [1279071275, 1279071275]

# Function to start the bot conversation
def start(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    if user_id not in ALLOWED_USERS:
        # Check if the user is authorized to use the bot
        update.message.reply_text("You are not authorized to access this bot.")
        return ConversationHandler.END
    
    # Display the options to the user
    reply_keyboard = [['/Start', 'Help']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Choose an option:', reply_markup=markup)
    return CHOOSING

# Function to handle user choice
def choice(update: Update, context: CallbackContext) -> int:
    user_choice = update.message.text.lower()
    if user_choice == 'deploy code-server':
        deploy_code_server(update, context)
    elif user_choice == 'help':
        help_op(update, context)
    else:
        # Handle an invalid user choice
        update.message.reply_text('Invalid option.')
    return CHOOSING

# Function to cancel the ongoing process
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Cancelled the process.')
    return ConversationHandler.END

# Main function to run the bot
def main():
    updater = Updater(Token)
    dp = updater.dispatcher

    # Define conversation handler to manage user interactions
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(Filters.text & ~Filters.command, choice),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Add conversation handler to the bot dispatcher
    dp.add_handler(conv_handler)
    
    # Start polling for updates from Telegram
    updater.start_polling()
    
    # Keep the bot running until interrupted
    updater.idle()

if __name__ == '__main__':
    main()
