import os
import logging
from datetime import datetime, timezone
import discord
from discord import app_commands
from events.logging import setup_logging
from events.commands import commands_load

# Call the logging event to start logging
logger = setup_logging()

# Set the token from an environment token
TOKEN = os.getenv("DEVELOPMENT")
if not TOKEN:
    logger.error("No token found in environment variable DEVELOPMENT")
    raise ValueError("No token found in environment variable DEVELOPMENT")

# Setup intents
intents = discord.Intents.default()
intents.message_content = True

# Initialize the client
class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.command_count = 0
        self.start_time = datetime.now(timezone.utc)
        logger.info("Cypher client initialized")

# Pull commands from the commands directory and inform the user 
    async def setup_hook(self):
        try:
            self.command_count = await commands_load(self.tree)
            logger.info("Loaded %d application commands", self.command_count)
        except Exception:
            logger.exception("Failed to load commands in setup_hook")


# The bot is ready to start, inform the user of any changes to the bot.
    async def on_ready(self):
        logger.info("READY as %s (ID: %s)", self.user, self.user.id)

    async def on_guild_join(self, guild):
        logger.info("Joined new guild: %s (ID: %s) with %s members", guild.name, guild.id, guild.member_count)

    async def on_guild_remove(self, guild):
        logger.info("Left guild: %s (ID: %s)", guild.name, guild.id)

    async def on_command_completion(self, interaction):
        guild_info = interaction.guild.name if interaction.guild else "DM"
        logger.info("Command completed: /%s by %s in %s", interaction.command.name, interaction.user, guild_info)

    async def on_app_command_completion(self, interaction, command):
        guild_info = f"in {interaction.guild.name}" if interaction.guild else "in DM"
        logger.info("Slash command completed: /%s by %s %s", command.name, interaction.user, guild_info)

    async def on_error(self, event_method, *args, **kwargs):
        logger.error("Error in event %s: %s, %s", event_method, args, kwargs, exc_info=True)

    async def on_disconnect(self):
        logger.warning("Bot disconnected from Discord")

    async def on_resumed(self):
        logger.info("Bot connection resumed")

# Start the bot
client = MyClient()
client.run(TOKEN)
