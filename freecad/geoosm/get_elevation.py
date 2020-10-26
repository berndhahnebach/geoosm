# ***************************************************************************
# *   Copyright (c) 2020 Bernd Hahnebach <bernd@bimstatik.org>              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************
"""get elevation data"""

import json
import requests
import time

# import FreeCAD
import FreeCADGui


# ****************************************************************************
"""
# https://github.com/adamcharnock/python-srtm
from sidepackages_geoosm import python_srtm as pysrtm
srtm1_data = pysrtm.Srtm1HeightMapCollection()
srtm1_data.get_altitude(latitude=40.123, longitude=-7.456)
Srtm1HeightMapCollection().get_elevation_profile(40.123, -7.456, 40.129, -7.460)
"""


# ****************************************************************************
"""
import geoosm.get_elevation
import importlib
importlib.reload(geoosm.get_elevation)
geoosm.get_elevation.get_height_srtm_tkrajina(46.503, 8.035)

geoosm.get_elevation.get_height_srtm_tkrajina(46.7830721, 8.0028829)

"""


def get_height_srtm_tkrajina(b, l):

    # from sidepackages_geoosm import srtm as srtmtkrjina
    # eledata = srtmtkrjina.get_data()
    # eledata.get_elevation(46.503, 8.035)

    from sidepackages_geoosm import srtmtkrjina
    eledata = srtmtkrjina.get_data()
    try:
        elevation = eledata.get_elevation(float(b), float(l))
    except:
        print(
            "Error on elevation for: lat: {}, long: {}, exception raised"
            .format(b, l)
        )
    # print("lat: {}, long: {}, ele: {}".format(b, l, elevation))
    if elevation is None:
        print(
            "No elevation for: lat: {}, long: {}, (None returned)"
            .format(b, l)
        )
        return 0.0
    else:
        return round(elevation * 1000, 2)


"""
import geoosm.get_elevation
import importlib
importlib.reload(geoosm.get_elevation)
pts = [["620877237", "46.8076263", "8.0596176"], ["5067330264", "46.8010987", "8.0548266"]]
geoosm.get_elevation.get_heights_srtm_tkrajina(pts)

{'46.8076263 8.0596176': 1241000, '46.8010987 8.0548266': 1534000}

"""


def get_heights_srtm_tkrajina(points):

    # uses get_height_srtm_tkrajina to get the height of each point

    heights = {}
    for pt in points:
        # print(pt)
        key = "{:.7f} {:.7f}".format(float(pt[1]), float(pt[2]))
        # print(key)
        heights[key] = get_height_srtm_tkrajina(pt[1], pt[2])
        # print(heights[key])
    return heights


# ****************************************************************************
"""
import geoosm.get_elevation
import importlib
importlib.reload(geoosm.get_elevation)
geoosm.get_elevation.get_height_srtm4(46.503, 8.035)

"""


def get_height_srtm4(b, l):
    """
    get height of a single point with latitude b, longitude l
    """

    try:
        from srtm4 import srtm4
        nosrtm4 = False
    except:
        print("Module srtm4 not found")
        nosrtm4 = True

    if nosrtm4 is True:
        return(0.0)

    # https://en.wikipedia.org/wiki/SRTM
    # resolution is 30 m
    # in english it says 30 m for United States and 90 m outside United States
    # downloaded tiffs from area locally
    # download von ca 35 MB, aber halbe Schweiz dann lokal gespeichert
    # https://pypi.org/project/elevation/
    # https://pypi.org/project/srtm4/
    # https://github.com/cmla/srtm4/issues/10
    # import srtm4
    # srtm4.srtm4(8.035, 46.503)  # Konkordiaplatz

    # the longitude as first argument, and the latitude as second argument
    # thus method parameters are swaped

    elevation = srtm4(float(l), float(b))
    # print("lat: {}, long: {}, ele: {}".format(b, l, elevation))
    return round(elevation * 1000, 2)


"""
import geoosm.get_elevation
import importlib
importlib.reload(geoosm.get_elevation)
pts = [["620877237", "46.8076263", "8.0596176"], ["5067330264", "46.8010987", "8.0548266"]]
geoosm.get_elevation.get_heights_srtm4(pts)


{'46.8076263 8.0596176': 1300240.0, '46.8010987 8.0548266': 1727440.0}

"""


def get_heights_srtm4(points):

    # uses get_height_srtm4 to get the height of each point

    heights = {}
    for pt in points:
        # print(pt)
        key = "{:.7f} {:.7f}".format(float(pt[1]), float(pt[2]))
        # print(key)
        # swap will happen in other method
        heights[key] = get_height_srtm4(pt[1], pt[2])
        # print(heights[key])
    return heights


# ****************************************************************************
"""
import geoosm.get_elevation
import importlib
importlib.reload(geoosm.get_elevation)
geoosm.get_elevation.getHeight(46.7869, 8.0439)

"""


def getHeight(b, l):
    """
    get height of a single point with latitude b, longitude l
    """
    # return 390000.00
    # return 0.0

    # https://open-elevation.com/
    # https://github.com/Jorl17/open-elevation/blob/master/docs/api.md
    # https://gis.stackexchange.com/questions/212106/seeking-alternative-to-google-maps-elevation-api
    # https://www.openstreetmap.org/node/620877237
    # https://nominatim.openstreetmap.org/ui/search.html
    #
    # browser
    # https://api.open-elevation.com/api/v1/lookup?locations=46.7869,8.0439
    # {"results": [{"latitude": 46.7869, "elevation": 2242, "longitude": 8.0439}]}
    # is on Brienzer Rothorn, thus 2242 is correct :-)
    #
    # Python
    # import requests, json
    # r=requests.get("https://api.open-elevation.com/api/v1/lookup?locations=46.78690,8.04390", timeout=30)
    # r.text
    # '{"results": [{"latitude": 46.7869, "elevation": 2242, "longitude": 8.0439}]}'
    # json.loads(r.text)["results"][0]["elevation"]
    # json.loads('{"results": [{"latitude": 46.7869, "elevation": 2242, "longitude": 8.0439}]}')["results"][0]["elevation"]
    # {"results": [{"latitude": 46.7869, "elevation": 2242, "longitude": 8.0439}]}
    #
    # https://github.com/Jorl17/open-elevation/issues/33
    # https://github.com/Jorl17/open-elevation/issues/29
    #
    # use NASA SRMT data downloaded tiffs from area locally
    # https://pypi.org/project/elevation/
    # https://pypi.org/project/srtm4/
    # https://github.com/cmla/srtm4/issues/10
    # download von ca 35 MB, aber halbe Schweiz dann lokal gespeichert

    base_source = "https://api.open-elevation.com/api/v1/lookup?locations="

    source = "{}{},{}".format(base_source, b, l)
    print(source)

    answer = elevation_request(source)

    if answer is not None:
        print("Answer: {}".format(answer))
        data = json.loads(answer)["results"]
        elevation = data[0]["elevation"]
        return round(elevation * 1000, 2)  # in mm with 2 dezimals
    else:
        print("No elevation, return 0.0")
        return 0.0


"""
import geoosm.get_elevation
import importlib
importlib.reload(geoosm.get_elevation)
geoosm.get_elevation.getHeights([["620877237", "46.8076263", "8.0596176"], ["5067330264", "46.8010987", "8.0548266"]])

"""


def getHeights(points):
    """
    get heights for a list of points
    """
    # return {'50.3407298 11.2325036': 404000, '50.3407539 11.2327103': 404000, '50.3408268 11.2326894': 404000, '50.3408026 11.2324827': 404000, '60.0000000 10.0000000': 0}
    # return {}

    # browser
    # https://api.open-elevation.com/api/v1/lookup?locations=46.8076, 8.0596|46.8011, 8.0548
    #
    # Python
    # import requests, json
    # r=requests.get("https://api.open-elevation.com/api/v1/lookup?locations=46.8076, 8.0596|46.8011, 8.0548", timeout=30)
    # r.text
    # "{"results": [{"latitude": 46.8076, "elevation": 1246, "longitude": 8.0596}, {"latitude": 46.8011, "elevation": 1636, "longitude": 8.0548}]}'
    # d=json.loads(r.text)["results"]
    # [{"latitude": 46.8076, "elevation": 1246, "longitude": 8.0596}, {"latitude": 46.8011, "elevation": 1636, "longitude": 8.0548}]

    base_source = "https://api.open-elevation.com/api/v1/lookup?locations="

    heights = {}
    i = 0
    size = len(points)
    while i < size:
        source = base_source
        ii = 0
        if i > 0:
            time.sleep(1)
        while ii < 20 and i < size:  # send maximum 20 points in one request
            p = points[i]
            ss = "{}, {}|".format(p[1], p[2])
            source += ss
            i += 1
            ii += 1
        source += "60.0,10.0"  # what is the reason for this?
        print(source)

        answer = elevation_request(source)

        if answer is not None:
            print("Answer: {}".format(answer))
            data = json.loads(answer)["results"]
            for point in data:
                key = "{:.7f} {:.7f}".format(point["latitude"], point["longitude"])
                heights[key] = round(point["elevation"] * 1000, 2)

    return heights


def elevation_request(apistring):

    answer = None
    count = 1
    while count < 50:  # 50 x 30 = 1500 sek = halbe stunde!!!
        print("Try fetching elevations, attempt {}".format(count))
        FreeCADGui.updateGui()
        try:
            response = requests.get(apistring, timeout=30)
        except:
            response = None
        count += 1
        time.sleep(5)
        if response is not None:
            answer = response.text
            if "502 Bad Gateway" not in answer:
                break

    return answer
