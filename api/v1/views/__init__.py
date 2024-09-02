#!/usr/bin/python3
from flask import Blueprint
app_views = Blueprint("app_views", __name__, url_prefix="/gitlougui")

from api.v1.views.home_page import *
from api.v1.views.repo_info import *
from api.v1.views.user_profile import *