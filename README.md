# Whispr - Anonymous Confession & Reply Discord Bot

Whispr is a Discord bot that allows users to send anonymous confessions and replies in your server.

## Features

- **Anonymous confessions via DM** - Users can DM the bot to send anonymous confessions
- **Anonymous replies to confessions** - Users can reply to specific confessions anonymously
- **Interactive server selection** - Easy-to-use buttons when users are in multiple servers
- **Per-server confession channels and numbering** - Each server has its own confession channel and numbering system
- **Smart member detection** - Only shows confession channels for servers where the user is a member
- **Admin setup via Discord command** - No code editing required, admins can set up via `!setup`
- **Per-server rate limiting** - Users can confess once every 30 seconds per server
- **Reply notifications** - Original confessors get notified when their confession receives a reply
- **Auto-onboarding** - Bot introduces itself when joining new servers
- **Easy to use and configure** - Simple commands and clear error messages

## Setup Instructions

1. **Clone this repository** and enter the directory.

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Create a `.env` file** in this directory with your bot token:
   ```
   TOKEN=your_discord_bot_token
   ```

4. **Run the bot:**
   ```
   python bot.py
   ```

5. **Invite the bot to your Discord server** using the OAuth2 URL from the Discord Developer Portal.  
   Make sure to give it permissions to read/send messages, add reactions, and read message history.

6. **Set up the confession channel:**
   - As a server admin, type:
     ```
     !setup #your-confession-channel
     ```
     (Replace `#your-confession-channel` with the actual channel mention.)

7. **Get help:**
   - Type `!whisprhelp` in your server for usage instructions.

## Usage

- **Send a confession:**  
  DM the bot your message. If you're in multiple servers with confession channels, you'll get interactive buttons to choose which server to confess in.

- **Reply to a confession:**  
  DM the bot:
  ```
  reply #001 your reply message
  ```
  or
  ```
  reply 001 your reply message
  ```
  (Replace `001` with the confession number.)
  
  For multiple servers, you'll get buttons to choose which server to reply in.

- **Multi-server support:**  
  If you're in multiple servers with Whispr set up, the bot will show you interactive buttons to choose which server you want to confess or reply in.

- **Rate limiting:**  
  Users must wait 30 seconds between confessions per server (you can confess in different servers independently).

- **Help:**  
  Use `!whisprhelp` in your server for a summary of commands.

## Admin Commands

- `!setup #channel` — Set the confession channel for your server (admin only).
- `!whisprhelp` — Show help and usage instructions.

## How to Add Whispr to Your Server

1. **Use the invite link below:**  
   Anyone can use this link to add Whispr to their server:

   **Demo Invite Link:**  
   [Click here to invite Whispr to your server](https://discord.com/oauth2/authorize?client_id=1390659226401116341&permissions=75840&integration_type=0&scope=bot)

2. **After inviting:**  
   - The bot will automatically introduce itself and provide setup instructions in your server.
   - An admin should run `!setup #channel` in their server to set the confession channel.
   - Users can then DM the bot to send confessions and replies.
   - Use `!whisprhelp` for detailed usage instructions.

## Deploying on Render

You can deploy Whispr on [Render](https://render.com/) for free. Here’s how:

### 1. Push Your Code to GitHub
- Make sure your bot code is in a GitHub repository.

### 2. Create a New Web Service on Render
- Go to [Render Dashboard](https://dashboard.render.com/).
- Click **"New +"** and select **"Web Service"**.
- Connect your GitHub repo.
- For **Environment**, select **Python**.
- For **Build Command**, use:
  ```
  pip install -r requirements.txt
  ```
- For **Start Command**, use:
  ```
  python bot.py
  ```
- Add an environment variable:
  - Key: `TOKEN`
  - Value: *your Discord bot token*

## Notes

- **All confessions and replies are completely anonymous** - The bot never reveals user identities publicly.
- **Multi-server support** - The bot works across multiple servers with independent confession channels and numbering.
- **Smart server detection** - Users only see confession options for servers where they're actually members.
- **Interactive interface** - Easy-to-use buttons for server selection when users are in multiple servers.
- **Persistent data** - Data is stored in JSON files in the bot directory. Make sure your deployment preserves these files for persistent operation.
- **Reply notifications** - Original confessors are privately notified when their confessions receive replies (without revealing the replier's identity).

---

**🎉 Enjoy anonymous confessions with Whispr! 🎉**

## Contributing

Feel free to fork this repository and submit pull requests for improvements or new features!

