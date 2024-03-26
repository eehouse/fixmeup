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

import math
from math import pi

try:
    from app.fmu.constants import Constants
except:
    from constants import Constants

sDefaults = {
    'maxRing' : 53,
    'minRing' : 34,
    'maxCog' : 20,
    'minCog' : 13,
    'stayLen' : 42.0,
    'wheelDiam' : 26.16,
    'isMetric' : 1,
    'display' : 'png',
    'useHalfLink' : 0,
    'stretch' : 0.0,
    'axleAdjust' : 'vert',
    'sortKey' : 'STAYLEN',
    # These two are for use with FlaskTable (my GearsTable subclass)
    'sort' : 'stayLen',
    'direction' : 'asc',
}

def addDefaults(cur):
    result = cur.copy()
    for key, val in sDefaults.items():
        if key in result and result[key]:
            # print('casting {} to type {}: {}'.format(result[key], type(val), type(val)(result[key])))
            result[key] = type(val)(result[key])
        else:
            result[key] = val
    print('getDefaults({}) => {}'.format(cur, result))
    return result

def moveLeft(params):
    result = params.copy()
    result['stayLen'] -= Constants.STAY_RANGE_IN / 2
    return result

def moveRight(params):
    result = params.copy()
    result['stayLen'] += Constants.STAY_RANGE_IN / 2
    return result

def buildNodeListFrom(params, sort = None):
    print('buildNodeListFrom(sort={})'.format(sort))
    nodes = buildNodeList(params['maxRing'],
                          params['minRing'],
                          params['maxCog'],
                          params['minCog'],
                          params['isMetric'],
                          params['stayLen'],
                          params['wheelDiam'],
                          params['stretch'],
                          params['useHalfLink'],
    )

    if sort:
        if sort == 'ring': key = lambda node: node.ring
        elif sort == 'cog': key = lambda node: node.cog
        elif sort == 'stayLen': key = lambda node: node.stayLen
        elif sort == 'gearIn': key = lambda node: node.gearIn
        nodes.sort(key=key)

    # print('buildNodeList() => {}'.format(nodes))
    return nodes

def buildNodeList(bigRing, smallRing, bigCog, smallCog, isMetric, stayLen,
                  wheelDiam, stretch=0.0, useHalfLink=False):
    result = []
    stayLenInIn = isMetric and stayLen / Constants.IN_TO_CM or stayLen
    minStayLen = stayLenInIn - (Constants.STAY_RANGE_IN/2.0)
    maxStayLen = stayLenInIn + (Constants.STAY_RANGE_IN/2.0)

    for ring in range( bigRing, smallRing - 1, -1 ):
        for cog in range( bigCog, smallCog - 1, -1 ):

            perim = perimeterFromGear( ring, cog, minStayLen )
            minHalfLinks = chainBound( perim, stretch, True, useHalfLink )

            perim = perimeterFromGear( ring, cog, maxStayLen )
            maxHalfLinks = chainBound( perim, stretch, False, useHalfLink )

            curHalfLinks = minHalfLinks

            while curHalfLinks <= maxHalfLinks:
                curStayLength = calcStayForGear( ring, cog,
                                                 calcStretch( curHalfLinks * 0.5, stretch ), 
                                                 maxHalfLinks )

                if curStayLength <= maxStayLen and curStayLength >= minStayLen:
                    stayLen = isMetric and curStayLength * Constants.IN_TO_CM or curStayLength
                    node = Node( ring, cog, stayLen, curHalfLinks, (ring*wheelDiam)/cog )
                    result.append( node )
                curHalfLinks += useHalfLink and 1 or 2

    return result

def perimeterFromGear( ring, cog, stayLength ):
    cogRadius = cog / (4 * pi)
    ringRadius = ring / (4 * pi)

    theta = math.acos( (ringRadius-cogRadius)/stayLength)*(180/pi)

    result = ((180-theta) * pi * ringRadius + theta * pi * cogRadius +
               180 * math.sqrt( pow(stayLength,2) - 
                                pow((ringRadius-cogRadius),2) )) / 90

    return result

def chainBound( dd, stretch, upper, useHalfLink ):
    oneLink = calcStretch( useHalfLink and 0.5 or 1.0, stretch )
    linkCount = math.floor( dd / oneLink)
    temp = oneLink * linkCount

    if upper and temp != dd:linkCount += 1

    if not useHalfLink: linkCount *= 2
    return linkCount

def calcStretch( chainlen, stretch):
    return chainlen + (( chainlen * stretch) / 12 )

def calcStayForGear( ring, cog, chainLen, trialStayLength ):
    kTolerance = 0.0001
    counter = 6

    while True:
        counter -= 1
        if counter == 0: break

        # compare with chainLen (target) and adjust
        curDiff = perimeterFromGear( ring, cog, trialStayLength ) - chainLen

        # this is ok as the only way it can be below 0 is if greater
        # than -kTolerance

        if curDiff < kTolerance: break

        trialStayLength -= curDiff / 2.0

    if counter <= 0: trialStayLength = 0.0

    return trialStayLength

class Node():
    def __init__(self, ring, cog, stayLen, halfLinks, gearIn ):
        self.ring = ring
        self.cog = cog
        self.stayLen = stayLen
        self.halfLinks = halfLinks
        self.gearIn = gearIn

    def __repr__(self):
        return '{}x{}, stay: {}'.format(self.ring, self.cog, self.stayLen)

def main():
    nodes = buildNodeList(42, 42, 23, 11, 16, 27)
    for node in nodes:
        print('{}'.format(node))

##############################################################################
if __name__ == '__main__':
    main()
