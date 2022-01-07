import json
from argparse import ArgumentParser
from src.db.database import DBConfig


class ArgsParser:

    def __init__(self, args: list):
        self.__passed_args: list = args
        self.__args: dict = {}

    def parse(self):
        parser = ArgumentParser(prog="Car Rental System", usage="%(prog)s [options]",
                                description="Car Rental Management System")

        parser.add_argument("--host",
                            nargs=1,
                            required=False,
                            default="localhost",
                            type=str,
                            help="host used to host the MySQL instance")

        parser.add_argument("--user",
                            nargs=1,
                            required=True,
                            type=str,
                            help="user used to connect to MySQL instance")

        parser.add_argument("--password",
                            nargs=1,
                            required=True,
                            type=str,
                            help="password used to connect to MySQL instance")

        self.__args = parser.parse_args()

        db_config = DBConfig(
            host=self.__args.host[0] if isinstance(self.__args.host, list) else self.__args.host,
            user=self.__args.user[0],
            password=self.__args.password[0],
        )
        return db_config

