# -*- coding: utf-8 -*-

"""
The server (backend) code to manage (fectch, store) the broadcast schedules.

This subpackage may be later moved to standalone repository.

__Features__
- [ ] Fetch the schedule from the REST service and show the result.
- [ ] Allow to save the result to the database.
      Check wneever the schedules are already saved.
- [ ] Allow to manage stored schedules.
      Must be specified
"""

import flask
# @todo Add to dependencies.


def main():
    app = flask.current_app
