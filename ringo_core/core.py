# -*- coding: utf-8 -*-
import os
from ringo_service import start_service
import ringo_core.api
from ringo_core.model.user import User
from ringo_core.lib.db import init_db

package_directory = os.path.dirname(os.path.abspath(__file__))


def run():
    init_db()
    start_service(os.path.abspath(os.path.join("ringo_core", "api", "swagger.yaml")), ringo_core)


if __name__ == "__main__":
    run()
