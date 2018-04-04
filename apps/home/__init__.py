# .py

__author__ = 'bnk'

from flask import Blueprint

home = Blueprint('home',__name__)

import apps.home.views