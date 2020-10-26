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
"""gui for import data from openstreetmap"""


from freecad.trails.guigeoimport.gui_import_osm import MyApp


# the gui backend child
class MyOSMImportApp(MyApp):
    """execution layer of the Gui"""

    def __init__(self):
        super(MyOSMImportApp, self).__init__()
        print("__init__ MyOSMImportApp in gui_import_osm from geoosm")

    def import_osm(self, lat, lon, bk, progressbar, status, elevation):
        """
        import the osm data by the use of import_osm module
        """

        print("import_osm from geoosm")
        from freecad.geoosm.import_osm import import_osm2
        has_finished = import_osm2(
            lat,
            lon,
            bk,
            progressbar,
            status,
            elevation
        )
        return has_finished


# the gui startup
def mydialog():
    """ starts the gui dialog """

    print("mydialog Gui in gui_import_osm from geoosm")

    app = MyOSMImportApp()

    from freecad.trails.geoimport import miki
    my_miki = miki.Miki()
    my_miki.app = app
    app.root = my_miki

    from freecad.trails.guigeoimport.miki_import_osm import s6
    my_miki.parse2(s6)
    my_miki.run(s6)

    print("before return dialog Gui in gui_import_osm from geoosm")

    return my_miki
