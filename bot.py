"""
Whispr - Anonymous Confession & Reply Discord Bot

Setup Instructions:
1. Install dependencies:
   pip install -r requirements.txt

2. Create a .env file in this directory with:
   TOKEN=your_discord_bot_token

3. Run the bot:
   python bot.py

requirements.txt:
discord.py
python-dotenv

The bot allows users to send anonymous confessions and replies via DM.
"""

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import time
import json

CONFESSION_RATE_LIMIT = 30
COUNTER_FILE = "confession_counter.txt"
CONFESSION_MAP_FILE = "confession_map.json"
CONFESSION_GUILD_MAP_FILE = "confession_guild_map.json"
CONFESSION_COUNTERS_FILE = "confession_counters.json"

user_last_confession = {}

def load_guild_map():
    if not os.path.exists(CONFESSION_GUILD_MAP_FILE):
        return {}
    with open(CONFESSION_GUILD_MAP_FILE, "r") as f:
        return json.load(f)

def save_guild_map(guild_map):
    with open(CONFESSION_GUILD_MAP_FILE, "w") as f:
        json.dump(guild_map, f)

def load_confession_counters():
    if not os.path.exists(CONFESSION_COUNTERS_FILE):
        return {}
    with open(CONFESSION_COUNTERS_FILE, "r") as f:
        return json.load(f)

def save_confession_counters(counters):
    with open(CONFESSION_COUNTERS_FILE, "w") as f:
        json.dump(counters, f)

def get_next_confession_code(guild_id):
    counters = load_confession_counters()
    gid = str(guild_id)
    num = counters.get(gid, 1)
    counters[gid] = num + 1
    save_confession_counters(counters)
    return num

def load_confession_map():
    if not os.path.exists(CONFESSION_MAP_FILE):
        return {}
    with open(CONFESSION_MAP_FILE, "r") as f:
        return json.load(f)

def save_confession_map(confession_map):
    with open(CONFESSION_MAP_FILE, "w") as f:
        json.dump(confession_map, f)

confession_map = load_confession_map()
guild_map = load_guild_map()

load_dotenv()
TOKEN = os.getenv('TOKEN')
if not TOKEN:
    raise RuntimeError("Missing TOKEN in .env file.")

intents = discord.Intents.default()
intents.messages = True
intents.dm_messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx, channel: discord.TextChannel):
    """Set the confession channel for this server."""
    guild_map = load_guild_map()
    guild_map[str(ctx.guild.id)] = channel.id
    save_guild_map(guild_map)
    await ctx.send(f"✅ Confession channel set to {channel.mention}")

@setup.error
async def setup_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need administrator permissions to use this command.")
    else:
        await ctx.send("❌ Usage: !setup #channel")

@bot.event
async def on_guild_join(guild):
    channel = guild.system_channel
    if channel is None:
        for c in guild.text_channels:
            if c.permissions_for(guild.me).send_messages:
                channel = c
                break
    if channel:
        await channel.send(
            "**Hi! I'm Whispr, your anonymous confession bot!**\n"
            "• To get started, an admin should run `!setup #channel` to set the confession channel.\n"
            "• For help and usage instructions, use `!whisprhelp`.\n"
            "• Users can DM me to send confessions or anonymous replies!"
        )

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if isinstance(message.channel, discord.DMChannel):
        confession_channel = None
        for guild in bot.guilds:
            guild_map = load_guild_map()
            channel_id = guild_map.get(str(guild.id))
            if channel_id:
                channel = bot.get_channel(channel_id)
                if channel:
                    confession_channel = channel
                    break
        if not confession_channel:
            await message.channel.send(
                "❌ Confession channel not set up. Ask an admin to use `!setup #channel` in their server.\n"
                "For more info, use `!whisprhelp` in the server."
            )
            return

        if message.content.lower().startswith("reply"):
            parts = message.content.strip().split(maxsplit=2)
            if len(parts) < 3:
                await message.channel.send("❌ Invalid reply format. Use: reply #001 your message or reply 001 your message")
                return
            code_part = parts[1]
            if code_part.startswith("#"):
                code = code_part[1:]
            else:
                code = code_part
            if not code.isdigit():
                await message.channel.send("❌ Invalid confession code. Use: reply #001 your message or reply 001 your message")
                return
            reply_content = parts[2].strip()
            if not reply_content:
                await message.channel.send("❌ Your reply cannot be empty.")
                return
            channel = confession_channel
            if channel is None:
                await message.channel.send("❌ Confession channel not found. Please contact the admin.")
                return

            confession_message = None
            async for msg in channel.history(limit=100):
                if msg.author == bot.user and msg.content.startswith(f"💬 **Anonymous Confession #{int(code):03d}:**"):
                    confession_message = msg
                    break
            if confession_message:
                reply_msg = await channel.send(
                    f"💬 **Anonymous Reply to Confession #{int(code):03d}:**\n{reply_content}",
                    reference=confession_message
                )
                await message.channel.send(f"✅ Your anonymous reply to confession #{int(code):03d} has been posted as a reply!")
                confession_map = load_confession_map()
                user_id = confession_map.get(str(int(code)))
                if user_id:
                    try:
                        user = await bot.fetch_user(user_id)
                        await user.send(
                            f"📩 Your confession #{int(code):03d} received a new anonymous reply:\n{reply_content}"
                        )
                    except Exception:
                        pass
            else:
                await channel.send(f"💬 **Anonymous Reply to Confession #{int(code):03d}:**\n{reply_content}")
                await message.channel.send(f"⚠️ Confession #{int(code):03d} not found. Your reply was posted as a normal message.")
            return

        now = time.time()
        last = user_last_confession.get(message.author.id, 0)
        if now - last < CONFESSION_RATE_LIMIT:
            await message.channel.send("⏳ Please wait before sending another confession.")
            return
        user_last_confession[message.author.id] = now

        content = message.content.strip()
        if not content:
            await message.channel.send("❌ Your confession cannot be empty.")
            return
        channel = confession_channel
        if channel is None:
            await message.channel.send("❌ Confession channel not found. Please contact the admin.")
            return
        guild_id = confession_channel.guild.id
        code = get_next_confession_code(guild_id)
        confession_msg = await confession_channel.send(f"💬 **Anonymous Confession #{code:03d}:**\n{content}")
        await confession_msg.add_reaction("👍")
        await confession_msg.add_reaction("👎")
        confession_map[str(code)] = message.author.id
        save_confession_map(confession_map)
        await message.channel.send("✅ Your confession has been posted anonymously!")

    await bot.process_commands(message)

@bot.command(name="whisprhelp")
async def whisprhelp(ctx):
    """Show help for Whispr bot."""
    help_text = (
        "**Whispr Bot Help**\n"
        "• `!setup #channel` — Set the confession channel (admin only).\n"
        "• DM me your message — Send an anonymous confession.\n"
        "• DM me `reply #001 your message` — Reply anonymously to confession #001.\n"
        "• Wait 30 seconds between confessions.\n"
        "• Confessions and replies are anonymous.\n"
        "• Only server admins can run `!setup`.\n"
        "• If you need more help, contact your server admin."
    )
    await ctx.send(help_text)

bot.run(TOKEN)