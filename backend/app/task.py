from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncEngine

from backend import interfaces
from backend.models import Task
from .errors import NonExistentTaskIDError


class TaskService(interfaces.TaskService):
    def __init__(self, engine: AsyncEngine, repo: interfaces.TaskRepository):
        self._engine = engine
        self._repo = repo

    async def get_tasks(self, user_id: str) -> tuple[list[Task], int]:
        async with self._engine.begin() as conn:
            curr_revision = await self._repo.get_revision(conn, user_id)
            if curr_revision is None:
                curr_revision = 0
                await self._repo.set_init_revision(conn, user_id)
            tasks = await self._repo.get_tasks(conn, user_id)
        return tasks, curr_revision

    async def get_task(self, user_id: str, task_id: UUID4) -> tuple[Task, int]:
        async with self._engine.begin() as conn:
            curr_revision = await self._repo.get_revision(conn, user_id)
            task = await self._repo.get_task(conn, user_id, task_id)
            if task is None:
                raise NonExistentTaskIDError(task_id)
        return task, curr_revision
