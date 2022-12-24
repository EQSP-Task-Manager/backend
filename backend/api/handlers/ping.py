from aiohttp import web


class PingHandler(web.View):
    PATH = '/api/ping'

    async def get(self) -> web.Response:
        return web.Response(status=web.HTTPOk.status_code)
