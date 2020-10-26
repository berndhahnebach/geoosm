# outside FreeCAD
import sys
sys.path.append("/home/hugo/.FreeCAD/Mod/geodata/sidepackages_geodata")
import srtm
eledata = srtm.get_data()
eledata.get_elevation(50.8682, 7.1377)
eledata.get_elevation(46.503, 8.035)


# inside FreeCAD
from sidepackages_geodata import srtm
eledata = srtm.get_data()
eledata.get_elevation(50.8682, 7.1377)
eledata.get_elevation(46.503, 8.035)


"""
eledata.get_elevation(46.503, 8.035)
# should be 2773.88

>>> eledata.get_elevation(46.503, 8.035)
4 2884802
2723
"""


# **************************************************************************
# https://pypi.org/project/SRTM.py/
# https://github.com/tkrajina/srtm.py

elevation_data = srtm.get_data()
print('CGN Airport elevation (meters):', elevation_data.get_elevation(50.8682, 7.1377))
# /home/hugo/.cache/srtm is used


elevation_data_with_custom_dir = srtm.get_data(local_cache_dir="tmp_cache")
print('CGN Airport elevation (meters):', elevation_data_with_custom_dir.get_elevation(50.8682, 7.1377))
