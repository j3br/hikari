import os
import sys
from dataclasses import dataclass, field

@dataclass
class ILOAuth:
    username: str = os.environ.get("ILO_USER")
    password: str = os.environ.get("ILO_PASS")

@dataclass
class ILOSettings:
    auth : ILOAuth = field(default_factory=ILOAuth)
    base_url: str = os.environ.get("ILO_URL")
    verify_ssl: bool = os.getenv('ILO_VERIFY_SSL', 'False') == 'True'

@dataclass
class DiscordSettings:
    token: str = os.environ.get("DISCORD_TOKEN")
    channel_id : str = os.environ.get("CHANNEL_ID")

@dataclass
class Settings:
    ilo: ILOSettings = field(default_factory=ILOSettings)
    discord: DiscordSettings = field(default_factory=DiscordSettings)
