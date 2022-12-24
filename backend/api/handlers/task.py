from typing import Any

from aiohttp import web

from backend.app.errors import OutdatedRevisionError, NonExistentTaskIDError
from backend.interfaces import TaskService
from .base import ProtectedHandler
from ..models import AddTasksRequest, UpdateTaskRequest, UpdateTasksRequest


class BaseTaskHandler(ProtectedHandler):
    @property
    def service(self) -> TaskService:
        return self.request.app['task_service']


class GetTasksHandler(BaseTaskHandler):
    PATH = '/api/tasks'

    async def get(self) -> tuple[int, Any]:
        tasks, revision = await self.service.get_tasks(self.user_id)
        for i, task in enumerate(tasks):
            tasks[i] = task.dict()
        return web.HTTPOk.status_code, {'list': tasks, 'revision': revision}


class GetTaskHandler(BaseTaskHandler):
    PATH = '/api/tasks/{id}'

    async def get(self) -> tuple[int, Any]:
        task_id = self.request.match_info['id']
        try:
            task, revision = await self.service.get_task(self.user_id, task_id)
        except NonExistentTaskIDError:
            return web.HTTPNotFound.status_code, None
        return web.HTTPOk.status_code, {'element': task.dict(), 'revision': revision}


class AddTasksHandler(BaseTaskHandler):
    PATH = '/api/tasks'

    async def post(self) -> tuple[int, Any]:
        body = await self.request.json()
        data = AddTasksRequest(**body)
        try:
            revision = await self.service.add_tasks(self.user_id, data.list, data.revision)
        except OutdatedRevisionError as e:
            return web.HTTPConflict.status_code, {'revision': e.actual}
        return web.HTTPCreated.status_code, {'revision': revision}


class DeleteTaskHandler(BaseTaskHandler):
    PATH = '/api/tasks/{id}'

    async def delete(self) -> tuple[int, Any]:
        task_id = self.request.match_info['id']
        revision = await self.service.delete_task(self.user_id, task_id)
        return web.HTTPOk.status_code, {'revision': revision}


class UpdateTaskHandler(BaseTaskHandler):
    PATH = '/api/tasks'

    async def put(self) -> tuple[int, Any]:
        body = await self.request.json()
        data = UpdateTaskRequest(**body)
        revision = await self.service.update_task(self.user_id, data.element)
        return web.HTTPOk.status_code, {'revision': revision}


class UpdateTasksHandler(BaseTaskHandler):
    PATH = '/api/tasks'

    async def patch(self) -> tuple[int, Any]:
        body = await self.request.json()
        data = UpdateTasksRequest(**body)
        try:
            revision = await self.service.update_tasks(self.user_id, data.list, data.revision)
        except OutdatedRevisionError as e:
            return web.HTTPConflict.status_code, {'revision': e.actual}
        return web.HTTPOk.status_code, {'revision': revision}
