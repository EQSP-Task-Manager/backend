from aiohttp import web

from .handlers import PingHandler


def register_handlers(router: web.UrlDispatcher):
    router.add_view(PingHandler.PATH, PingHandler)
