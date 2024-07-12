from dataclasses import dataclass


@dataclass
class ILOAuth:
    username: str
    password: str


@dataclass
class ILOSettings:
    auth: ILOAuth
    base_url: str
    verify_ssl: bool

    def __post_init__(self):
        if not self.base_url.startswith("http"):
            raise ValueError("Invalid base_url, must start with 'http' or 'https'")



@dataclass
class DiscordSettings:
    token: str
    channel_id: str

    def __post_init__(self):
        if not self.channel_id.isdigit():
            raise ValueError("Invalid channel_id, must be numeric")



@dataclass
class Settings:
    ilo: ILOSettings
    discord: DiscordSettings
