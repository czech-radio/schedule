import logging
import datetime as dt

import flask
from flask import Blueprint, request, current_app as app

from cro.schedule import Client


__all__ = tuple(["home_bp"])


home_bp = Blueprint(name = "home_bp", import_name = __name__, template_folder= "templates", static_folder = "static")


@home_bp.route("/", methods = ["POST", "GET"])
def home():

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
