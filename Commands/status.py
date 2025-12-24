import discord
from discord import app_commands
from datetime import datetime, timezone
import time
import psutil
import os

async def status(interaction: discord.Interaction, public: bool = False):
    current_time = datetime.now(timezone.utc)
    
    bot_start_time = interaction.client.user.created_at if hasattr(interaction.client, 'start_time') else current_time
    if hasattr(interaction.client, 'start_time'):
        uptime_seconds = (current_time - interaction.client.start_time).total_seconds()
    else:
        process = psutil.Process(os.getpid())
        process_start = datetime.fromtimestamp(process.create_time(), tz=timezone.utc)
        uptime_seconds = (current_time - process_start).total_seconds()
    
    days = int(uptime_seconds // 86400)
    hours = int((uptime_seconds % 86400) // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    seconds = int(uptime_seconds % 60)
    
    if days > 0:
        uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
    elif hours > 0:
        uptime_str = f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        uptime_str = f"{minutes}m {seconds}s"
    else:
        uptime_str = f"{seconds}s"
    
    discord_latency = interaction.client.latency * 1000
    
    start = time.perf_counter()
    await interaction.response.defer(ephemeral=(not public) if interaction.guild else False)
    round_trip = (time.perf_counter() - start) * 1000
    
    embed = discord.Embed(
        title="Status",
        color=0xffe478,
        timestamp=current_time
    )
    
    embed.add_field(
        name="Uptime",
        value=f"Cypher has been up for **{uptime_str}**",
        inline=True
    )
    
    embed.add_field(
        name="Round Trip Latency",
        value=f" **{round_trip:.2f} ms**",
        inline=True
    )
    
    embed.add_field(
        name="Discord API Latency",
        value=f" **{discord_latency:.2f} ms**",
        inline=True
    )
    
    embed.add_field(
        name="Memory Usage",
        value=f" **{psutil.Process().memory_info().rss / 1024 / 1024:.1f} MB**",
        inline=True
    )
    
    if interaction.client.user.avatar:
        embed.set_thumbnail(url=interaction.client.user.avatar.url)
    
    embed.set_footer(
        text=f"Requested by {interaction.user.display_name}",
        icon_url=interaction.user.display_avatar.url
    )
    
    await interaction.followup.send(embed=embed)

command = app_commands.Command(
    name="status",
    description="Status of Cypher",
    callback=status,
)
command.dm_permission = True
