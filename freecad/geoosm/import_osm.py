# **************************************************************************
# *                                                                        *
# *  Copyright (c) 2016 microelly <>                                       *
# *  Copyright (c) 2020 Bernd Hahnebach <bernd@bimstatik.org               *
# *                                                                        *
# *  This program is free software; you can redistribute it and/or modify  *
# *  it under the terms of the GNU Lesser General Public License (LGPL)    *
# *  as published by the Free Software Foundation; either version 2 of     *
# *  the License, or (at your option) any later version.                   *
# *  for detail see the LICENCE text file.                                 *
# *                                                                        *
# *  This program is distributed in the hope that it will be useful,       *
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *  GNU Library General Public License for more details.                  *
# *                                                                        *
# *  You should have received a copy of the GNU Library General Public     *
# *  License along with this program; if not, write to the Free Software   *
# *  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *  USA                                                                   *
# *                                                                        *
# **************************************************************************
"""
Import data from OpenStreetMap
"""

import os
import time

import FreeCAD
import FreeCADGui
import Part

from freecad.trails.geomatics.geoimport import inventortools
from freecad.trails.geomatics.geoimport import transversmercator

from freecad.trails.geomatics.geoimport.import_osm import get_osmdata
from freecad.trails.geomatics.geoimport.import_osm import get_way_information
from freecad.trails.geomatics.geoimport.import_osm import map_data
from freecad.trails.geomatics.geoimport.import_osm import organize_doc
from freecad.trails.geomatics.geoimport.import_osm import set_cam

from freecad.trails.geomatics.geoimport.say import say
from freecad.trails.geomatics.geoimport.say import sayErr
from freecad.trails.geomatics.geoimport.say import sayexc
# from freecad.trails.geomatics.geoimport.say import sayW

# from .get_elevation import get_height_srtm_tkrajina as get_height_single
# from .get_elevation import get_heights_srtm_tkrajina as get_height_list
from .get_elevation import get_height_srtm4 as get_height_single
from .get_elevation import get_heights_srtm4 as get_height_list

"""
# http://api.openstreetmap.org/api/0.6/map?bbox=11.74182,50.16413,11.74586,50.16561
# http://api.openstreetmap.org/api/0.6/way/384013089
# http://api.openstreetmap.org/api/0.6/node/3873106739

from freecad.geoosm.import_osm import import_osm2
rc = import_osm2(50.340722, 11.232647, 0.03, False, False, False)

# with elevations
from freecad.geoosm import import_osm
import importlib
importlib.reload(import_osm)
rc = import_osm.import_osm2(50.340722, 11.232647, 0.03, False, False, True)

"""


# TODO: test run osm import method in on non gui
debug = False


def import_osm2(b, l, bk, progressbar=False, status=False, elevation=False):

    bk = 0.5 * bk
    if elevation:
        say("get height for {}, {}".format(b, l))
        baseheight = get_height_single(b, l)
        say("baseheight: {}".format(baseheight))
    else:
        baseheight = 0.0

    say("The importer of geoosm is used to import osm data.")
    say("This one does support elevations.")
    say(b, l, bk, progressbar, status, elevation)

    # *************************************************************************
    # get and parse osm data
    if progressbar and FreeCAD.GuiUp:
        progressbar.setValue(0)
    if status and FreeCAD.GuiUp:
        status.setText(
            "get data from openstreetmap.org and parse it for later usage ..."
        )
        FreeCADGui.updateGui()
    tree = get_osmdata(b, l, bk)
    if tree is None:
        sayErr("Something went wrong on retrieving OSM data.")
        return False

    # say("nodes")
    # for element in tree.getiterator("node"):
    #     say(element.params)
    # say("ways")
    # for element in tree.getiterator("way"):
    #     say(element.params)
    # say("relations")
    # for element in tree.getiterator("relation"):
    #     say(element.params)

    # *************************************************************************
    if status and FreeCAD.GuiUp:
        status.setText("transform data ...")
        FreeCADGui.updateGui()

    # relations = tree.getiterator("relation")
    nodes = tree.getiterator("node")
    ways = tree.getiterator("way")
    bounds = tree.getiterator("bounds")[0]

    # get base area size and map nodes data to the area on coordinate origin
    tm, size, corner_min, points, nodesbyid = map_data(nodes, bounds)
    # say(tm)
    # say(size)
    # say(corner_min)
    # say(len(points))
    # say(len(nodesbyid))

    # *************************************************************************
    if status and FreeCAD.GuiUp:
        status.setText("create visualizations  ...")
        FreeCADGui.updateGui()

    # new document
    # TODO, if a document exists or was passed use this one
    # it makes sense to use the doc as return value
    doc = FreeCAD.newDocument("OSM Map")
    say("New FreeCAD document created.")

    # base area
    area = doc.addObject("Part::Plane", "area")
    area.Length = size[0] * 2
    area.Width = size[1] * 2
    placement_for_area = FreeCAD.Placement(
        FreeCAD.Vector(-size[0], -size[1], 0.00),
        FreeCAD.Rotation(0.00, 0.00, 0.00, 1.00)
    )
    area.Placement = placement_for_area
    if FreeCAD.GuiUp:
        # set camera
        set_cam(area, bk)
        area.ViewObject.Document.activeView().viewAxonometric()
        FreeCADGui.updateGui()
    say("Base area created.")

    if elevation:
        elearea = doc.addObject("Part::Feature","Elevation_Area")
        elearea.Shape = get_elebase_sh(corner_min, size, baseheight, tm)
        doc.recompute()
        if FreeCAD.GuiUp:
            area.ViewObject.hide()
            elearea.ViewObject.Transparency = 75       
            elearea.ViewObject.Document.activeView().viewAxonometric()
            # elearea.ViewObject.Document.activeView().fitAll()  # the cam was set
            FreeCADGui.updateGui()
        say("Area with Hights done")

    # *************************************************************************
    # ways
    say("Ways")
    wn = -1
    count_ways = len(ways)
    starttime = time.time()
    refresh = 1000

    for way in ways:
        wid = way.params["id"]
        wn += 1

        # say(way.params)
        # say("way content")
        # for c in way.content:
        #     say(c)
        # for debugging, break after some of the ways have been processed
        # if wn == 6:
        #     say("Waycount restricted to {} by dev".format(wn - 1))
        #     break

        nowtime = time.time()
        # if wn != 0 and (nowtime - starttime) / wn > 0.5:  # had problems
        if wn != 0:
            say(
                "way ---- # {}/{} time per house: {}"
                .format(wn, count_ways, round((nowtime-starttime)/wn, 2))
            )

        if progressbar:
            progressbar.setValue(int(0 + 100.0 * wn / count_ways))

        # get a name for the way
        name, way_type, nr, building_height = get_way_information(way)

        # generate way polygon points
        say("get nodes", way)
        if not elevation:
            polygon_points = []
            for n in way.getiterator("nd"):
                wpt = points[str(n.params["ref"])]
                # say(wpt)
                polygon_points.append(wpt)
        else:
            # get heights for lat lon way polygon points
            polygon_points = get_ppts_with_heights(way, way_type, points, nodesbyid, baseheight)

        # create document object out of the way polygon points
        # for p in polygon_points:
        #    say(p)

        # a wire for each way polygon
        polygon_shape = Part.makePolygon(polygon_points)
        polygon_obj = doc.addObject("Part::Feature", "w_" + wid)
        polygon_obj.Shape = polygon_shape
        # polygon_obj.Label = "w_" + wid

        if name == " ":
            g = doc.addObject("Part::Extrusion", name)
            g.Base = polygon_obj
            g.ViewObject.ShapeColor = (1.0, 1.0, 0.0)
            g.Dir = (0, 0, 10)
            g.Solid = True
            g.Label = "way ex "

        if way_type == "building":
            g = doc.addObject("Part::Extrusion", name)
            g.Base = polygon_obj
            g.ViewObject.ShapeColor = (1.0, 1.0, 1.0)
            if building_height == 0:
                building_height = 10000
            g.Dir = (0, 0, building_height)
            g.Solid = True
            g.Label = name
            inventortools.setcolors2(g)  # what does this do?

        if way_type == "highway":
            g = doc.addObject("Part::Extrusion", "highway")
            g.Base = polygon_obj
            g.ViewObject.LineColor = (0.0, 0.0, 1.0)
            g.ViewObject.LineWidth = 10
            g.Dir = (0, 0, 0.2)
            g.Label = name

        if way_type == "landuse":
            g = doc.addObject("Part::Extrusion", name)
            g.Base = polygon_obj
            if nr == "residential":
                g.ViewObject.ShapeColor = (1.0, 0.6, 0.6)
            elif nr == "meadow":
                g.ViewObject.ShapeColor = (0.0, 1.0, 0.0)
            elif nr == "farmland":
                g.ViewObject.ShapeColor = (0.8, 0.8, 0.0)
            elif nr == "forest":
                g.ViewObject.ShapeColor = (1.0, 0.4, 0.4)
            g.Dir = (0, 0, 0.1)
            g.Label = name
            g.Solid = True


        refresh += 1
        if refresh > 3 and FreeCAD.GuiUp:
            FreeCADGui.updateGui()
            # FreeCADGui.SendMsgToActiveView("ViewFit")
            refresh = 0

    # *************************************************************************
    doc.recompute()
    if progressbar and FreeCAD.GuiUp:
        progressbar.setValue(100)
    if status and FreeCAD.GuiUp:
        status.setText("import finished.")
        FreeCADGui.updateGui()

    organize_doc(doc)
    doc.recompute()

    endtime = time.time()
    say(("running time ", int(endtime-starttime),  " count ways ", count_ways))

    return True


def get_elebase_sh(corner_min, size, baseheight, tm):

    from FreeCAD import Vector as vec
    from MeshPart import meshFromShape
    from Part import makeLine

    # scaled place on orgin
    place_for_mesh = FreeCAD.Vector(
        -corner_min.x - size[0],
        -corner_min.y - size[1],
        0.00)
    
    # SRTM data resolution is 30 m = 30'000 mm in the usa
    # rest of the world is 90 m = 90'000 mm
    # it makes no sense to use values smaller than 90'000 mm
    pt_distance = 100000
    
    say(corner_min)
    # y is huge!, but this is ok!
    say(size)
    
    # base area surface mesh with heights
    # Version new
    pn1 = vec(
        0,
        0,
        0
    )
    pn2 = vec(
        pn1.x + size[0] * 2,
        pn1.y,
        0
    )
    pn3 = vec(
        pn1.x + size[0] * 2,
        pn1.y + size[1] * 2,
        0
    )
    pn4 = vec(
        pn1.x,
        pn1.y + size[1] * 2,
        0
    )
    ln1 = makeLine(pn1, pn2)
    ln2 = makeLine(pn2, pn3)
    ln3 = makeLine(pn3, pn4)
    ln4 = makeLine(pn4, pn1)
    wi = Part.Wire([ln1, ln2, ln3, ln4])
    fa = Part.makeFace([wi], "Part::FaceMakerSimple")
    msh = meshFromShape(fa, LocalLength=pt_distance)
    # move to corner_min to retrieve the heights
    msh.translate(
        corner_min.x,
        corner_min.y,
        0,
    )
    # move mesh points z-koord
    for pt_msh in msh.Points:
        # say(pt_msh.Index)
        # say(pt_msh.Vector)
        pt_tm = tm.toGeographic(pt_msh.Vector.x, pt_msh.Vector.y)
        height = get_height_single(pt_tm[0], pt_tm[1])  # mm
        # say(height)
        pt_msh.move(FreeCAD.Vector(0, 0, height))
    # move mesh back centered on origin
    msh.translate(
        -corner_min.x - size[0],
        -corner_min.y - size[1],
        -baseheight,
    )

    # create Shape from Mesh
    sh = Part.Shape()
    sh.makeShapeFromMesh(msh.Topology, 0.1)

    return sh


def get_ppts_with_heights(way, way_type, points, nodesbyid, baseheight):

    plg_pts_latlon = []
    for n in way.getiterator("nd"):
        # say(n.params)
        m = nodesbyid[n.params["ref"]]
        plg_pts_latlon.append([
            n.params["ref"],
            m.params["lat"],
            m.params["lon"]
        ])
    say("    baseheight: {}".format(baseheight))
    say("    get heights for " + str(len(plg_pts_latlon)))
    heights = get_height_list(plg_pts_latlon)
    # say(heights)
    
    # set the scaled height for each way polygon point
    height = None
    polygon_points = []
    for n in way.getiterator("nd"):
        wpt = points[str(n.params["ref"])]
        # say(wpt)
        m = nodesbyid[n.params["ref"]]
        # say(m.params)
        hkey = "{:.7f} {:.7f}".format(
            float(m.params["lat"]),
            float(m.params["lon"])
        )
        # say(hkey)
        if way_type == "building":
            # for buildings use the height of the first point for all
            # thus code a bit different from the others
            # TODO use 10 cm below the lowest not the first
            # Why do we get all heights if only use one
            # but we need them all to get the lowest
            if height is None:
                say("    Building")
                if hkey in heights:
                    say("    height abs: {}".format(heights[hkey]))
                    height = heights[hkey]
                    say(heights[hkey])
                    say("    height rel: {}".format(height))
                else:
                    sayErr("   ---no height in heights for " + hkey)
                    height = baseheight
        elif way_type == "highway":
            # use the hight for all points
            if height is None:
                say("    Highway")
            if hkey in heights:
                height = heights[hkey]
            else:
                sayErr("   ---no height in heights for " + hkey)
                height = baseheight
        elif way_type == "landuse":
            # use 1 mm above base height
            if height is None:
                sayErr("    ---no height used for landuse ATM")
                height = baseheight + 1
        else:
            # use the hight for all points
            if height is None:
                say("    Other")
            if hkey in heights:
                height = heights[hkey]
            else:
                sayErr("   ---no height in heights for " + hkey)
                height = baseheight
        if height is None:
            height = baseheight
        wpt.z = height - baseheight
        # say("    with base: {}".format(wpt.z))
        polygon_points.append(wpt)
    
    return polygon_points
