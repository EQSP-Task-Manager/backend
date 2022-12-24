from aiohttp import web

from .handlers import (
    PingHandler,
    GetTasksHandler, GetTaskHandler,
    AddTasksHandler, DeleteTaskHandler,
    UpdateTaskHandler, UpdateTasksHandler
)
from .middlewares import logging_middleware, error_middleware, auth_middleware, encoding_middleware

MIDDLEWARES = [logging_middleware, error_middleware, auth_middleware, encoding_middleware]


def register_handlers(router: web.UrlDispatcher):
    router.add_get(PingHandler.PATH, PingHandler)
    router.add_get(GetTasksHandler.PATH, GetTasksHandler)
    router.add_get(GetTaskHandler.PATH, GetTaskHandler)
    router.add_post(AddTasksHandler.PATH, AddTasksHandler)
    router.add_delete(DeleteTaskHandler.PATH, DeleteTaskHandler)
    router.add_put(UpdateTaskHandler.PATH, UpdateTaskHandler)
    router.add_patch(UpdateTasksHandler.PATH, UpdateTasksHandler)


__all__ = ('MIDDLEWARES', 'register_handlers')
