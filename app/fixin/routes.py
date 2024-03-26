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

from flask import render_template, send_from_directory, flash, url_for, request
from app.fixin import bp
from app.fmu.engine import addDefaults, moveLeft, moveRight, buildNodeListFrom
from flask_table import Table, Col
from app.fmu.constants import Constants

# I can't figure out how to get links into my static directory to
# "just work," so serving them manually. This *should* go away.
@bp.route("/static/<image_path>")
def get_static(image_path):
    try:
        return send_from_directory('/app/static', filename=image_path, as_attachment=False)
    except FileNotFoundError:
        abort(404)

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('home.html', title='Home')

@bp.route('/why')
def why():
    return render_template('why.html')

@bp.route('/fixin')
def fixin():
    return render_template('fixin.html', dated=True)

@bp.route('/axle')
def axle():
    return render_template('axle.html')

@bp.route('/products')
def products():
    return render_template('products.html', dated=True)

@bp.route('/order')
def order():
    return render_template('order.html', dated=True)

@bp.route('/fixmeup')
def fixmeup():
    return render_template('fixmeup.html')

@bp.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

@bp.route('/tutorial1')
def tutorial1():
    return render_template('tutorial1.html')

@bp.route('/tutorial2')
def tutorial2():
    return render_template('tutorial2.html')

@bp.route('/tutorial3')
def tutorial3():
    return render_template('tutorial3.html')

@bp.route('/fmu1_1_big')
def fmu1_1_big():
    return render_template('fmu1_1_big.html')

@bp.route('/formfmu', methods=['GET', 'POST'])
def formfmu():
    args = request.args or request.form
    # flash('formfmu called with method {}, args {}'.format(request.method, args))
    params = addDefaults(args)
    leftParams = moveLeft(params)
    rightParams = moveRight(params)
    print('passing params: {}'.format(params))

    template_args = {
        'params' : params,
        'right_url' : url_for('fixin.formfmu', **rightParams),
        'left_url' : url_for('fixin.formfmu', **leftParams),
        'axleAdjust' : Constants.AXLE_ADJUST,
        'wheelSize' : Constants.WHEEL_SIZE,
    }

    if params['display'] == 'png':
        template_args['center_url'] = url_for('fmu.makepng', **params)
    else:
        sort = params.get('sort')
        nodes = buildNodeListFrom(params, sort)
        if params.get('direction', 'asc') == 'desc': nodes.reverse()
        table = GearsTable(nodes, params)
        template_args['table'] = table

    return render_template('formfmu.html', **template_args )

class FloatCol(Col):
    def __init__(self, title, rightCount):
        super(FloatCol, self).__init__(title)
        self.rightCount = rightCount

    def td_format(self, content):
        return '{:.{rightCount}f}'.format(content, rightCount=self.rightCount)

class GearsTable(Table):
    border = 1
    allow_sort = True
    ring = Col('Ring')
    cog = Col('Cog')
    stayLen = FloatCol('Stay Length', 3)
    halfLinks = Col('Halflinks')
    gearIn = FloatCol('Gear inches', 1)

    def __init__(self, nodes, params):
        sort_by = params.get('sort', 'stayLen')
        sort_reverse = 'desc' == params.get('direction', 'asc')
        super(GearsTable, self).__init__(nodes, sort_by=sort_by, sort_reverse=sort_reverse)
        self.params = params

    def sort_url(self, col_key, reverse=False):
        params = self.params
        params['direction'] = reverse and 'desc' or 'asc'
        params['sort'] = col_key
        url = url_for('fixin.formfmu', **self.params)
        return url

@bp.route('/downloads')
def downloads():
    return render_template('downloads.html')

@bp.route('/stretch')
def stretch():
    return render_template('stretch.html')

@bp.route('/chainstay')
def chainstay():
    return render_template('chainstay.html')

@bp.route('/links')
def links():
    return render_template('links.html')

@bp.route('/source')
def source():
    return render_template('source.html')

@bp.route('/credits')
def credits():
    return render_template('credits.html')

@bp.route('/javafmu')
def javafmu():
    return render_template('javafmu.html')
