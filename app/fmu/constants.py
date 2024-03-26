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

# should have no dependencies
class Constants:
    IN_TO_CM = 2.54
    STAY_RANGE_IN = 0.4 # in inches
    CHART_TOP = 25
    TOP_MARGIN = 15
    BOTTOM_MARGIN = 15
    PIXEL_LENGTH_IN = 0.0005
    GEAR_HEIGHT = 10
    LEFT_OFFSET = 30
    NODE_WIDTH = 40
    PIXELS_PER_ROW = 50
    HORIZONTAL_INTERVAL = 0.05
    INCHES_PER_ROW = 5

    COLOR_GREY = (255//2, 255//2, 255//2)
    COLOR_BLACK = (0, 0, 0)
    COLOR_HIGHLIGHT = (225, 225, 255)
    CHAIN_COLORS = [ (255, 0, 0),
                     (0, 255, 0),
                     (0, 0, 255),
                     (0, 255, 255),
                     (255, 0, 255),
        ]

    AXLE_ADJUST = (
        ('none', 'None', 0.0 ),
        ('vert', 'Vertical', 0.05 ),
        ('fi', 'Fixed Innovations', 0.2 ),
        ('ex', 'Eccentric BB', 0.3 ),
        ('hor', 'Horizontal', 1.0 ),
    )

    WHEEL_SIZE = (
        (26.8, "700x35",),
        (26.27, "700x28",),
        (26.16, "700x23",),
        (26.08, "700x20",),
        (26.84, "27x1.25",),
        (25.63, "26x1.9",),
        (23.97, "26(559mm)x1.0",),
        (24.49, "26(650c)x1.0",),
        (21.97, "24x1",),
        (19.15, "20x1.75",),
    )
