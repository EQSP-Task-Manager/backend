from unittest.mock import Mock

import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer

from backend.api import register_handlers, MIDDLEWARES


def create_stubs(app: web.Application):
    app['task_service'] = Mock()
    app['auth_service'] = Mock()


async def create_app() -> web.Application:
    app = web.Application(middlewares=MIDDLEWARES)
    create_stubs(app)
    register_handlers(app.router)
    return app


@pytest.fixture
async def client() -> TestClient:
    app = await create_app()
    test_server = TestServer(app)
    test_client = TestClient(test_server)
    await test_client.start_server()
    try:
        yield test_client
    finally:
        await test_client.close()
