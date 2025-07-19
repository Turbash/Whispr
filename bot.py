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
intents.members = True  

bot = commands.Bot(
    command_prefix='!', 
    intents=intents,
    reconnect=True,
    max_messages=1000  
)

class ServerSelectView(discord.ui.View):
    def __init__(self, confession_channels, user_message):
        super().__init__(timeout=60)
        self.confession_channels = confession_channels
        self.user_message = user_message
        
        for i, channel in enumerate(confession_channels[:5]):  
            button = discord.ui.Button(
                label=channel.guild.name[:80],  
                style=discord.ButtonStyle.primary,
                custom_id=f"server_{i}"
            )
            button.callback = self.create_callback(i)
            self.add_item(button)
    
    def create_callback(self, index):
        async def callback(interaction):
            if interaction.user.id != self.user_message.author.id:
                await interaction.response.send_message("❌ This is not your server selection.", ephemeral=True)
                return
            
            confession_channel = self.confession_channels[index]
            await interaction.response.defer()
            
            await self.process_confession(confession_channel, self.user_message)
            
            # The process_confession method already sends a confirmation message
            # Just edit the button message to show success
            embed = discord.Embed(
                title="✅ Server Selected!",
                description=f"Confession posted successfully!",
                color=0x00ff00
            )
            await interaction.edit_original_response(embed=embed, view=None)
        
        return callback
    
    async def process_confession(self, confession_channel, user_message):
        guild_id = confession_channel.guild.id
        key = (user_message.author.id, guild_id)
        now = time.time()
        last = user_last_confession.get(key, 0)
        if now - last < CONFESSION_RATE_LIMIT:
            await user_message.channel.send("⏳ Please wait before sending another confession in this server.")
            return
        user_last_confession[key] = now

        content = user_message.content.strip()
        if not content:
            await user_message.channel.send("❌ Your confession cannot be empty.")
            return
        
        code = get_next_confession_code(guild_id)
        
        embed = discord.Embed(
            title=f"💬 Anonymous Confession #{code:03d}",
            description=content,
            color=0x3498db,
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(text=f"Reply using: DM me 'reply #{code:03d} your message'")
        
        confession_msg = await confession_channel.send(embed=embed)
        await confession_msg.add_reaction("👍")
        await confession_msg.add_reaction("👎")
        
        confession_map = load_confession_map()
        confession_map[str(code)] = user_message.author.id
        save_confession_map(confession_map)
        
        await user_message.channel.send(f"✅ Your confession has been posted anonymously in **{confession_channel.guild.name}**!")
    
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

class ReplySelectView(discord.ui.View):
    def __init__(self, confession_channels, user_message, code, reply_content):
        super().__init__(timeout=60)
        self.confession_channels = confession_channels
        self.user_message = user_message
        self.code = code
        self.reply_content = reply_content
        
        for i, channel in enumerate(confession_channels[:5]):  
            button = discord.ui.Button(
                label=channel.guild.name[:80],
                style=discord.ButtonStyle.secondary,
                custom_id=f"reply_server_{i}"
            )
            button.callback = self.create_callback(i)
            self.add_item(button)
    
    def create_callback(self, index):
        async def callback(interaction):
            if interaction.user.id != self.user_message.author.id:
                await interaction.response.send_message("❌ This is not your reply selection.", ephemeral=True)
                return
            
            confession_channel = self.confession_channels[index]
            await interaction.response.defer()
            
            await self.process_reply(confession_channel, self.user_message, self.code, self.reply_content)
            
            embed = discord.Embed(
                title="✅ Server Selected!",
                description=f"Reply posted successfully!",
                color=0x00ff00
            )
            await interaction.edit_original_response(embed=embed, view=None)
        
        return callback
    
    async def process_reply(self, confession_channel, user_message, code, reply_content):
        confession_message = None
        async for msg in confession_channel.history(limit=100):
            if (msg.author == bot.user and 
                msg.embeds and 
                msg.embeds[0].title and 
                msg.embeds[0].title.startswith(f"💬 Anonymous Confession #{int(code):03d}")):
                confession_message = msg
                break
        
        if confession_message:
            reply_embed = discord.Embed(
                title=f"💬 Anonymous Reply to Confession #{int(code):03d}",
                description=reply_content,
                color=0xe74c3c,
                timestamp=discord.utils.utcnow()
            )
            reply_embed.set_footer(text="This is an anonymous reply")
            
            await confession_channel.send(embed=reply_embed, reference=confession_message)
            await user_message.channel.send(f"✅ Your anonymous reply to confession #{int(code):03d} has been posted in **{confession_channel.guild.name}**!")
            
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
            reply_embed = discord.Embed(
                title=f"💬 Anonymous Reply to Confession #{int(code):03d}",
                description=reply_content,
                color=0xe74c3c,
                timestamp=discord.utils.utcnow()
            )
            reply_embed.set_footer(text="Original confession not found")
            
            await confession_channel.send(embed=reply_embed)
            await user_message.channel.send(f"⚠️ Confession #{int(code):03d} not found in **{confession_channel.guild.name}**. Your reply was posted as a normal message.")
    
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx, channel: discord.TextChannel):
    """Set the confession channel for this server."""
    permissions = channel.permissions_for(ctx.guild.me)
    if not permissions.send_messages:
        await ctx.send("❌ I don't have permission to send messages in that channel. Please give me 'Send Messages' permission.")
        return
    if not permissions.embed_links:
        await ctx.send("❌ I don't have permission to send embeds in that channel. Please give me 'Embed Links' permission.")
        return
    if not permissions.add_reactions:
        await ctx.send("❌ I don't have permission to add reactions in that channel. Please give me 'Add Reactions' permission.")
        return
    
    guild_map = load_guild_map()
    
    existing_channel_id = guild_map.get(str(ctx.guild.id))
    if existing_channel_id:
        existing_channel = bot.get_channel(existing_channel_id)
        if existing_channel:
            await ctx.send(f"⚠️ Confession channel is already set to {existing_channel.mention}.\nChanging it to {channel.mention}...")
        else:
            await ctx.send(f"⚠️ Previous confession channel no longer exists.\nSetting new channel to {channel.mention}...")
    
    guild_map[str(ctx.guild.id)] = channel.id
    save_guild_map(guild_map)
    
    await ctx.send(f"✅ Confession channel set to {channel.mention}")
    
    test_embed = discord.Embed(
        title="🎉 Whispr Setup Complete!",
        description="This server is now ready for anonymous confessions!\n\nUsers can DM me to send confessions and replies.",
        color=0x00ff00
    )
    test_embed.set_footer(text="This is a test message - setup successful!")
    
    await channel.send(embed=test_embed)

@setup.error
async def setup_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need administrator permissions to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Usage: `!setup #channel`\nExample: `!setup #confessions`")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Please mention a valid text channel.\nUsage: `!setup #channel`")
    else:
        await ctx.send("❌ An error occurred during setup. Please try again or contact support.")
        print(f"Setup error: {error}")  

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
        confession_channels = []
        guild_map = load_guild_map()
        
        user_guilds = []
        for guild in bot.guilds:
            try:
                member = await guild.fetch_member(message.author.id)
                if member:
                    user_guilds.append(guild)
            except discord.NotFound:
                continue
            except discord.Forbidden:
                try:
                    member = guild.get_member(message.author.id)
                    if member:
                        user_guilds.append(guild)
                except:
                    continue
            except:
                continue
        
        for guild in user_guilds:
            channel_id = guild_map.get(str(guild.id))
            if channel_id:
                channel = bot.get_channel(channel_id)
                if channel:
                    confession_channels.append(channel)
        
        if not confession_channels:
            await message.channel.send(
                "❌ No confession channel set up in servers where you're a member. Ask an admin to use `!setup #channel` in their server.\n"
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

            if len(confession_channels) > 1:
                embed = discord.Embed(
                    title="🎯 Choose Server for Reply",
                    description=f"You want to reply to confession #{code}. Please select which server:",
                    color=0x3498db
                )
                
                view = ReplySelectView(confession_channels, message, code, reply_content)
                await message.channel.send(embed=embed, view=view)
                return
            else:
                confession_channel = confession_channels[0]
                
                confession_message = None
                async for msg in confession_channel.history(limit=100):
                    if (msg.author == bot.user and 
                        msg.embeds and 
                        msg.embeds[0].title and 
                        msg.embeds[0].title.startswith(f"💬 Anonymous Confession #{int(code):03d}")):
                        confession_message = msg
                        break
                
                if confession_message:
                    reply_embed = discord.Embed(
                        title=f"💬 Anonymous Reply to Confession #{int(code):03d}",
                        description=reply_content,
                        color=0xe74c3c,
                        timestamp=discord.utils.utcnow()
                    )
                    reply_embed.set_footer(text="This is an anonymous reply")
                    
                    await confession_channel.send(embed=reply_embed, reference=confession_message)
                    await message.channel.send(f"✅ Your anonymous reply to confession #{int(code):03d} has been posted in **{confession_channel.guild.name}**!")
                    
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
                    # Create embed for reply when original confession not found
                    reply_embed = discord.Embed(
                        title=f"💬 Anonymous Reply to Confession #{int(code):03d}",
                        description=reply_content,
                        color=0xe74c3c,
                        timestamp=discord.utils.utcnow()
                    )
                    reply_embed.set_footer(text="Original confession not found")
                    
                    await confession_channel.send(embed=reply_embed)
                    await message.channel.send(f"⚠️ Confession #{int(code):03d} not found in **{confession_channel.guild.name}**. Your reply was posted as a normal message.")
                return

        if len(confession_channels) > 1:
            embed = discord.Embed(
                title="🎯 Choose Your Server",
                description="You're in multiple servers with confession channels. Please select which server you want to send your confession to:",
                color=0x3498db
            )
            
            view = ServerSelectView(confession_channels, message)
            await message.channel.send(embed=embed, view=view)
            return
        
        confession_channel = confession_channels[0]

        # For single server, process confession directly without creating a view
        guild_id = confession_channel.guild.id
        key = (message.author.id, guild_id)
        now = time.time()
        last = user_last_confession.get(key, 0)
        if now - last < CONFESSION_RATE_LIMIT:
            await message.channel.send("⏳ Please wait before sending another confession in this server.")
            return
        user_last_confession[key] = now

        content = message.content.strip()
        if not content:
            await message.channel.send("❌ Your confession cannot be empty.")
            return
        
        code = get_next_confession_code(guild_id)
        
        # Create embed for confession to prevent @everyone pings
        embed = discord.Embed(
            title=f"💬 Anonymous Confession #{code:03d}",
            description=content,
            color=0x3498db,
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(text=f"Reply using: DM me 'reply #{code:03d} your message'")
        
        confession_msg = await confession_channel.send(embed=embed)
        await confession_msg.add_reaction("👍")
        await confession_msg.add_reaction("👎")
        
        confession_map = load_confession_map()
        confession_map[str(code)] = message.author.id
        save_confession_map(confession_map)
        
        await message.channel.send(f"✅ Your confession has been posted anonymously in **{confession_channel.guild.name}**!")

    await bot.process_commands(message)

@bot.command(name="whisprhelp")
async def whisprhelp(ctx):
    """Show help for Whispr bot."""
    help_text = (
        "**Whispr Bot Help**\n"
        "• `!setup #channel` — Set the confession channel (admin only).\n"
        "• DM me your message — Send an anonymous confession.\n"
        "• DM me `reply #001 your message` — Reply anonymously to confession #001.\n"
        "• Wait 30 seconds between confessions per server.\n"
        "• Confessions and replies are anonymous.\n"
        "• Only server admins can run `!setup`.\n"
        "• If you need more help, contact your server admin."
    )
    await ctx.send(help_text)

@bot.command(name="status")
@commands.has_permissions(administrator=True)
async def status(ctx):
    """Check if confession channel is set up for this server (admin only)."""
    guild_map = load_guild_map()
    channel_id = guild_map.get(str(ctx.guild.id))
    
    if not channel_id:
        await ctx.send("❌ No confession channel set up for this server.\nUse `!setup #channel` to set one up.")
        return
    
    channel = bot.get_channel(channel_id)
    if not channel:
        await ctx.send("❌ Confession channel was set but no longer exists.\nUse `!setup #channel` to set a new one.")
        return
    
    permissions = channel.permissions_for(ctx.guild.me)
    missing_perms = []
    if not permissions.send_messages:
        missing_perms.append("Send Messages")
    if not permissions.embed_links:
        missing_perms.append("Embed Links")
    if not permissions.add_reactions:
        missing_perms.append("Add Reactions")
    
    if missing_perms:
        await ctx.send(f"⚠️ Confession channel: {channel.mention}\n❌ Missing permissions: {', '.join(missing_perms)}")
    else:
        await ctx.send(f"✅ Confession channel: {channel.mention}\n✅ All permissions are correct!")

@status.error
async def status_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need administrator permissions to use this command.")

bot.run(TOKEN)