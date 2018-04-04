

__author__ = 'bnk'

from flask import Blueprint

admin = Blueprint('admin',__name__)

import apps.admin.views