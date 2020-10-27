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

import json
import os
import requests
import time
from urllib import request

from pivy import coin

import FreeCAD
import FreeCADGui
import MeshPart
import Part

from freecad.trails.geoimport import inventortools
from freecad.trails.geoimport import my_xmlparser
from freecad.trails.geoimport import transversmercator

# from .get_elevation import get_height_srtm_tkrajina as get_height_single
# from .get_elevation import get_heights_srtm_tkrajina as get_height_list
from .get_elevation import get_height_srtm4 as get_height_single
from .get_elevation import get_heights_srtm4 as get_height_list
from freecad.trails.geoimport.say import say
from freecad.trails.geoimport.say import sayErr
from freecad.trails.geoimport.say import sayexc
from freecad.trails.geoimport.say import sayW


"""
# http://api.openstreetmap.org/api/0.6/map?bbox=11.74182,50.16413,11.74586,50.16561
# http://api.openstreetmap.org/api/0.6/way/384013089
# http://api.openstreetmap.org/api/0.6/node/3873106739

from freecad.geoosm.import_osm import import_osm2
rc = import_osm2(50.340722, 11.232647, 0.03, False, False, False)

# with elevations
import geoosm.import_osm
import importlib
importlib.reload(freecad.geoosm.import_osm)
rc = freecad.geoosm.import_osm.import_osm2(50.340722, 11.232647, 0.03, False, False, True)

"""


# TODO: make run osm import method in on non gui too
debug = False


def import_osm2(b, l, bk, progressbar, status, elevation):

    print("The importer of geoosm is used to import osm data. ")
    print("This one does support elevations.")
    print(b, l, bk, progressbar, status, elevation)

    if progressbar:
        progressbar.setValue(0)

    if status:
        status.setText("get data from openstreetmap.org ...")
        FreeCADGui.updateGui()

    content = ""
    bk = 0.5 * bk
    dn = os.path.join(FreeCAD.ConfigGet("UserAppData"), "geoimport_data/")
    fn = dn+str(b)+"-"+str(l)+"-"+str(bk)
    if not os.path.isdir(dn):
        os.makedirs(dn)

    try:
        say("I try to read data from cache file ... ")
        say(fn)
        f = open(fn, "r")
        content = f.read()
    #    say(content)
    #    raise Exception("to debug:force load from internet")
    except Exception:
        sayW("no cache file, so I connect to  openstreetmap.org...")
        lk = bk
        b1 = b - bk / 1113 * 10
        l1 = l - lk / 713 * 10
        b2 = b + bk / 1113 * 10
        l2 = l + lk / 713 * 10
        koord_str = "{},{},{},{}".format(l1, b1, l2, b2)
        source = "http://api.openstreetmap.org/api/0.6/map?bbox="+koord_str
        say(source)

        response = requests.get(source)
        # data = response.text
        # lines = response.text.split("\n")
        FreeCAD.t = response

        f = open(fn, "w")
        # f.write(response.text)
        if response.status_code == 200:
            with open(fn, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
        f.close()
        # print("The dev would like to break");return

        if False:
            try:
                say("read--")
                response = request.urlopen(source)

                say(response)
                say("2huu")
                first = True
                content = ""
                f = open(fn, "w")
                li = 0
                z = 0
                # ct = 0

                say("2wkkw")
                # say(response.text)
                # lines=response.text.split("\n")
                #  say(len(lines))
                say("ll")
                # for line in lines:
                for line in response:
                    print("Y", line)
                    if status:
                        if z > 5000:
                            status.setText("read data ..." + str(li))
                            z = 0
                        FreeCADGui.updateGui()
                        li += 1
                        z += 1
                    if first:
                        first = False
                    else:
                        content += line
                        f.write(line)
                f.close()
                if status:
                    status.setText("FILE CLOSED ..." + str(li))
                    FreeCADGui.updateGui()
                response.close()
            except Exception:
                sayErr("Fehler beim Lesen")

            if status:
                status.setText("got data from openstreetmap.org ...")
                FreeCADGui.updateGui()
            sayW("Beeenden - im zweiten versuch daten auswerten")

            return False

    if elevation:
        say("get height for {}, {}".format(b, l))
        baseheight = get_height_single(b, l)
        say("baseheight = {} mm".format(baseheight))
    else:
        baseheight = 0

    if debug:
        say("-------Data---------")
        say(content)

    if status:
        status.setText("parse data ...")
        FreeCADGui.updateGui()

    say("------------------------------")
    say(fn)

    tree = my_xmlparser.getData(fn)

    # say("nodes")
    # for element in tree.getiterator("node"):
    #     say(element.params)
    # say("ways")
    # for element in tree.getiterator("way"):
    #     say(element.params)
    # say("relations")
    # for element in tree.getiterator("relation"):
    #     say(element.params)

    if False:
        try:
            sd = my_xmlparser.parse(content)
        except Exception:
            sayexc("Problem parsing data - abort")
            status.setText(
                "Problem parsing data - aborted, for details see Report view"
            )
            return

        if debug:
            say(json.dumps(sd, indent=4))

    if status:
        status.setText("transform data ...")
        FreeCADGui.updateGui()

    # relations = tree.getiterator("relation")
    nodes = tree.getiterator("node")
    ways = tree.getiterator("way")
    bounds = tree.getiterator("bounds")[0]

    # center of the scene
    minlat = float(bounds.params["minlat"])
    minlon = float(bounds.params["minlon"])
    maxlat = float(bounds.params["maxlat"])
    maxlon = float(bounds.params["maxlon"])
    # print(minlat)
    # print(minlon)
    # print(maxlat)
    # print(maxlon)

    tm = transversmercator.TransverseMercator()
    # print("Center vorh: {}".format(tm.fromGeographic(b,l)))
    tm.lat = 0.5 * (minlat + maxlat)
    tm.lon = 0.5 * (minlon + maxlon)
    # setting values changes the result, see transversmerctor module
    # print("Center nach: {}".format(center))

    center = tm.fromGeographic(tm.lat, tm.lon)
    corner_min = tm.fromGeographic(minlat, minlon)
    corner_max = tm.fromGeographic(maxlat, maxlon)
    # print("Corner lu: {}".format(corner_min))
    # print("Corner ro: {}".format(corner_max))
    vec_corner_min = FreeCAD.Vector(
        corner_min[0],
        corner_min[1],
        0
    )
    vec_corner_max = FreeCAD.Vector(
        corner_max[0],
        corner_max[1],
        0
    )
    print("Corner lu: {}".format(vec_corner_min))
    print("Corner ro: {}".format(vec_corner_max))
    size = [center[0] - corner_min[0], center[1] - corner_min[1]]

    # map all points to xy-plane
    points = {}
    nodesbyid = {}
    for n in nodes:
        nodesbyid[n.params["id"]] = n
        ll = tm.fromGeographic(
            float(n.params["lat"]),
            float(n.params["lon"])
        )
        points[str(n.params["id"])] = FreeCAD.Vector(
            ll[0] - center[0],
            ll[1] - center[1],
            0.0
        )

    if status:
        status.setText("create visualizations  ...")
        FreeCADGui.updateGui()

    # new document
    # TODO, if a document exists or was passed use this one
    # it makes sense to use the doc as return value
    doc = FreeCAD.newDocument("OSM Map")
    say("New FreeCAD document created.")

    # base area
    area = doc.addObject("Part::Plane", "area")
    say("Base area created.")
    try:
        viewprovider = area.ViewObject
        root = viewprovider.RootNode
        myLight = coin.SoDirectionalLight()
        myLight.color.setValue(coin.SbColor(0, 1, 0))
        root.insertChild(myLight, 0)
        say("Lighting on base area activated.")
    except Exception:
        sayexc("Lighting 272")

    cam = """#Inventor V2.1 ascii
    OrthographicCamera {
      viewportMapping ADJUST_CAMERA
      orientation 0 0 -1.0001  0.001
      nearDistance 0
      farDistance 10000000000
      aspectRatio 100
      focalDistance 1
    """
    x = 0
    y = 0
    height = 200 * bk * 10000 / 0.6
    cam += "\nposition " + str(x) + " " + str(y) + " 999\n "
    cam += "\nheight " + str(height) + "\n}\n\n"
    FreeCADGui.activeDocument().activeView().setCamera(cam)
    FreeCADGui.activeDocument().activeView().viewAxonometric()
    say("Camera was set.")

    area.Length = size[0] * 2
    area.Width = size[1] * 2
    placement_for_area = FreeCAD.Placement(
        FreeCAD.Vector(-size[0], -size[1], 0.00),
        FreeCAD.Rotation(0.00, 0.00, 0.00, 1.00)
    )
    area.Placement = placement_for_area
    say("Base area scaled.")

    if elevation:
        # base area surface mesh with heights
        tparea_obj = doc.addObject("Part::Plane", "tmp_area")
        tparea_obj.Length = size[0] * 2
        tparea_obj.Width = size[1] * 2
        tparea_obj.Placement = FreeCAD.Placement(
            vec_corner_min,
            FreeCAD.Rotation(0.00, 0.00, 0.00, 1.00)
        )
        doc.recompute()
        # data resolution is 30 m = 30'000 mm in the usa
        # rest of the world is 90 m = 90'000 mm
        # it makes no sense to use values smaller than 90'000 mm
        pt_distance = 100000
        tmarea_msh = MeshPart.meshFromShape(
            tparea_obj.Shape,
            LocalLength=pt_distance
        )
        print("area mesh points: {}".format(tmarea_msh.CountPoints))
        FreeCADGui.updateGui()

        # move mesh points
        for pt_msh in tmarea_msh.Points:
            # print(pt_msh.Index)
            # print(pt_msh.Vector)
            pt_tm = tm.toGeographic(pt_msh.Vector.x, pt_msh.Vector.y)
            height = get_height_single(pt_tm[0], pt_tm[1])  # mm
            pt_msh.move(FreeCAD.Vector(0, 0, height - baseheight))

        tmarea_obj = doc.addObject("Mesh::Feature", "TAreaMesh")
        tmarea_obj.Mesh = tmarea_msh
        place_for_mesh = FreeCAD.Vector(
            -vec_corner_min.x - size[0],
            -vec_corner_min.y - size[1],
            0.00)
        tmarea_obj.Placement = FreeCAD.Placement(
            place_for_mesh,
            FreeCAD.Rotation(0.00, 0.00, 0.00, 1.00)
        )
        tmarea_obj.ViewObject.Transparency = 50

        tparea_obj.Placement = placement_for_area
        tparea_obj.ViewObject.hide()

        area.ViewObject.hide()
        doc.recompute()
        say("Area with Hights")
        FreeCADGui.updateGui()

    # ways
    say("Ways")
    wn = -1
    count_ways = len(ways)
    starttime = time.time()
    refresh = 1000

    for w in ways:
        wid = w.params["id"]

        # say(w.params)
        # say("way content")
        # for c in w.content:
        #     say(c)

        building = False
        landuse = False
        highway = False
        wn += 1
        
        # for debugging, break after some of the ways have been processed
        # if wn == 6:
        #     print("Waycount restricted to {} by dev".format(wn - 1))
        #     break

        nowtime = time.time()
        # if wn != 0 and (nowtime - starttime) / wn > 0.5:  # had problems
        if wn != 0:
            print(
                "way ---- # {}/{} time per house: {}"
                .format(wn, count_ways, round((nowtime-starttime)/wn, 2))
            )

        if progressbar:
            progressbar.setValue(int(0 + 100.0 * wn / count_ways))

        st = ""
        st2 = ""
        nr = ""
        h = 0
        # ci is never used
        # ci = ""

        for t in w.getiterator("tag"):
            try:
                if debug:
                    say(t)
                    # say(t.params["k"])
                    # say(t.params["v"])

                if str(t.params["k"]) == "building":
                    building = True
                    if st == "":
                        st = "building"

                if str(t.params["k"]) == "landuse":
                    landuse = True
                    st = t.params["k"]
                    nr = t.params["v"]

                if str(t.params["k"]) == "highway":
                    highway = True
                    st = t.params["k"]

                if str(t.params["k"]) == "addr:city":
                    pass
                    # ci is never used
                    # ci = t.params["v"]

                if str(t.params["k"]) == "name":
                    zz = t.params["v"]
                    nr = beaustring(zz)

                if str(t.params["k"]) == "ref":
                    zz = t.params["v"]
                    nr = beaustring(zz)+" /"

                if str(t.params["k"]) == "addr:street":
                    zz = t.params["v"]
                    st2 = " "+beaustring(zz)

                if str(t.params["k"]) == "addr:housenumber":
                    nr = str(t.params["v"])

                if str(t.params["k"]) == "building:levels":
                    if h == 0:
                        h = int(str(t.params["v"]))*1000*3

                if str(t.params["k"]) == "building:height":
                    h = int(str(t.params["v"]))*1000

            except Exception:
                sayErr("unexpected error {}".format(50*"#"))

        name = str(st) + st2 + " " + str(nr)
        if name == " ":
            name = "landuse xyz"
        if debug:
            say(("name ", name))
        # say(name, zz, nr, ci)

        # generate pointlist for polygon of the way
        polygon_points = []
        height = None
        llpoints = []
        # say("get nodes", w)
        for n in w.getiterator("nd"):
            # say(n.params)
            m = nodesbyid[n.params["ref"]]
            llpoints.append([
                n.params["ref"],
                m.params["lat"],
                m.params["lon"]
            ])

        # elevations
        height = None
        # if I use srtm it does not matter for speed if
        # one point or list, since the list does call the
        # one point method for all points anyway
        if elevation:
            print("    baseheight: {}".format(baseheight))
            print("    get heights for " + str(len(llpoints)))
            heights = get_height_list(llpoints)
            # print(heights)
        for n in w.getiterator("nd"):
            p = points[str(n.params["ref"])]
            # print(p)
            m = nodesbyid[n.params["ref"]]
            # print(m.params)
            hkey = "{:.7f} {:.7f}".format(
                float(m.params["lat"]),
                float(m.params["lon"])
            )
            # print(hkey)
            if elevation and building:
                # for buildings use the height of the first point for all
                # TODO use 10 cm below the lowest not the first
                # Why do we get all heights if only use one
                # but we need them all to get the lowest
                if height is None:
                    print("    Building")
                    print("    No height: {}".format(height))
                    if hkey in heights:
                        print("    height abs: {}".format(heights[hkey]))
                        height = heights[hkey] - baseheight
                        print(heights[hkey] - baseheight)
                        print("    height rel: {}".format(height))
                    else:
                        sayErr("   ---no height in heights for " + hkey)
                        height = 0
            elif elevation and highway:
                # use the real hight for all points
                if height is None:
                    print("    Highway")
                if hkey in heights:
                    height = heights[hkey] - baseheight
                # print("    srmt method: {}".format(heights[hkey]))
                # print("    height poly: {}".format(height))
            elif elevation and landuse:
                if height is None:
                    sayErr("    ---no height used for landuse ATM")
                    height = 1
            elif elevation:
                # use the real hight for all points
                if height is None:
                    print("    Other")
                if hkey in heights:
                    height = heights[hkey] - baseheight
            if height is None:
                height = 0.0
            p.z = height
            # print("    with base: {}".format(p.z))
            polygon_points.append(p)

        # create 2D map
        # for p in polygon_points:
        #    print(p)
        pp_shape = Part.makePolygon(polygon_points)
        pp_obj = doc.addObject("Part::Feature", "w_" + wid)
        pp_obj.Shape = pp_shape
        # pp_obj.Label = "w_" + wid

        if name == " ":
            g = doc.addObject("Part::Extrusion", name)
            g.Base = pp_obj
            g.ViewObject.ShapeColor = (1.00, 1.00, 0.00)
            g.Dir = (0, 0, 10)
            g.Solid = True
            g.Label = "way ex "

        if building:
            g = doc.addObject("Part::Extrusion", name)
            g.Base = pp_obj
            g.ViewObject.ShapeColor = (1.00, 1.00, 1.00)

            if h == 0:
                h = 10000
            g.Dir = (0, 0, h)
            g.Solid = True
            g.Label = name
            inventortools.setcolors2(g)

        if landuse:
            g = doc.addObject("Part::Extrusion", name)
            g.Base = pp_obj
            if nr == "residential":
                g.ViewObject.ShapeColor = (1.00, 0.60, 0.60)
            elif nr == "meadow":
                g.ViewObject.ShapeColor = (0.00, 1.00, 0.00)
            elif nr == "farmland":
                g.ViewObject.ShapeColor = (0.80, 0.80, 0.00)
            elif nr == "forest":
                g.ViewObject.ShapeColor = (1.0, 0.40, 0.40)
            g.Dir = (0, 0, 0.1)
            g.Label = name
            g.Solid = True

        if highway:
            g = doc.addObject("Part::Extrusion", "highway")
            g.Base = pp_obj
            g.ViewObject.LineColor = (0.00, 0.00, 1.00)
            g.ViewObject.LineWidth = 10
            g.Dir = (0, 0, 0.2)
            g.Label = name
        refresh += 1

        if os.path.exists("/tmp/stop"):
            sayErr("notbremse gezogen")
            FreeCAD.w = w
            raise Exception("Notbremse Manager main loop")

        if refresh > 3:
            FreeCADGui.updateGui()
            # FreeCADGui.SendMsgToActiveView("ViewFit")
            refresh = 0

    doc.recompute()
    FreeCADGui.updateGui()
    doc.recompute()

    if status:
        status.setText("import finished.")
    if progressbar:
        progressbar.setValue(100)

    organize_doc(doc)

    endtime = time.time()
    say(("running time ", int(endtime-starttime),  " count ways ", count_ways))
    doc.recompute()

    return True


def organize_doc(doc):
    """
    Create groups for the different object types
    GRP_highways, GRP_building, GRP_landuse
    """
    highways = doc.addObject(
        "App::DocumentObjectGroup",
        "GRP_highways"
    )
    landuse = doc.addObject(
        "App::DocumentObjectGroup",
        "GRP_landuse"
    )
    buildings = doc.addObject(
        "App::DocumentObjectGroup",
        "GRP_building"
    )
    pathes = doc.addObject(
        "App::DocumentObjectGroup",
        "GRP_pathes"
    )

    for obj in doc.Objects:
        if obj.Label.startswith("building"):
            buildings.addObject(obj)
            # obj.ViewObject.Visibility=False
        if obj.Label.startswith("highway") or obj.Label.startswith("way"):
            highways.addObject(obj)
            # obj.ViewObject.Visibility = False
        if obj.Label.startswith("landuse"):
            landuse.addObject(obj)
            # obj.ViewObject.Visibility = False
        if obj.Label.startswith("w_"):
            pathes.addObject(obj)
            obj.ViewObject.Visibility = False


# hack to catch German special character (Umlaute)
def beaustring(string):
    res = ""
    for tk in zz:
        try:
            res += str(tk)
        except Exception:
            if ord(tk) == 223:
                res += "ß"
            elif ord(tk) == 246:
                res += "ö"
            elif ord(tk) == 196:
                res += "Ä"
            elif ord(tk) == 228:
                res += "ä"
            elif ord(tk) == 242:
                res += "ü"
            else:
                sayErr(["error sign", tk, ord(tk), string])
                res += "#"
    return res

