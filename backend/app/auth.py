from aiohttp import ClientSession

from backend.models import UserInfo
from .errors import ExtServiceError, InvalidOAuthToken, ExtServiceUnexpectedResponseError

YANDEX_AUTH_SERVICE = 'login.yandex.ru'


class AuthService:
    def __init__(self):
        self._session = ClientSession()

    async def get_user_info(self, oauth_token: str) -> UserInfo:
        """
        Authenticates user by checking passed OAuth token through Yandex API
        """

        url = 'https://login.yandex.ru/info'
        params = {
            'format': 'json',
            'oauth_token': oauth_token
        }
        response = await self._session.get(url, params=params)
        if response.status != 200:
            if response.status == 401:
                raise InvalidOAuthToken()
            elif response.status >= 500:
                raise ExtServiceError(YANDEX_AUTH_SERVICE, response)
            else:
                raise ExtServiceUnexpectedResponseError(YANDEX_AUTH_SERVICE, response)
        data = await response.json()
        return UserInfo(**data)

    async def close(self):
        await self._session.close()
