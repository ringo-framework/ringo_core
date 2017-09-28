# -*- coding: utf-8 -*-
import os
from ringo_service.service import start_service
from ringo_service.lib.swagger import generate_config
import ringo_core.api
from ringo_core.model.user import User
from ringo_core.lib.db import init_db

package_directory = os.path.dirname(os.path.abspath(__file__))


def run():
    init_db()
    swagger_config = os.path.abspath(os.path.join("ringo_core", "api", "swagger.yaml"))
    config = generate_config(swagger_config, User)
    start_service(config, ringo_core.api)


if __name__ == "__main__":
    run()
