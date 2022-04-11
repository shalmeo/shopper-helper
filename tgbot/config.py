from dataclasses import dataclass

from environs import Env


@dataclass
class Database:
    login: str
    password: str
    host: str
    port: int
    name: str


@dataclass
class Redis:
    password: str
    host: str
    port: int


@dataclass
class Bot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class Config:
    bot: Bot
    db: Database
    redis: Redis


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        bot=Bot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=Database(
            login=env.str('DB_LOGIN'),
            password=env.str('DB_PASS'),
            host=env.str('DB_HOST'),
            port=env.int('DB_PORT'),
            name=env.str('DB_NAME'),
        ),
        redis=Redis(
            password=env.str('REDIS_PASS'),
            host=env.str('REDIS_HOST'),
            port=env.str('REDIS_PORT')
        )
    )
