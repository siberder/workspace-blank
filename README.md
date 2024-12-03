# Food Diary Telegram Bot

This project is a Telegram bot for tracking your daily food intake. It allows you to recognize calories in food from photos and text using the ChatGPT API, manually edit food entries, set and track goals for calories, protein, fat, and carbohydrates, and view previous days' entries.

## Features

- Recognize calories in food from photos (using ChatGPT API)
- Recognize calories in food from text (using ChatGPT API)
- Manually edit food entries
- Set and edit goals for calories, protein, fat, and carbohydrates
- Track current goals for calories, protein, fat, and carbohydrates
- View previous days' entries

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/githubnext/workspace-blank.git
   cd workspace-blank
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up the configuration file:
   - Create a file named `config.py` in the root directory.
   - Add your Telegram bot API key and ChatGPT API key to the configuration file.
   - Set default goals for calories, protein, fat, and carbohydrates.

## Usage Instructions

1. Start the bot:
   ```
   python bot.py
   ```

2. Use the following commands to interact with the bot:
   - `/add_photo` - Add a food entry by sending a photo
   - `/add_text` - Add a food entry by sending a text description
   - `/edit_entry` - Manually edit a food entry
   - `/set_goal` - Set a goal for calories, protein, fat, and carbohydrates
   - `/view_goal` - View the current goals
   - `/view_history` - View previous days' entries
