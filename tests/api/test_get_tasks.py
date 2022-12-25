from unittest.mock import Mock, AsyncMock

import pytest
from aiohttp.test_utils import TestClient

from backend.models import Task, TaskImportance, UserInfo

DEVICE_ID = 'df963423-9585-4423-b4d7-853af30b029f'
OAUTH_TOKEN = 'y0_AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
USER_INFO = UserInfo(
    id='555555555',
    login='test-login',
    client_id='26826a430e2b4f3b8f8c002d8794f371',
    display_name='Ivan Ivanov',
    real_name='Ivan Ivanov',
    first_name='Ivan',
    last_name='Ivanov',
    sex='male',
    default_avatar_id='0/0-0',
    is_avatar_empty=True,
    psuid='AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
)


test_data = [
    (
        '1',
        [
            Task(
                id='6ef08e6c-586d-4062-ba8d-1a6c79b062dc',
                title='Test task title',
                description='Test task description',
                done=False,
                tags=[],
                created_at=1671958915,
                changed_at=1671958915
            )
        ],
        1,
        {
            'list': [
                {
                    'id': '6ef08e6c-586d-4062-ba8d-1a6c79b062dc',
                    'title': 'Test task title',
                    'description': 'Test task description',
                    'done': False,
                    'tags': [],
                    'created_at': 1671958915,
                    'changed_at': 1671958915,
                    'importance': TaskImportance.BASIC.value,
                    'deadline': None,
                    'color': None
                }
            ],
            'revision': 1
        }
    )
]


@pytest.mark.parametrize('user_id,stub_tasks,stub_revision,expected', test_data)
async def test_get_tasks(
        client: TestClient,
        user_id: str,
        stub_tasks: list[Task],
        stub_revision: int,
        expected: dict
):
    auth_service: Mock = client.app['auth_service']
    auth_service.get_user_info = AsyncMock()
    auth_service.get_user_info.return_value = USER_INFO

    task_service: Mock = client.app['task_service']
    task_service.get_tasks = AsyncMock()
    task_service.get_tasks.return_value = (stub_tasks, stub_revision)

    headers = {
        'X-Device-Id': DEVICE_ID,
        'Authorization': f'OAuth {OAUTH_TOKEN}'
    }

    response = await client.get('/api/tasks', headers=headers)
    response_json = await response.json()

    assert response.status == 200
    assert response_json == expected
