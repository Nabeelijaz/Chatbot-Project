import discord
import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ensure API Key is available
if not DISCORD_TOKEN or not OPENAI_API_KEY:
    raise ValueError("Missing DISCORD_TOKEN or OPENAI_API_KEY in .env file.")

# Set OpenAI API Key
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

class MyClient(discord.Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def on_ready(self):
        print(f'Bot logged in as {self.user}')  

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        print(f"Message from {message.author}: {message.content}")

        # ChatGPT API integration
        response = await self.chatgptapi(message.content)
        await message.channel.send(response)

        if message.content.lower() == 'bye':
            await message.channel.send(f'Goodbye {message.author.name}!')

    async def chatgptapi(self, user_input):
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_input}],
                max_tokens=100
            )
            return response.choices[0].message.content
        except openai.OpenAIError as e:
            print(f"Error: {e}")
            return "I'm having trouble accessing ChatGPT right now. Please try again later."

# Define bot intents
intents = discord.Intents.default()
intents.message_content = True 

client = MyClient(intents=intents)
client.run(DISCORD_TOKEN)  # Use token from .env file
