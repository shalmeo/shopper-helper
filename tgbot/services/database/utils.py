from tgbot import config


def get_connection_string(db: config.Database, async_fallback: bool = False) -> str:
    result = (
        f"postgresql+asyncpg://{db.login}:{db.password}@{db.host}:{db.port}/{db.name}"
    )
    
    if async_fallback:
        result += "?async_fallback=True"

    return result
