#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtDesigner
import orsciscintilla

class OrSciScintillaPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin):
    def __init__(self, parent=None):
        super(OrSciScintillaPlugin, self).__init__(parent)
        self.initialized = False

    def initialize(self, core):
        if self.initialized:
            return
        self.initialized = True

    def isInitialized(self):
        return self.initialized

    def createWidget(self, parent):
        return orsciscintilla.OrSciScintilla(parent)

    def name(self):
        return "OrSciScintilla"

    def group(self):
        return "Or Widgets"

    def icon(self):
        return QtGui.QIcon(_logo_pixmap)

    def toolTip(self):
        return ""

    def whatsThis(self):
        return ""

    def isContainer(self):
        return False

    def domXml(self):
        return '<widget class="OrSciScintilla" name="OrSciScintilla" />\n'

    def includeFile(self):
        return "widgets.orsciscintilla"


_logo_16x16_xpm = [
"16 16 46 1",
". c #a5a5dc",
"l c #a69fd6",
"k c #a7a5da",
"h c #a7a6dc",
"a c #a7a7de",
"Q c #a8a5da",
"s c #a9a7d7",
"R c #a9a9e0",
"z c #abaad4",
"E c #afafda",
"M c #afafdb",
"K c #b0a8e2",
"o c #b1afe4",
"p c #b2b2d7",
"# c #b2b2ed",
"i c #b39eb6",
"F c #b3b3e1",
"e c #b4b4ef",
"t c #b58bab",
"d c #b6b6f2",
"n c #b798b8",
"P c #b798b9",
"c c #b8b6f2",
"D c #b8b89c",
"m c #b9648d",
"J c #ba84b0",
"A c #bdbdfb",
"f c #bfbffe",
"g c #c06996",
"b c #c0c0ff",
"B c #cbb889",
"L c #cbb989",
"O c #cfcf87",
"I c #d09585",
"w c #d0cf86",
"x c #dede81",
"G c #e8e87c",
"q c #edde7b",
"N c #f1e07b",
"v c #f2e07b",
"H c #f6e57c",
"j c #fb917e",
"u c #ffb580",
"r c #ffda80",
"C c #fffe80",
"y c #ffff80",
".##############a",
"#bbbbbbbbcdbbbbe",
"#bbbbbbbfghbbbbe",
"#bbbbbbbijkbbbbe",
"#blmnobpqrsbbbbe",
"#bbtuvwxyyzbbbbe",
"#bbABCyyyyDEfbbe",
"#bbbFGyyyyyHIJKe",
"#bbbFGyyyyyHIJKe",
"#bbALCyyyyDMfbbe",
"#bbtuNOxyyzbbbbe",
"#blmPobpqrsbbbbe",
"#bbbbbbbijQbbbbe",
"#bbbbbbbfghbbbbe",
"#bbbbbbbbcdbbbbe",
"aeeeeeeeeeeeeeeR"]

_logo_pixmap = QtGui.QPixmap(_logo_16x16_xpm)