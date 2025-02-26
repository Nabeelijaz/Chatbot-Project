import discord
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Bot logged in as {self.user}')  

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        print(f"Message from {message.author}: {message.content}")

        await self.handle_ping(message)
        await self.handle_hello(message)
        await self.handle_bye(message)

    async def handle_ping(self, message):
        if message.content.lower() == 'ping':
            await message.channel.send('pong')

    async def handle_hello(self, message):
        if message.content.lower() == 'hello':
            await message.channel.send(f'Hello {message.author.name}!')

    async def handle_bye(self, message):
        if message.content.lower() == 'bye':
            await message.channel.send(f'Goodbye {message.author.name}!')

intents = discord.Intents.default()
intents.message_content = True 

client = MyClient(intents=intents)
client.run(TOKEN)  # Use token from .env file
