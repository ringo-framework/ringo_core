=====
Usage
=====

Configuration
-------------
The connection of the database is configured through a `RINGO_CORE_DB_URI` environment variable. The default value is *sqlite:///:memory:*. To set the environment variable on a unix system just export it before you start a application using the ringo_core library.::

        export RINGO_CORE_DB_URI=postgresql://@/ringo_core

API
---

User
""""
.. automodule:: ringo_core.api.user
   :members:

Internal CRUD
""""""""""""""
.. automodule:: ringo_core.api.crud
   :members: _create, _read, _update, _delete

Migration
---------
