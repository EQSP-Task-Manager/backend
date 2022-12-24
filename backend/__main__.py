import logging

from aiohttp import web

from .api import register_handlers

logger = logging.getLogger(__name__)


def main():
    app = web.Application()
    register_handlers(app.router)
    web.run_app(app, host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()
