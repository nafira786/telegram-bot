import logging
import requests
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command

# Replace with your actual API keys
TELEGRAM_BOT_TOKEN = "7952257277:AAECKUEOerPlmNm1M4dB-zxktSAkBaXjL3s"
OPENROUTER_API_KEY = "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"

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Enable logging
logging.basicConfig(level=logging.INFO)

# Function to interact with OpenRouter API
async def chat_with_ai(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",  # Change this if needed
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, json=data, headers=headers)

    # Debugging: Print response for errors
    print("Response Status Code:", response.status_code)
    print("Response JSON:", response.json())

    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response from AI")
    
    return f"Error: {response.json()}"  # Show API error message

# Start command
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Hello! I am a Deep seek bot. Send me a message, and I'll reply!")

# Handle user messages
@dp.message()
async def chat(message: Message):
    response = await chat_with_ai(message.text)
    await message.answer(response)

# Main function to start the bot
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Run the bot
if __name__ == "__main__":
    asyncio.run(main())