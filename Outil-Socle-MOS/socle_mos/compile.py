# Build QGIS plugin ui and resource files in the current directory
# Use: python compile.py
# Must be run from the OSGeo4W shell

import glob
import os
import subprocess

ui_files = glob.glob('*.ui')
for ui in ui_files:
    (name, ext) = os.path.splitext(ui)
    print "pyuic4 -o {}.py {}".format(name, ui)
    subprocess.call(["pyuic4.bat", "-o", "{}.py".format(name), ui])

rc_files = glob.glob('*.qrc')
for rc in rc_files:
    (name, ext) = os.path.splitext(rc)
    print "pyrcc4.exe -o {}_rc.py {}".format(name, rc)
    subprocess.call(["pyrcc4.exe", "-o", "{}_rc.py".format(name), rc])


rc_files = glob.glob('forms/*.qrc')
for rc in rc_files:
    (name, ext) = os.path.splitext(rc)
    print "pyrcc4.exe -o {}_rc.py {}".format(name, rc)
    subprocess.call(["pyrcc4.exe", "-o", "{}_rc.py".format(name), rc])