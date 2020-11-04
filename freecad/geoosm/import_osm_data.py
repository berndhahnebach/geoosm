# ***************************************************************************
# *   Copyright (c) 2017 Bernd Hahnebach <bernd@bimstatik.org>              *
# *                                                                         *
# *   This file is part of the FreeCAD CAx development system.              *
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

import FreeCAD

# use geoosm workbench
from freecad.geoosm import import_osm
import importlib
importlib.reload(import_osm)


def read_osm_sample_geoosm():

    # https://www.openstreetmap.org/#map=18/50.340722/11.232647

    latitude = 50.340722
    longitude = 11.232647
    cutout_edge_length = 0.3 / 10  # in lat,lon unit, 0.03 are ca 30 meter, value is ca km
    progressbar = False
    status = False
    elevation = False

    # test elevation with min data
    # cutout_edge_length = 0.01
    # elevation = True

    # center of cutout rectangle will be 0,0 (origin) in CAD

    rc = import_osm.import_osm2(
        latitude,
        longitude,
        cutout_edge_length,
        progressbar,
        status,
        elevation
    )
    print(rc)  # return value is just True
    FreeCAD.Console.PrintMessage("OSM data was read\n")

    return True


def read_osm_zurich():

    # https://www.openstreetmap.org/#map=16/47.37782/8.54039

    latitude = 47.37782
    longitude = 8.54039
    cutout_edge_length = 0.5  # ca km
    progressbar = False
    status = False
    elevation = False

    import_osm.import_osm2(
        latitude,
        longitude,
        cutout_edge_length,
        progressbar,
        status,
        elevation
    )
    FreeCAD.Console.PrintMessage("OSM data was read\n")

    return True


def read_osm_brienzerrothorn():

    # https://www.openstreetmap.org/#map=17/46.78690/8.04390

    latitude = 46.78690
    longitude = 8.04390
    cutout_edge_length = 0.5  # ca km
    progressbar = False
    status = False
    elevation = False

    # fuer elevation test 46.788, 8.045, cutout_edge_length 0.1
    # test elevation
    # latitude = 46.788
    # longitude = 8.045
    # cutout_edge_length = 0.1  # ca km
    cutout_edge_length = 0.5  # ca km   9.9 error, 5.0 ok
    # cutout_edge_length = 5.0  # ca km   9.9 error, 5.0 ok
    elevation = True

    import_osm.import_osm2(
        latitude,
        longitude,
        cutout_edge_length,
        progressbar,
        status,
        elevation
    )
    FreeCAD.Console.PrintMessage("OSM data was read\n")

    return True


def read_osm_alpedhuez():

    # zufahrtsstrasse
    # https://www.openstreetmap.org/#map=15/45.0790/6.0550&layers=C
    # 4.0 km
    latitude = 45.0790
    longitude = 6.0550
    cutout_edge_length = 4.0  # ca km
    progressbar = False
    status = False
    elevation = True

    # dorf
    # https://www.openstreetmap.org/#map=19/45.09000/6.07000&layers=C
    # 0.1 ... nur 9 wege und auch gebeude
    latitude = 45.09
    longitude = 6.07
    # cutout_edge_length = 0.1
    cutout_edge_length = 0.5
    elevation = True

    import_osm.import_osm2(
        latitude,
        longitude,
        cutout_edge_length,
        progressbar,
        status,
        elevation
    )
    FreeCAD.Console.PrintMessage("OSM data was read\n")

    return True
