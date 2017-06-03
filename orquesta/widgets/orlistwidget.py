# -*- coding: utf-8 -*-
import sys
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QListWidget, QListWidgetItem, QFont, QColor, QListView, QAbstractItemView, QApplication
sys.path.append('..')

class OrListWidgetItem(QListWidgetItem):
    """items base component"""
    COLOR = ['#FFFFFF', '#90EE90']
    def __init__(self, active = True, parent = None):
        self.active = active
        QListWidgetItem.__init__(self, parent)
        self.set_color()
        font = QFont(QFont.SansSerif);
        font.setStyleHint(QFont.Monospace);
        font.setPointSize(10);
        font.setFixedPitch (True);
        self.setFont(font);
        self.setTextAlignment(4)

    def set_color(self):
        self.setBackgroundColor(QColor(OrListWidgetItem.COLOR[self.active]))

    def change(self, element_dic):
        self.active = not self.active 
        self.set_color()
        element_dic[self.text()]['active'] = self.active



class OrListWidget(QListWidget):
    """ list used for terminals selection """
    def __init__(self, parent = None):
        QListWidget.__init__(self, parent)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setMovement(QListView.Static)
        self.setProperty('isWrapping', False)
        self.setLayoutMode(QListView.SinglePass)
        self.setSelectionRectVisible(False)
        self.uniformItemSizes()
        self.wordWrap()
        self.clicked.connect(self.slotSelect)
        self.itemActivated.connect(self.slotSelect)
        self.dic = None
      
    def add_item(self, name, tooltip = "", all_actives = True):
        mlwi = OrListWidgetItem(all_actives, parent = name)
        mlwi.setToolTip(tooltip)
        self.addItem(mlwi)

    def add_items(self, dic, all_actives = True):
        self.dic = dic
        for key in self.dic:
            self.add_item(key, tooltip = '{}\nip: {}\nprotocol: {}\nport:{}'.format(key, 
                                                                                    self.dic[key]['ip'], 
                                                                                    self.dic[key]['protocol'], 
                                                                                    self.dic[key]['port']), 
                          all_actives = all_actives)
    def slotSelect(self):
        self.currentItem().change(self.dic)
    
    def get_actives(self):
        return [self.item(n).text() for n in range(self.count()) if self.item(n).active]
    
    def select(self, selall = True):
        for n in range(self.count()):
            if self.item(n).active != selall:
                self.item(n).change(self.dic)
    
    def get_items(self):
        return [self.item(n) for n in range(self.count())]
              
    def select_elements(self, names):
        """  return True if the selection is possible """
        incorrect_names = self.check_names(names)
        if incorrect_names:
            self.emit(SIGNAL('incorrect_names'), 'the following names are incorrect: \n' + ', '.join(incorrect_names))
            return False
        if 'all' in names:
            self.select(True)
            return True
        #selected_items = [self.findItems(name, Qt.MatchExactly)[0] for name in names]
        for item in self.get_items():
            item_text = item.text()
            if item_text in names and not item.active:
                item.change(self.dic)
            elif not (item_text in names) and item.active:
                item.change(self.dic)
        return True
    
    def check_names(self, names):
        """ return a list of all incorrect names trying to select """
        incorrect_names =  set(names) - set(list(self.dic.keys()) + ['all'])
        return list(incorrect_names)
                
    def invert_selection(self):
        for item in self.get_items():
            item.change(self.dic)
                
if __name__ == '__main__':
    from utiles import utiles
    import os
    os.chdir('..')
    app = QApplication(sys.argv)
    mylist = OrListWidget()
    mylist.add_items(utiles.Elements('test').dic, all_actives = True)
    mylist.select_elements(['foo', 'bar'])
    mylist.invert_selection()
    mylist.select_elements(['foo', 'bar'])
    mylist.show()
    app.exec_()
