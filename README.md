
# Discord-Economy-bot

## Description

This is a Discord bot created using Python. It has features to:  
- Track user money.  
- Save and load user data.  
- Provide commands for managing virtual currency.  

## Features

- Store and manage user money.  
- Persistent storage using `pickle` to save and load data.  
- Easy-to-use commands.  

## Installation

1. Clone this repository:  
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install the required dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your bot token:  
   ```
   DISCORD_TOKEN=your_discord_bot_token
   ```

## Usage

1. Start the bot:  
   ```bash
   python bot.py
   ```

2. Use the following commands in Discord:  
   - **Add Money**: `.addmoney <@user> <amount>`  
     Adds virtual money to a user's account.  
   - **Deduct Money**: `.deductmoney <@user> <amount>`  
     Deducts virtual money from a user's account.  
   - **Check Balance**: `.balance <@user>`  
     Displays the user's current balance.  

## Files

- `bot.py`: Main bot script.  
- `UserMoney.pkl`: File where user data is stored.  
- `requirements.txt`: List of Python dependencies.  
- `.env`: File for storing your bot token securely.  

## Dependencies

- `discord.py`: Discord API wrapper for Python.  
- `python-dotenv`: For managing environment variables.  

Install all dependencies using:  
```bash
pip install -r requirements.txt
```

## Contributing

Feel free to fork this repository and create pull requests with improvements!  

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
