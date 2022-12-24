from dataclasses import dataclass

from configargparse import ArgumentParser, YAMLConfigFileParser


@dataclass
class Config:
    @dataclass
    class API:
        host: str
        port: int

    @dataclass
    class DB:
        user: str
        password: str
        host: str
        port: int
        name: str

    api: API
    db: DB
    log_level: str


def parse_config() -> Config:
    args_parser = _setup_args_parser()
    args = args_parser.parse_args()
    return Config(
        api=Config.API(
            host=args.api_host,
            port=args.api_port
        ),
        db=Config.DB(
            user=args.db_user,
            password=args.db_password,
            host=args.db_host,
            port=args.db_port,
            name=args.db_name
        ),
        log_level=args.log_level
    )


def _setup_args_parser() -> ArgumentParser:
    parser = ArgumentParser(
        default_config_files=['config.yml'],
        config_file_parser_class=YAMLConfigFileParser,
        args_for_setting_config_path=['-c', '--config-file'],
        config_arg_help_message='Config file path',
        auto_env_var_prefix=''
    )

    api_group = parser.add_argument_group('API')
    api_group.add_argument('--api-host', type=str, default='0.0.0.0')
    api_group.add_argument('--api-port', type=int, default=8080)

    db_group = parser.add_argument_group('Database')
    db_group.add_argument('--db-user', type=str, default='postgres')
    db_group.add_argument('--db-password', type=str, default='postgres')
    db_group.add_argument('--db-host', type=str, default='localhost')
    db_group.add_argument('--db-port', type=int, default=5432)
    db_group.add_argument('--db-name', type=str, default='task-manager')

    parser.add_argument('--log-level', default='INFO', type=str,
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'])

    return parser
