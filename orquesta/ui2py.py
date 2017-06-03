'''
convert Qt Designer UI files to Python code 
'''
import os
# I know, that's ugly but I love it ;-)
uidir = "ui"
uifiles = filter(lambda x: x.endswith(".ui"), os.listdir(uidir))
uifiles = map(lambda x: x.split(".")[0], uifiles)
list(map(os.system, map(lambda x: "pyuic4 -o {0}ui.py ./ui/{0}.ui".format(x), uifiles)))
os.system("pyrcc4 -py3 ./ui/resources.qrc -o resources_rc.py")
