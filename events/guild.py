async def on_guild_join(self, guild):
        logger.info(f"Joined new guild: {guild.name} (ID: {guild.id}) with {guild.member_count} members")
        
async def on_guild_remove(self, guild):
        logger.info(f"Left guild: {guild.name} (ID: {guild.id})")
        
async def on_command_completion(self, interaction):
        logger.info(f"Command completed: /{interaction.command.name} by {interaction.user} in {interaction.guild.name if interaction.guild else 'DM'}")
        
async def on_app_command_completion(self, interaction, command):
        guild_info = f"in {interaction.guild.name}" if interaction.guild else "in DM"
        logger.info(f"Slash command completed: /{command.name} by {interaction.user} {guild_info}")
        
async def on_error(self, event_method, *args, **kwargs):
        logger.error(f"Error in event {event_method}: {args}, {kwargs}", exc_info=True)
        
async def on_disconnect(self):
        logger.warning("Bot disconnected from Discord")
        
async def on_resumed(self):
        logger.info("Bot connection resumed")
