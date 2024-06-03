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


@dataclass
class DiscordSettings:
    token: str
    channel_id: str


@dataclass
class Settings:
    ilo: ILOSettings
    discord: DiscordSettings
