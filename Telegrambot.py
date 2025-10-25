#Following is script to run a telegram bot which sends back to the user questions of Physics, Chemistry and Mathematics.
import random
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext
)
import asyncio

# Bot token provided by @BotFather
BOT_TOKEN = '7250302154:AAGd4R69g_JqvF-b8a-U2IsC_6IEsOoHqms'

# Define the directories where images are stored
IMAGE_DIRS = {
    'Physics': '/home/Ashutos2520/Physics',
    'Chemistry': '/home/Ashutos2520/Chemistry',
    'Math': '/home/Ashutos2520/Maths',
    'Random': '/home/Ashutos2520/Random'  # Path for random images
}

# Function to start the bot and provide options
async def start(update: Update, context: CallbackContext) -> None:
    reply_keyboard = [['Random Problem', 'Physics', 'Chemistry', 'Math']]
    await update.message.reply_text(
        'Welcome! Please choose a subject:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

# Function to handle the user’s choice
async def send_question(update: Update, context: CallbackContext) -> None:
    user_choice = update.message.text
    if user_choice in IMAGE_DIRS:
        images = os.listdir(IMAGE_DIRS[user_choice])
        if images:
            selected_image = random.choice(images)
            image_path = os.path.join(IMAGE_DIRS[user_choice], selected_image)
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(image_path, 'rb'))
        else:
            await update.message.reply_text(f"No images found for {user_choice}.")
    elif user_choice == 'Random Problem':
        random_subject = random.choice([subject for subject in IMAGE_DIRS.keys() if subject != 'Random'])
        images = os.listdir(IMAGE_DIRS[random_subject])
        if images:
            selected_image = random.choice(images)
            image_path = os.path.join(IMAGE_DIRS[random_subject], selected_image)
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(image_path, 'rb'))
        else:
            await update.message.reply_text(f"No images found for {random_subject}.")
    else:
        await update.message.reply_text("Invalid choice. Please select an option from the keyboard.")

def main():
    # Initialize the application with the bot token
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers for the start command and message responses
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_question))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()