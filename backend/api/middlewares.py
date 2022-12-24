import json
import logging
from datetime import datetime
from enum import Enum
from typing import Any, Callable
from uuid import UUID

from aiohttp import web
from pydantic import ValidationError

from backend.app.errors import InvalidOAuthToken, ExtServiceError, ExtServiceUnexpectedResponseError
from backend.interfaces import AuthService

logger = logging.getLogger(__name__)


@web.middleware
async def logging_middleware(request: web.Request, handler: Callable) -> web.Response:
    response: web.Response = await handler(request)
    log_message = ' '.join([
        f'method={request.method}',
        f'uri={request.path}',
        f'status={response.status}'
    ])
    if response.status >= 500:
        logger.error(log_message)
    elif response.status >= 400:
        logger.info(log_message)
    return response


@web.middleware
async def error_middleware(request: web.Request, handler: Callable) -> web.Response:
    try:
        return await handler(request)
    except ValidationError as e:
        return web.json_response(status=web.HTTPBadRequest.status_code, data={'validation_error': e.errors()})
    except (ExtServiceError, ExtServiceUnexpectedResponseError) as e:
        logger.exception(e)
        return web.Response(status=web.HTTPServiceUnavailable.status_code)
    except web.HTTPException as e:
        return web.Response(status=e.status_code)
    except Exception as e:
        logger.exception(e, exc_info=True)
        return web.Response(status=web.HTTPInternalServerError.status_code)


@web.middleware
async def auth_middleware(request: web.Request, handler: Callable) -> web.Response:
    auth_service: AuthService = request.app['auth_service']
    auth_header = request.headers.get('Authorization')
    if auth_header is not None:
        parts = auth_header.split(' ')
        if len(parts) == 2 and parts[0] == 'OAuth':
            oauth_token = parts[1]
            try:
                request._user_info = await auth_service.get_user_info(oauth_token)
            except InvalidOAuthToken:
                return web.Response(status=web.HTTPUnauthorized.status_code)
    return await handler(request)


@web.middleware
async def encoding_middleware(request: web.Request, handler: Callable) -> web.Response:
    class Encoder(json.JSONEncoder):
        def default(self, o: Any) -> Any:
            if isinstance(o, datetime):
                return int(o.timestamp())
            if isinstance(o, Enum):
                return o.value
            if isinstance(o, UUID):
                return str(o)
            return super().default(o)

    status, data = await handler(request)
    if data is not None:
        encoded_data = json.dumps(data, cls=Encoder)
        return web.Response(body=encoded_data, status=status, content_type='application/json')
    return web.Response(status=status)
