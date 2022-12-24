from typing import Any

from aiohttp import web

from .base import BaseHandler


class PingHandler(BaseHandler):
    PATH = '/api/ping'

    async def get(self) -> tuple[int, Any]:
        return web.HTTPOk.status_code, None
