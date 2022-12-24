from aiohttp import web

from backend.models import UserInfo

DEVICE_ID_HEADER = "X-Device-Id"


class BaseHandler(web.View):
    def __init__(self, request: web.Request):
        super().__init__(request)
        if request.headers.get(DEVICE_ID_HEADER) is None:
            raise web.HTTPForbidden(text=f'{DEVICE_ID_HEADER} header is not provided')
        self._device_id = request.headers[DEVICE_ID_HEADER]

    @property
    def device_id(self) -> str:
        return self._device_id


class ProtectedHandler(BaseHandler):
    def __init__(self, request: web.Request):
        super().__init__(request)
        if not hasattr(request, '_user_info'):
            raise web.HTTPUnauthorized()
        self._user_info = getattr(request, '_user_info')

    @property
    def user_info(self) -> UserInfo:
        return self._user_info

    @property
    def user_id(self) -> str:
        return self.user_info.id
