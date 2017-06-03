#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
from PyQt4.QtCore import Qt, QDir, QUrl
from PyQt4.QtGui import QDirModel, QTreeView, QDesktopServices, QApplication, QItemSelectionModel
 
class FileSystemModel(QDirModel):
    def __init__(self, parent=None):
        """ Custom QDirModel with Drag & Drop support """
        self.parent = parent
        super(FileSystemModel, self).__init__(parent)

    def columnCount(self, index):
        return 1
        
    def flags(self, index):
        if index.isValid() and self.isDir(index):
            return Qt.ItemIsDropEnabled | Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled


class OrTreeView(QTreeView):
    def __init__(self, parent=None):
        super(OrTreeView, self).__init__(parent)
        self.model = FileSystemModel()
        self.model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)
        self.model.setSorting(QDir.DirsFirst)
        self.setModel(self.model)
        
    def mouseDoubleClickEvent(self, event):
        """method override"""
        QTreeView.mouseDoubleClickEvent(self, event)
        self.clicked()
        
    def getSelectedPath(self):
        """Return selected filename"""
        index = self.currentIndex()
        if index:
            return os.path.normpath(str(self.model.filePath(index)))
        
    def clicked(self):
        fname = self.getSelectedPath()
        if fname:
            if os.path.isdir(fname):
                self.model.refresh()
            else:
                self.open(fname)
                
    def open(self, name):
        QDesktopServices.openUrl(QUrl('file://'+name))


    def setup(self, root_dir = './', wdir = '.'):
        self.root_dir = root_dir
        self.wdir = wdir
        os.makedirs(root_dir , exist_ok = True)
        os.makedirs(wdir , exist_ok = True)
        self.model.setFilter(QDir.NoDotAndDotDot | QDir.AllEntries)
        self.setModel(self.model)
        self.setRootIndex(self.model.index(self.root_dir))
        self.selectionModel().setCurrentIndex(self.model.index(self.wdir), QItemSelectionModel.Select)
        self.setAnimated(False)
        self.setIndentation(20)
        self.setHeaderHidden(True)
        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tree = OrTreeView()
    tree.setup('logs', 'logs\default')
    tree.show()
    app.exec_()
