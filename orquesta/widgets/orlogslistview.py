#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
from PyQt4.QtCore import Qt, QDir, QUrl
from PyQt4.QtGui import QDesktopServices, QApplication, QItemSelectionModel, QFileSystemModel, QListView
 

class OrLogsListView(QListView):
    def __init__(self, parent = None):
        super(OrLogsListView, self).__init__(parent)
        self.model = QFileSystemModel()
        self.model.sort(3, Qt.DescendingOrder)
        self.model.setFilter(QDir.Files)
        self.setModel(self.model)
        
    def mouseDoubleClickEvent(self, event):
        """method override"""
        QListView.mouseDoubleClickEvent(self, event)
        self.clicked()
        
    def getSelectedPath(self):
        """Return selected filename"""
        index = self.currentIndex()
        if index:
            return os.path.normpath(self.model.filePath(index))
        
    def clicked(self):
        fname = self.getSelectedPath()
        if fname:
            self.open(fname)
                
    def open(self, fname):
        QDesktopServices.openUrl(QUrl('file:///' + fname))

    def setup(self, wdir = '.'):
        os.makedirs(wdir , exist_ok = True)
        self.model.setRootPath(wdir)
        self.setRootIndex(self.model.index(wdir))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tree = OrLogsListView()
    tree.setup( '../logs/default' )
    tree.show()
    app.exec_()
