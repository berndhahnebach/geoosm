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


import FreeCADGui as Gui


class Geoosm(Gui.Workbench):
    """
    Class which gets initiated at startup of the FreeCAD GUI.
    """

    MenuText = "Geoosm"
    ToolTip = "ToolTip Geoosm"

    def Initialize(self):
        """
        Called when the workbench is first activated.
        """
        tool_specifier_list = ["Geoosm_01"]
        self.appendToolbar("Geoosm", tool_specifier_list)
        self.appendMenu("Geoosm", tool_specifier_list)

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
            "MenuText": "tool1",
            "ToolTip": "import OSM data"
        }


Gui.addCommand("Geoosm_01", TOOL1())
