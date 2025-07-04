# Whispr - Anonymous Confession & Reply Discord Bot

Whispr is a Discord bot that allows users to send anonymous confessions and replies in your server.

## Features

- Anonymous confessions via DM
- Anonymous replies to confessions via DM
- Per-server confession channels and numbering
- Admin setup via Discord command
- Rate limiting to prevent spam
- Notifies confessors of replies
- Easy to use and configure

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
  DM the bot your message. It will be posted anonymously in the confession channel.

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

- **Rate limiting:**  
  Users must wait 30 seconds between confessions.

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
   - An admin should run `!setup #channel` in their server to set the confession channel.
   - Users can then DM the bot to send confessions and replies.

## Submitting as a Project

Whispr is designed to be an easy drop-in solution for anonymous confessions in Discord servers. To submit this as a project:

- Ensure your bot is running smoothly and can handle basic commands.
- Prepare a demo server where we can see Whispr in action.
- Submit your project link along with a brief description and any relevant details.

## Notes

- All confessions and replies are anonymous.
- The bot supports multiple servers, each with their own confession channel and numbering.
- Data is stored in JSON files in the bot directory. Make sure your deployment preserves these files for persistent operation.

---

Enjoy anonymous confessions with Whispr!
---

