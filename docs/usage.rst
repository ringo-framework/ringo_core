=====
Usage
=====

Configuration
-------------
The connection of the database is configured through a `RINGO_CORE_DB_URI` environment variable. The default value is *sqlite:///:memory:*. To set the environment variable on a unix system just export it before you start a application using the tedega_core library.::

        export RINGO_CORE_DB_URI=postgresql://@/tedega_core

API
---
The API gives access to all (currently) known uses cases related to the core
models. Please do not access any attributes or methods on the model directly!
Use the API to prevent unindented coupling with the underlying model. For this
reason the API does return only simple datatype like dictionaries or lists.

If you miss a use case which is not covered by the API, please make a feature
request.

User
""""
.. automodule:: tedega_core.api.user
   :members:

Internal CRUD
""""""""""""""
.. automodule:: tedega_core.api.crud
   :members: _create, _read, _update, _delete

Migration
---------
