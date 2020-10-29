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
"""get elevation data by srtm.py module"""



"""
https://pypi.org/project/SRTM.py/
https://github.com/tkrajina
AFAIR some heights are missing thus not usable for import_osm


from sidepackages_geoosm import srtm as srtmpy
eledata = srtmpy.get_data()
eledata.get_elevation(46.503, 8.035)


from freecad.geoosm import get_elevation_srtmpy
import importlib
importlib.reload(get_elevation_srtmpy)
get_elevation_srtmpy.get_height_single(46.503, 8.035)

# no height ???
get_elevation_srtmpy.get_height_single(46.7830721, 8.0028829)

"""


def get_height_single(b, l):

    from sidepackages_geoosm import srtm as srtmpy
    eledata = srtmpy.get_data()
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
from freecad.geoosm import get_elevation_srtmpy
import importlib
importlib.reload(get_elevation_srtmpy)
pts = [["620877237", "46.8076263", "8.0596176"], ["5067330264", "46.8010987", "8.0548266"]]
get_elevation_srtmpy.get_height_list(pts)

{'46.8076263 8.0596176': 1241000, '46.8010987 8.0548266': 1534000}

"""


def get_height_list(points):
    """
    uses get_height_single to get the height of each point
    """
    heights = {}
    for pt in points:
        # print(pt)
        key = "{:.7f} {:.7f}".format(float(pt[1]), float(pt[2]))
        # print(key)
        heights[key] = get_height_single(pt[1], pt[2])
        # print(heights[key])
    return heights

