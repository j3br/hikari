import json
import logging
import os
from hikari.config import Settings, ILOAuth, ILOSettings, DiscordSettings

logger = logging.getLogger(__name__)


def format_code_block(string):
    return f"```\n{string}\n```"


def handle_error_response(response, state):
    message = ""

    if response.status_code >= 400 and response.status_code < 500:
        extended_info = (
            response.json().get("error", {}).get("@Message.ExtendedInfo", [])
        )
        message = format_code_block(json.dumps(extended_info, indent=2, sort_keys=True))

    elif response.status_code != 200:
        message = format_code_block(
            f"An error occurred during the HTTP request: {response.status_code}"
        )
    return f"Failed to initiate power {state}" + message


def check_env_vars(required_env_vars: list) -> bool:
    if all(os.getenv(var_name) is not None for var_name in required_env_vars):
        return True
    else:
        missing_variables = [
            var_name for var_name in required_env_vars if os.getenv(var_name) is None
        ]
        logger.error(
            "One or more required environment variables is not set: %s",
            ", ".join(missing_variables),
        )
        return False


def get_env_var(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def get_bool_env_var(name: str, default: str = "False") -> bool:
    return os.getenv(name, default).lower() in ["true", "1", "yes"]


def load_settings_from_env() -> Settings:
    ilo_auth = ILOAuth(
        username=get_env_var("ILO_USER"), password=get_env_var("ILO_PASS")
    )

    ilo_settings = ILOSettings(
        auth=ilo_auth,
        base_url=get_env_var("ILO_URL"),
        verify_ssl=get_bool_env_var("ILO_VERIFY_SSL", "False"),
    )

    discord_settings = DiscordSettings(
        token=get_env_var("DISCORD_TOKEN"), channel_id=get_env_var("CHANNEL_ID")
    )

    return Settings(ilo=ilo_settings, discord=discord_settings)
