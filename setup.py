from setuptools import setup, find_packages

PACKAGE_NAME = 'backend'

setup(
    name='task-manager-api',
    version='1.0.0',
    platforms='all',
    packages=find_packages(exclude=['tests']),
    package_data={
      f'{PACKAGE_NAME}.storage.db': ['alembic.ini', 'alembic/*', 'alembic/versions/*']
    },
    entry_points={
        'console_scripts': [
            'task-manager-api = {0}.__main__:main'.format(PACKAGE_NAME),
        ]
    },
    python_requires='>=3.10'
)
