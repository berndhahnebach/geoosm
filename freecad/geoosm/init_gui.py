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

import importlib

import FreeCADGui as Gui


wbname = "Geoosm"


class Geoosm(Gui.Workbench):
    """
    Class which gets initiated at startup of the FreeCAD GUI.
    """

    MenuText = wbname
    ToolTip = "ToolTip for {}".format(wbname)

    def Initialize(self):
        """
        Called when the workbench is first activated.
        """
        tool_count = 6
        tool_specifier_list = []
        for i in range(tool_count):
            tool_specifier_list.append("{}_{}".format(wbname, i+1))
        self.appendToolbar(wbname, tool_specifier_list)
        self.appendMenu(wbname, tool_specifier_list)

    def GetClassName(self):
        return "Gui::PythonWorkbench"


Gui.addWorkbench(Geoosm())


class TOOL1():
    def Activated(self):
        from freecad.geoosm.gui_import_osm import mydialog
        print("start the Gui in InitGui from geoosm")
        mydialog()

        print("import OSM Gui in InitGui from geoosm\n\n")

    def GetResources(self):
        return {
            "Pixmap": "python",
            "MenuText": "TOOL1",
            "ToolTip": "start osm import gui"
        }


Gui.addCommand("{}_1".format(wbname), TOOL1())


class TOOL2():
    def Activated(self):
        from freecad.trails.geomatics.geoimport.run_tests import test_import_osm

        print("run geodata test osm import")
        test_import_osm()

    def GetResources(self):
        return {
            "Pixmap": "python",
            "MenuText": "TOOL2",
            "ToolTip": "run geodat osm test import"
        }


Gui.addCommand("{}_2".format(wbname), TOOL2())


class TOOL3():
    def Activated(self):
        import freecad.geoosm.import_osm_data
        importlib.reload(freecad.geoosm.import_osm_data)

        print("Read geodata test data with my own code.")
        freecad.geoosm.import_osm_data.read_osm_sample_geoosm()

    def GetResources(self):
        return {
            "Pixmap": "python",
            "MenuText": "TOOL3",
            "ToolTip": "Read geodat test data with my own code"
        }


Gui.addCommand("Geoosm_3", TOOL3())


class TOOL4():
    def Activated(self):
        import freecad.geoosm.import_osm_data
        importlib.reload(freecad.geoosm.import_osm_data)

        print("Read Zuerich Hauptbahnhof test data with my own code.")
        freecad.geoosm.import_osm_data.read_osm_zurich()

    def GetResources(self):
        return {
            "Pixmap": "python",
            "MenuText": "TOOL4",
            "ToolTip": "reads osm data from Zuerich Hauptbahnhof"
        }


Gui.addCommand("{}_4".format(wbname), TOOL4())


class TOOL5():
    def Activated(self):
        import freecad.geoosm.import_osm_data
        importlib.reload(freecad.geoosm.import_osm_data)

        print("Read Brienzer Rothorn with elevations mapping with my own code.")
        freecad.geoosm.import_osm_data.read_osm_brienzerrothorn()

    def GetResources(self):
        return {
            "Pixmap": "python",
            "MenuText": "TOOL5",
            "ToolTip": "reads osm data from Brienzer Rothorn with elevations mapping"
        }


Gui.addCommand("{}_5".format(wbname), TOOL5())


class TOOL6():
    def Activated(self):
        import freecad.geoosm.import_osm_data
        importlib.reload(freecad.geoosm.import_osm_data)

        print("Read Alpe d’Huez with elevations mapping with my own code.")
        freecad.geoosm.import_osm_data.read_osm_alpedhuez()

    def GetResources(self):
        return {
            "Pixmap": "python",
            "MenuText": "TOOL6",
            "ToolTip": "reads osm data from Alpe d’Huez with elevations mapping"
        }


Gui.addCommand("{}_6".format(wbname), TOOL6())
