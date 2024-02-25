from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    chats: list[int]
    use_redis: bool
    api_alert: str
    rtsp_url: str


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            chats=list(map(int, env.list("CHATS"))),
            use_redis=env.bool("USE_REDIS"),
            api_alert=env.str("API_ALERT"),
            rtsp_url=env.str("RTSP_URL")
        ),
        misc=Miscellaneous()
    )
