# Hikari
光 - Hikari | A Discord Bot for power-cycling a HPE server via iLO ⚡


## Build and run the image

```bash
docker build -t hikari .

docker run --name hikari \
  -e ILO_URL=https://<ilo-url> \
  -e ILO_USER=<ilo-username> \
  -e ILO_PASS=<ilo-password> \
  -e ILO_VERIFY_SSL=<True | False>
  -e DISCORD_TOKEN=<discord-bot-token> \
  -e CHANNEL_ID=<discord-channel-id>
  -d hikari
```
The `CHANNEL_ID` will limit the bot to only respond in that channel.

Set `ILO_VERIFY_SSL` to `False` if you get request errors related to self-signed certificate or similar.

## Commands
- `!start`  - Sends a power on request
- `!stop`   - Sends a power off request
- `!status` - Returns the current power state

Please refer to https://discord.com/developers/docs for information and instructions on how to setup your Discord Application & Bot.

### 🌟 Acknowledgements
Heavily influenced by [Kerwood - Discord-ilo-bot](https://github.com/Kerwood/discord-ilo-bot)