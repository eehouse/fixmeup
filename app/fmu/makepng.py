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

from app.fmu.engine import buildNodeListFrom
from app.fmu.constants import Constants
from PIL import Image, ImageDraw, ImageFont
import math

class State:
    def __init__(self, params, fontPath, width, height):
        self.img = Image.new('RGB', (width, height + Constants.BOTTOM_MARGIN), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.img)
        self.fontLarge = ImageFont.truetype(font=fontPath, size=20) or ImageFont.load_default()
        self.fontSmall = ImageFont.truetype(font=fontPath, size=16) or ImageFont.load_default()
        self.usedColors = {}
        self.useHalfLink = params['useHalfLink']
        self.isMetric = params['isMetric']
        # self.staylenInches = params['stayLen']

def makePNG(params, fontPath):
    nodes = buildNodeListFrom(params)
    stayLenInIn = params['stayLen']
    print('stayLen before: {}'.format(stayLenInIn))
    if params['isMetric']:
        stayLenInIn /= Constants.IN_TO_CM
    print('stayLen after: {}'.format(stayLenInIn))
    width, height, maxGear, minStay = getSizeForImage( nodes, stayLenInIn )
    height += Constants.CHART_TOP + Constants.TOP_MARGIN
    width += Constants.LEFT_OFFSET + Constants.NODE_WIDTH
    print('makePNG(): width: {}; height: {}'.format(width, height) )

    state = State( params, fontPath, width, height )

    rgnWidth = getHiliteWidth(params)
    paintStayArea( state, stayLenInIn, height, minStay, rgnWidth )
    drawGrid( state, width, height, maxGear )
    drawVerts( state, stayLenInIn, width, height, params['isMetric'], minStay )

    for node in nodes:
        plot( state, node, minStay, maxGear )

    writeChainColors( state, height )

    return state.img

def getHiliteWidth(params):
    result = None
    sel = params.get('axleAdjust')
    for one in Constants.AXLE_ADJUST:
        if sel == one[0]:
            result = one[2]
            break
    return result

def plot( state, node, minStay, maxGear ):
    isHalflink = 1 == (node.halfLinks % 2)
    stayLenInIn = state.isMetric and node.stayLen / Constants.IN_TO_CM or node.stayLen
    # print('plot({}): stayLen: {}; minStay: {}'.format(node, stayLenInIn, minStay))

    xx = math.floor(((stayLenInIn - minStay) / Constants.PIXEL_LENGTH_IN))
    xx += Constants.LEFT_OFFSET
    yy = (maxGear - node.gearIn ) * Constants.GEAR_HEIGHT
    yy += Constants.CHART_TOP + Constants.TOP_MARGIN
    tstr = '{:d}{}{:d}'.format( node.ring, isHalflink and "*"or "x", node.cog )
    color = colorForChain( state, node )
    # print('drawing {} at xx: {}, yy: {}'.format(node, xx, yy))
    state.draw.text( (xx, yy), tstr, font=state.fontSmall, fill=color)
    # state.draw.text( (100, 100), tstr, font=state.fontSmall, fill=color)

def colorForChain( state, node ):
    indx = node.halfLinks % len(Constants.CHAIN_COLORS)
    color = Constants.CHAIN_COLORS[indx]
    state.usedColors[node.halfLinks] = color
    return color

def writeChainColors( state, height ):
    usedColors = state.usedColors
    if usedColors:
        xx = Constants.LEFT_OFFSET
        yy = height

        tstr = 'Chainlengths (in 1" links):'
        state.draw.text( (xx, yy), tstr, font=state.fontSmall, fill=Constants.COLOR_BLACK )
        xx += state.fontSmall.getsize(tstr)[0]

        for lenkey, colorval in usedColors.items():
            tstr = 0 == lenkey % 2 and '{:d}'.format( lenkey//2 ) or '{:.1f}'.format( lenkey/2 )
            state.draw.text( (xx, yy), tstr, font=state.fontSmall, fill=colorval )
            xx += state.fontSmall.getsize(tstr)[0] + 3

        if state.useHalfLink:
            tstr = '(* means half-link)'
            state.draw.text( (xx, yy), tstr, font=state.fontSmall, fill=Constants.COLOR_BLACK )

def getSizeForImage( nodes, stayLenInIn ):
    minGear = 1000.0
    maxGear = 0.0
    minStay = 100.00
    maxStay = 0.0

    for node in nodes:
        gear = node.gearIn
        if minGear > gear: minGear = gear
        if maxGear < gear: maxGear = gear

    minStay = stayLenInIn - (Constants.STAY_RANGE_IN/2)
    maxStay = minStay + Constants.STAY_RANGE_IN

    width = (maxStay-minStay) / Constants.PIXEL_LENGTH_IN
    height = (maxGear - minGear + 3) * Constants.GEAR_HEIGHT

    if height < 70 * Constants.GEAR_HEIGHT:
        height = 70 * Constants.GEAR_HEIGHT

    result = (math.ceil(width), math.ceil(height), maxGear, minStay)
    # print('getSizeForImage({}) => {}'.format(stayLenInIn, result))
    return result

def paintStayArea( state, center, height, stayMin, rgnWidthInches ):
    rectMiddle = Constants.LEFT_OFFSET + ((center - stayMin)/Constants.PIXEL_LENGTH_IN)

    rectWidth = rgnWidthInches / Constants.PIXEL_LENGTH_IN
    left = rectMiddle - round(rectWidth/2)
    if left < Constants.LEFT_OFFSET: left = Constants.LEFT_OFFSET

    state.draw.rectangle(((left, Constants.CHART_TOP),(left+rectWidth, height)),
                         fill=Constants.COLOR_HIGHLIGHT)

def drawGrid( state, width, height, maxGear ):
    print('drawGrid(height={}, maxGear={})'.format(height, maxGear))
    if maxGear == 0: maxGear = 99

    for ii in range(0, 1000):      # whatever
        thisHeight = (ii * Constants.PIXELS_PER_ROW) + Constants.CHART_TOP + Constants.TOP_MARGIN
        if thisHeight > height: break

        num = maxGear - (ii * Constants.INCHES_PER_ROW)
        drawNumStringBefore( state, Constants.LEFT_OFFSET,
                             thisHeight - 10//2,
                             num, '"', (0,0,0))
        state.draw.line( ((Constants.LEFT_OFFSET, thisHeight), (width, thisHeight)),
                         fill=Constants.COLOR_GREY, width=1 )

    state.draw.line( ((Constants.LEFT_OFFSET, height), (width,height)),
                     fill=Constants.COLOR_GREY )

def drawVerts( state, center, width, height, isMetric, minStay ):
    staylenAtStart = center

    state.draw.line( ((Constants.LEFT_OFFSET, Constants.CHART_TOP), (Constants.LEFT_OFFSET, height)),
                     fill=Constants.COLOR_GREY)

    for forward in [True, False]:
        staylenToDraw = center
        while True:
            if not drawOneVert( state, width, height, isMetric, staylenToDraw, minStay, forward ): break
            incr = Constants.HORIZONTAL_INTERVAL
            if not forward: incr *= -1
            # if isMetric: incr *= Constants.IN_TO_CM
            staylenToDraw += incr

def drawOneVert( state, width, height, metric, staylen, minStay, forward ):
    leftCoord = Constants.LEFT_OFFSET + round((staylen-minStay)/Constants.PIXEL_LENGTH_IN)

    if forward and leftCoord > width: return False
    if not forward and leftCoord < Constants.LEFT_OFFSET: return False

    state.draw.line( ((leftCoord, Constants.CHART_TOP), (leftCoord, height)), 
                     fill=Constants.COLOR_GREY)

    tstr = '{:.2f}{:s}'.format(metric and staylen * Constants.IN_TO_CM or staylen,
                               (metric and " cm" or "\"" ) )

    (txtWidth, txtHeight) = state.fontSmall.getsize(tstr)
    leftCoord -= txtWidth // 2
    state.draw.text( (leftCoord, Constants.CHART_TOP-txtHeight), tstr,
                     fill=Constants.COLOR_BLACK, font=state.fontSmall )

    return True

def drawNumStringBefore( state, xx, yy, num, suffix, color ):
    num = int(num)
    tstr = '{:d}{}'.format( num, suffix )
    (width, height) = state.fontSmall.getsize(tstr)
    xx -= width
    state.draw.text( (xx, yy), tstr, font=state.fontSmall, fill=color )
    return width
