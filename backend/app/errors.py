from aiohttp import ClientResponse
from pydantic import UUID4


class DomainError(Exception):
    pass


class OutdatedRevisionError(DomainError):
    def __init__(self, passed_revision: int, actual_revision: int):
        self.got = passed_revision
        self.actual = actual_revision
        super().__init__(f'outdated revision: {self.got}, actual revision: {self.actual}')


class NonExistentTaskIDError(DomainError):
    def __init__(self, task_id: UUID4):
        self.task_id = task_id
        super().__init__(f'user does not have task with id {task_id}')


class ExtServiceError(DomainError):
    def __init__(self, service: str, response: ClientResponse):
        self.service = service
        self.response = response
        super().__init__(f'got error response from {service}')


class ExtServiceUnexpectedResponseError(DomainError):
    def __init__(self, service: str, response: ClientResponse):
        self.service = service
        self.response = response
        super().__init__(f'got unexpected response from {service}')


class InvalidOAuthToken(DomainError):
    def __init__(self):
        super().__init__('got request with invalid oauth token')
