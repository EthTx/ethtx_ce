# Local Development

This repository contains 2 basic applications: `frontend` & `api`. It is easy to manage, and you can easily add new
local application(s).

## Basic structure

Application is based on [blueprints](https://flask.palletsprojects.com/en/2.0.x/blueprints/).

New extension requires:

- new Python Package in ![ethtx_ce](ethtx_ce/app) subdirectory.
- `create_app` function (created in new package in `init` file) which returns `Flask` object by
  calling ![app factory](ethtx_ce/app/factory.py) file.
- calling a function above in a `wsgi.py` file with assigned url prefix.

These simple steps allow you to add new extension and integrate with entire application.
