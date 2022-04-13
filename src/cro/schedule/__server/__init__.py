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

import datetime as dt

import flask

__all__ = tuple(["main"])


class Server:
    """
    The Flask based server application.
    """

    # todo


def main():

    app = flask.Flask(__name__, template_folder="./templates")

    from cro.schedule import Client

    client = Client(sid="plus")

    @app.route("/")
    def index():
        schedule = client.get_day_schedule()

        shows = schedule.shows

        return flask.render_template("index.html", date=dt.datetime.now(), shows=shows)

    app.run()
