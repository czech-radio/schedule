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

import logging
import datetime as dt

import flask
from flask_wtf.csrf import CSRFProtect


__all__ = tuple(["main"])


class Server:
    """
    The Flask based server application.
    """
    # todo


def main():

    logging.basicConfig(level=logging.DEBUG)

    app = flask.Flask(__name__, template_folder="./templates")

    app.config.update(
        SECRET_KEY="secret_sauce",
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        TEMPLATES_AUTO_RELOAD=True,
    )

    # csrf = CSRFProtect()
    # csrf.init_app(app)

    from cro.schedule import Client

    @app.route("/", methods = ["POST", "GET"])
    def index():

        client = Client()

        match flask.request.method:

            case "GET":
                shows = []
                for station in Client.get_stations():
                    client.station = station.id
                    schedule = client.get_day_schedule()
                    app.logger.info(schedule)
                    shows.append(sorted(schedule.shows))

                return flask.render_template("index.html", date=dt.datetime.now(), shows=shows)

            case "POST":
                date = flask.request.form.get("date")

                if date is None:
                    date = dt.datetime.now.date().isoformat()

                station = flask.request.form.get("station")

                app.logger.info(f"{date}, {station}, '<<<<<<<<<<<<<<<'")

                client.station = station
                schedule = client.get_day_schedule(date = date)
                shows = sorted(schedule.shows)

                return flask.render_template("index.html", date = date, shows=shows)

            case _:
                raise Exception("HTTP method not known!")

    app.run(debug=True, use_debugger=False, use_reloader=False)
