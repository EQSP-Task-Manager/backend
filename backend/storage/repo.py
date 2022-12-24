from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.sql import select, insert, update, delete, and_

from backend import interfaces
from backend.models import Task
from .db.schema import tasks_table, revisions_table


class TaskRepository(interfaces.TaskRepository):
    async def get_tasks(self, conn: AsyncConnection, user_id: str) -> list[Task]:
        query = select([
            tasks_table.c.uuid,
            tasks_table.c.title,
            tasks_table.c.description,
            tasks_table.c.done,
            tasks_table.c.importance,
            tasks_table.c.tags,
            tasks_table.c.created_at,
            tasks_table.c.changed_at,
            tasks_table.c.deadline,
            tasks_table.c.color,
        ]).where(tasks_table.c.user_id == user_id).order_by(tasks_table.c.id)

        result = await conn.execute(query)
        rows = result.fetchall()

        return [
            Task(
                id=row.uuid,
                title=row.title,
                description=row.description,
                done=row.done,
                importance=row.importance,
                tags=row.tags,
                created_at=row.created_at,
                changed_at=row.changed_at,
                deadline=row.deadline,
                color=row.color
            )
            for row in rows
        ]

    async def get_task(self, conn: AsyncConnection, user_id: str, task_id: UUID4) -> Task | None:
        query = select([
            tasks_table.c.uuid,
            tasks_table.c.title,
            tasks_table.c.description,
            tasks_table.c.done,
            tasks_table.c.importance,
            tasks_table.c.tags,
            tasks_table.c.created_at,
            tasks_table.c.changed_at,
            tasks_table.c.deadline,
            tasks_table.c.color,
        ]).where(
            and_(
                tasks_table.c.user_id == user_id,
                tasks_table.c.uuid == str(task_id)
            )
        )
        result = await conn.execute(query)
        row = result.fetchone()
        if row is None:
            return None
        return Task(
            id=row.uuid,
            title=row.title,
            description=row.description,
            done=row.done,
            importance=row.importance,
            tags=row.tags,
            created_at=row.created_at,
            changed_at=row.changed_at,
            deadline=row.deadline,
            color=row.color
        )

    async def get_revision(self, conn: AsyncConnection, user_id: str) -> int | None:
        query = select([revisions_table.c.revision]).where(revisions_table.c.user_id == user_id)
        result = await conn.execute(query)
        row = result.fetchone()
        if row is not None:
            return row.revision
        return None

    async def add_task(self, conn: AsyncConnection, user_id: str, task: Task) -> int:
        query = insert(tasks_table).values(
            uuid=str(task.id),
            user_id=user_id,
            title=task.title,
            description=task.description,
            done=task.done,
            importance=task.importance.value,
            tags=task.tags,
            created_at=task.created_at,
            changed_at=task.changed_at,
            deadline=task.deadline,
            color=task.color,
        )
        result = await conn.execute(query)
        return result.inserted_primary_key.id

    async def set_init_revision(self, conn: AsyncConnection, user_id: str):
        query = insert(revisions_table).values(user_id=user_id, revision=0)
        await conn.execute(query)

    async def increment_revision(self, conn: AsyncConnection, user_id: str):
        query = update(revisions_table).where(
            revisions_table.c.user_id == user_id
        ).values(revision=revisions_table.c.revision + 1)
        await conn.execute(query)

    async def delete_task(self, conn: AsyncConnection, user_id: str, task_id: UUID4):
        query = delete(tasks_table).where(
            and_(
                tasks_table.c.user_id == user_id,
                tasks_table.c.uuid == str(task_id)
            )
        )
        result = await conn.execute(query)
        return result.rowcount != 0

    async def update_task(self, conn: AsyncConnection, user_id: str, task: Task) -> bool:
        query = update(tasks_table).where(
            and_(
                tasks_table.c.user_id == user_id,
                tasks_table.c.uuid == str(task.id)
            )
        ).values(
            title=task.title,
            description=task.description,
            done=task.done,
            importance=task.importance.value,
            tags=task.tags,
            created_at=task.created_at,
            changed_at=task.changed_at,
            deadline=task.deadline,
            color=task.color
        )
        result = await conn.execute(query)
        return result.rowcount != 0

    async def delete_tasks(self, conn: AsyncConnection, user_id: str) -> int:
        query = delete(tasks_table).where(tasks_table.c.user_id == user_id)
        result = await conn.execute(query)
        return result.rowcount

    async def add_tasks(self, conn: AsyncConnection, user_id: str, tasks: list[Task]):
        query = insert(tasks_table).values(user_id=user_id)
        values = [
            {
                'uuid': str(task.id),
                'title': task.title,
                'description': task.description,
                'done': task.done,
                'importance': task.importance.value,
                'tags': task.tags,
                'created_at': task.created_at,
                'changed_at': task.changed_at,
                'deadline': task.deadline,
                'color': task.color
            }
            for task in tasks
        ]
        await conn.execute(query, values)
