import discord
import logging
import sys
from hikari.ilo.client import APIClient
from hikari.utils import check_env_vars, load_settings_from_env


REQUIRED_ENVIRONMENT_VARS = [
    "ILO_URL",
    "ILO_USER",
    "ILO_PASS",
    "DISCORD_TOKEN",
    "CHANNEL_ID",
]

# Set up logging
logger = logging.getLogger("discord")


def create_discord_client(settings, ilo_client) -> discord.Client:
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"Connected as {client.user}")

    @client.event
    async def on_message(message):
        if (
            message.author == client.user
            or str(message.channel.id) != settings.discord.channel_id
        ):
            return

        if message.content.lower() == "!status":
            state = ilo_client.actions.power.status
            response = (
                f"Current power state: **{state.upper()}**"
                if state
                else "Unable to determine current power state"
            )
            await message.channel.send(response)

        elif message.content.lower() == "!start":
            result = ilo_client.actions.power.on
            await message.channel.send(result)

        elif message.content.lower() == "!stop":
            result = ilo_client.actions.power.off
            await message.channel.send(result)

    return client


def main():

    # Verify that the required environment variables are set
    if not check_env_vars(REQUIRED_ENVIRONMENT_VARS):
        sys.exit(1)

    # Load settings from environment variables
    settings = load_settings_from_env()

    # Initialize ILO API client
    ilo_client = APIClient(
        base_url=settings.ilo.base_url,
        auth=settings.ilo.auth,
        verify_ssl=settings.ilo.verify_ssl,
    )

    # Set up Discord client
    discord_client = create_discord_client(settings, ilo_client)
    discord_client.run(settings.discord.token)


if __name__ == "__main__":
    main()
