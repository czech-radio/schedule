

import logging
import datetime as dt

import flask
from flask import Blueprint, request
from flask_wtf.csrf import CSRFProtect

from cro.schedule import Client


__all__ = tuple(["main"])

# ###########################################################################
# Blueprints
# ###########################################################################

api_bp = Blueprint(name = "api_bp", import_name = __name__, template_folder= "templates", static_folder = "static")
