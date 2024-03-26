# Copyright 1996 - 2024 by Eric House (xwords@eehouse.org).  All rights
# reserved.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.

from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__, static_url_path='/fixin/static')
    app.config.from_object(Config)

    from app.fixin import bp as fixin_bp
    app.register_blueprint(fixin_bp, url_prefix='/fixin')
    from app.fmu import bp as fmu_bp
    app.register_blueprint(fmu_bp, url_prefix='/fmu')

    return app
