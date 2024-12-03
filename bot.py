import os
from telegram import Update, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import openai
from PIL import Image
from food_diary import FoodDiary
from config import TELEGRAM_API_KEY, CHATGPT_API_KEY

# Initialize the food diary
food_diary = FoodDiary()

# Set up OpenAI API key
openai.api_key = CHATGPT_API_KEY

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Add Food (Photo)", callback_data='add_photo')],
        [InlineKeyboardButton("Add Food (Text)", callback_data='add_text')],
        [InlineKeyboardButton("Edit Entry", callback_data='edit_entry')],
        [InlineKeyboardButton("Set Goal", callback_data='set_goal')],
        [InlineKeyboardButton("View Goal", callback_data='view_goal')],
        [InlineKeyboardButton("View History", callback_data='view_history')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Welcome to the Food Diary Bot!', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == 'add_photo':
        query.edit_message_text(text="Please send a photo of your food.")
        context.user_data['action'] = 'add_photo'
    elif query.data == 'add_text':
        query.edit_message_text(text="Please send a text description of your food.")
        context.user_data['action'] = 'add_text'
    elif query.data == 'edit_entry':
        query.edit_message_text(text="Please provide the entry index and new values.")
        context.user_data['action'] = 'edit_entry'
    elif query.data == 'set_goal':
        query.edit_message_text(text="Please provide the new goals for calories, protein, fat, and carbohydrates.")
        context.user_data['action'] = 'set_goal'
    elif query.data == 'view_goal':
        goals = food_diary.goals
        query.edit_message_text(text=f"Current goals:\nCalories: {goals['calories']}\nProtein: {goals['protein']}\nFat: {goals['fat']}\nCarbohydrates: {goals['carbohydrates']}")
    elif query.data == 'view_history':
        query.edit_message_text(text="Please provide the number of days to view.")
        context.user_data['action'] = 'view_history'

def handle_message(update: Update, context: CallbackContext) -> None:
    action = context.user_data.get('action')
    if action == 'add_photo':
        photo_file = update.message.photo[-1].get_file()
        photo_file.download('food_photo.jpg')
        image = Image.open('food_photo.jpg')
        calories = recognize_calories_from_photo(image)
        food_diary.add_entry(calories)
        update.message.reply_text(f'Added food entry with {calories} calories.')
    elif action == 'add_text':
        text = update.message.text
        calories = recognize_calories_from_text(text)
        food_diary.add_entry(calories)
        update.message.reply_text(f'Added food entry with {calories} calories.')
    elif action == 'edit_entry':
        try:
            index, calories, protein, fat, carbohydrates = map(int, update.message.text.split())
            food_diary.edit_entry(index, calories, protein, fat, carbohydrates)
            update.message.reply_text(f'Edited entry at index {index}.')
        except ValueError:
            update.message.reply_text('Invalid input. Please provide the entry index and new values.')
    elif action == 'set_goal':
        try:
            calories, protein, fat, carbohydrates = map(int, update.message.text.split())
            food_diary.set_goal(calories, protein, fat, carbohydrates)
            update.message.reply_text('Goals updated successfully.')
        except ValueError:
            update.message.reply_text('Invalid input. Please provide the new goals for calories, protein, fat, and carbohydrates.')
    elif action == 'view_history':
        try:
            days = int(update.message.text)
            entries = food_diary.view_previous_days(days)
            if entries:
                response = f'Entries for the past {days} days:\n'
                for entry in entries:
                    response += f"Calories: {entry['calories']}, Protein: {entry['protein']}, Fat: {entry['fat']}, Carbohydrates: {entry['carbohydrates']}\n"
                update.message.reply_text(response)
            else:
                update.message.reply_text(f'No entries found for the past {days} days.')
        except ValueError:
            update.message.reply_text('Invalid input. Please provide the number of days to view.')

def recognize_calories_from_photo(image: Image) -> int:
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt="Estimate the number of calories in this food item based on the photo.",
        max_tokens=10
    )
    calories = int(response.choices[0].text.strip())
    return calories

def recognize_calories_from_text(text: str) -> int:
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Estimate the number of calories in the following food description: {text}",
        max_tokens=10
    )
    calories = int(response.choices[0].text.strip())
    return calories

def main() -> None:
    updater = Updater(TELEGRAM_API_KEY)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_message))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
