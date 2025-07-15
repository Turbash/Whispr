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

### 3. Deploy
- Click **"Create Web Service"**.
- Wait for the build and deploy to finish.

### 4. Keeping the Bot Active

- **Render free tier** services may sleep after 15 minutes of inactivity.
- There is no official way to keep a free Render service always online.
- Some users use free uptime monitoring services (like [UptimeRobot](https://uptimerobot.com/) or [Freshping](https://freshping.io/)) to "ping" their bot's web endpoint regularly.  
  > **Note:** This may violate Render's free tier policy and is not officially supported. Use at your own risk.
- If your bot sleeps, you can restart it from the Render dashboard by clicking **"Manual Deploy" > "Deploy latest commit"** or by toggling the service off and on.
- For 24/7 uptime, consider upgrading to a paid plan or using a VPS.

#### Alternative Hosting Options

- **Railway** ([railway.app](https://railway.app/)):  
  Offers a generous free tier and can keep bots alive longer than Render, but may still have usage limits.
- **Fly.io** ([fly.io](https://fly.io/)):  
  Free tier with global deployment. You can deploy your bot as a Docker or Python app, and it will stay online as long as you stay within the free resource limits.  
  See [Fly.io Getting Started](https://fly.io/docs/getting-started/python/) for details.
- **Pella** ([pella.dev](https://pella.dev/)):  
  Pella is a new cloud platform focused on running bots and background workers. It offers a free tier and is designed to keep bots like Discord bots online 24/7, even on the free plan (subject to their fair use policy).  
  See [Pella Docs](https://docs.pella.dev/) for setup instructions.
- **A VPS provider** (like [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/), [Google Cloud Free Tier](https://cloud.google.com/free), [AWS Free Tier](https://aws.amazon.com/free/)):  
  You can run your bot 24/7 for free within resource limits.  
  **Google Cloud will work**—your friend can deploy the bot on a Google Cloud VM or App Engine, and it will stay online as long as the instance is running and within the free tier limits.
- **Glitch** ([glitch.com](https://glitch.com/)):  
  Good for prototyping, but projects may sleep after some time.
- **Replit** ([replit.com](https://replit.com/)):  
  Free tier projects may sleep, but paid plans can keep your bot always online.

> For true 24/7 uptime on a free plan, a VPS (like Oracle Cloud Free Tier), Fly.io, or Pella (within free limits) are the most reliable options.

### 5. Re-deploying or Restarting

- Any time you push new code to GitHub, Render will auto-deploy.
- You can also manually trigger a deploy from the Render dashboard.

---

**Your bot will now run 24/7 (on paid plans) or wake up when needed (on free plans).**

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

