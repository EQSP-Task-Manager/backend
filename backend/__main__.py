import logging
from functools import partial

from aiohttp import web
from sqlalchemy.ext.asyncio import create_async_engine

from .api import register_handlers, MIDDLEWARES
from .config import parse_config, Config
from .logger import setup_logger

logger = logging.getLogger(__name__)


async def setup(db_config: Config.DB):
    db_url = 'postgresql+asyncpg://{}:{}@{}:{}/{}'
    db_url = db_url.format(db_config.user, db_config.password, db_config.host, db_config.port, db_config.name)
    db_engine = create_async_engine(db_url)
    yield
    await db_engine.close()


def main():
    config = parse_config()
    setup_logger(config.log_level)
    app = web.Application(middlewares=MIDDLEWARES)
    register_handlers(app.router)
    app.cleanup_ctx.append(partial(setup, db_config=config.db))
    web.run_app(app, host=config.api.host, port=config.api.port)


if __name__ == '__main__':
    main()
