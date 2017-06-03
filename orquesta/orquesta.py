# -*- coding: utf-8 -*-
import sys, os, re
from PyQt4.QtCore import (SIGNAL, QUrl)
from PyQt4.QtGui import (QDialog, QApplication, QMainWindow, QFileDialog,
                          QDesktopWidget, QMessageBox, QDesktopServices, QAction)
import initwindowui, mainwindowui
import terminals
from utils import utils
import functools as ft


class InitWindow(QDialog, initwindowui.Ui_Dialog):
    cfg_path = 'cfg'
    default_log_path = os.path.join(os.getcwd(), 'logs')
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle('New project')
        self.setFixedSize(320, 100)
        self.mainwindow = None
        self.project_name = ''
        self.lineedit_log_path.setText(self.default_log_path)
        for groups in os.listdir(self.cfg_path):
            self.combobox_term_group.addItem(groups.split('.')[0])
        self.connect(self.button_log_path, SIGNAL('clicked()'), self.slot_change_log_path)
            
    def slot_change_log_path(self):
        path = QFileDialog.getExistingDirectory(self, caption='select log path', directory='.', options = QFileDialog.ShowDirsOnly)
        if path:
            self.lineedit_log_path.setText(path)

    def accept(self):
        # ensuring a valid path name 
        self.project_name = re.sub(r'[^a-zA-Z0-9\-\(\) \t\r\n\v\f]+', '_', self.lineedit_project_name.text())
        self.close()
        self.mainwindow = MainWindow(self.project_name, self.combobox_term_group.currentText(), logs_dir = self.lineedit_log_path.text())
        self.mainwindow.show()
        

class MainWindow(QMainWindow, mainwindowui.Ui_MainWindow):    
    default_log_dir = 'default'
    var_path = os.path.join(os.getcwd(), 'var')
    def __init__(self, project_name, terminal_group = 'test', logs_dir = 'logs' , parent = None):    
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.script_name = '{}script.txt'.format(terminal_group)
        self.logs_dir = logs_dir
        self.teminal_group = terminal_group
        self.template_dir = os.path.join('templates', self.teminal_group)
        self.load_geometry()
        self.cfg_path = os.path.abspath(os.path.join('cfg', self.teminal_group + '.cfg' ))
        self.elements = utils.Elements(terminal_group)
        self.setup_listwidget()
        self.project_name = project_name
        self.init_window = None
        self.setcwd()
        self.setWindowTitle(self.windowTitle() + ' ( {} - {} )'.format(self.project_name, terminal_group))
        self.kittysmanager = terminals.KittysManager(terminal_group, self.wdir, self.elements)
        self.commands = terminals.Commands(self.kittysmanager, self.listwidget)
        self.connect_custom_signals()
        self.template_action_list = []
        self.add_templates()
        os.makedirs(self.logs_dir, exist_ok = True)
        os.makedirs(self.wdir, exist_ok = True)
        self.treeview.setup(root_dir = os.path.normpath(self.logs_dir), wdir = os.path.normpath(self.wdir))
        self.connect_actions()
        self.script_file_path = os.path.join(self.wdir, self.script_name)
        self.load_script()
        self.sciscintilla.textChanged.connect(self.verify_set_lines)
    
    def connect_custom_signals(self):
        self.connect(self.kittysmanager, SIGNAL('terminals_closed'), self.warning)
        self.connect(self.kittysmanager, SIGNAL('move_next'), self.sciscintilla.cursor_next_line)
        self.connect(self.commands, SIGNAL('wrong_set'), self.warning)
        self.connect(self.commands, SIGNAL('set_tracking_mark'), self.set_traking_mark)
        self.connect(self.commands, SIGNAL('move_next'), self.sciscintilla.cursor_next_line)
        self.connect(self.commands, SIGNAL('close_terminals'), self.close_terminals)
        self.connect(self.listwidget, SIGNAL('incorrect_names'), self.warning)
    
    def connect_actions(self):
        self.connect(self.action_exit, SIGNAL('triggered()'), self.close)
        self.connect(self.action_open_terminals, SIGNAL('triggered()'), self.open_terminals)
        self.connect(self.action_send, SIGNAL('triggered()'), lambda : self.process_line(move_next=False, decrement = 1))
        self.connect(self.action_send_move_next, SIGNAL('triggered()'), lambda : self.process_line(move_next=True, decrement = 2))
        self.connect(self.action_about, SIGNAL('triggered()'), self.about)
        self.action_new.triggered.connect(self.new_project)
        self.action_save.triggered.connect(self.save_script)
        self.action_edit_var_file.triggered.connect(lambda : self.open_file( os.path.join(self.var_path, self.teminal_group + '.txt')) )
        self.action_unselect_all.triggered.connect(lambda : self.listwidget.select(False))
        self.action_select_all.triggered.connect(lambda : self.listwidget.select(True))
        self.action_invert.triggered.connect(self.invert)
        self.action_close_terminals.triggered.connect(self.close_selection)
        self.action_save_as_template.triggered.connect(lambda : self.save_file(self.template_dir, "Save as template"))
        self.action_open_local_term.triggered.connect(self.open_local_term)
        self.action_open_local_dir.triggered.connect(self.open_local_dir)
        self.action_edit_config.triggered.connect(lambda : self.open_file(self.cfg_path))
        self.action_restart.triggered.connect(self.restart)
        
    def setcwd(self):
        """define current working directory"""
        if self.logs_dir == InitWindow.default_log_path and not self.project_name:
            self.wdir = os.path.join(self.logs_dir, self.default_log_dir)
            self.project_name = 'default'
        elif self.logs_dir == InitWindow.default_log_path and self.project_name:
            self.wdir = os.path.join(self.logs_dir, self.project_name )
        elif self.logs_dir != InitWindow.default_log_path and self.project_name:
            self.wdir = os.path.join(self.logs_dir, self.project_name )
        else:
            self.wdir = self.logs_dir
            self.project_name = os.path.basename(self.wdir)
         
    def slot_set_modify_line(self, prefix, line, index):
        setline = self.sciscintilla.text(line)
        if setline.startswith(prefix) and len(setline.split()) >= 3:
            self.commands.call(setline, move_next = False, line = line )
  
    def load_geometry(self):
        """ align window on screen """
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width()*0.97) - (self.frameSize().width()),
            (resolution.height() / 2) - (self.frameSize().height() / 2))
  
    def verify_set_lines(self):
        """ read all the lines in the editor (OrSciScintilla) to verify if contain set commands """
        self.commands.reset_var()
        for line in range(self.sciscintilla.lines()):
            self.slot_set_modify_line('set', line, 0)  
               
    def load_script(self):
        """load script located in current working directory"""
        if os.path.exists(self.script_file_path):
            script_file = open(self.script_file_path, newline = '\n')
            self.sciscintilla.setText(script_file.read())
            script_file.close()
        self.verify_set_lines()
         
    def save_script(self):
        script_file = open(self.script_file_path, 'w', newline = '\n')
        script_file.write(self.sciscintilla.text())
        script_file.close()
     
    def new_project(self):
        """close the main window an open an init window"""
        self.init_window = InitWindow()
        self.close()
        self.init_window.show()
               
    def setup_listwidget(self):
        self.listwidget.add_items(self.elements.dic, all_actives = False)
    
    def open_file(self, path):
        if os.path.isfile(path):
            QDesktopServices.openUrl(QUrl('file:///' + path))
        else:
            QMessageBox.warning(self, 'File doesn\'t exist','Var file not found for {}'.format(self.teminal_group))
    
    def open_local_term(self):
        """open windows cmd in cwd"""
        command = 'start cmd /K "cd ' + self.wdir + '"'
        os.system(command)     
    
    def open_local_dir(self):
        """open file explorer in cwd"""
        command = 'explorer /e,"' + self.wdir + '"'
        os.system(command)

    def restart(self):
        self.new_windows = self.__init__(self.project_name, self.teminal_group, self.logs_dir)
        self.close()
        
    def open_terminals(self):
        """ Open selected terminals """
        self.commands.call('open', move_next = False)

    def invert(self):
        """ Invert current selection """
        self.commands.call('inv')
     
    def close_selection(self):
        """ Close selected terminals """
        self.commands.call('close')        
 
    def process_line(self, move_next = True, decrement = 2):
        line = self.sciscintilla.get_current_line().strip()
        self.commands.call(line, move_next, decrement)
     
    def close_all_terminals(self):
        self.kittysmanager.kill_all()
                     
    def closeEvent(self, event):
        """ method override """
        if self.kittysmanager.get_runnings():
            reply = QMessageBox.question(self, 'Open terminals',
            'If you close the application, all open terminals also will does. Do you want to continue?', QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
                self.close_all_terminals()
            else:
                event.ignore()
                 
    def close_terminals(self, msg):
        reply = QMessageBox.question(self, 'Open terminals', msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.kittysmanager.close()

    def set_traking_mark(self, decrement = 2):
        self.sciscintilla.set_tracking_mark(self.sciscintilla.getLineNumber() - decrement)
 
    def save_file(self, directory, caption):
        filename = QFileDialog.getSaveFileName(self, caption = caption, directory = directory, filter = '*.txt')
        if filename:
            s = open(filename, 'w', newline = '\n')
            s.write(self.sciscintilla.text())
            s.close()
             
    def add_templates(self):
        """add templates to the menu"""
        template_path_list = []
        if os.path.exists(self.template_dir):
            list_dir = os.listdir(self.template_dir)
            list_dir = filter(lambda x : x.endswith('.txt'), list_dir)
            for n, file_name in enumerate(list_dir):
                sp = file_name.split('.')
                if len(sp) == 2 and sp[1] == 'txt':
                    template_name = sp[0].replace('_', " ")
                    self.template_action_list.append(QAction(self))
                    self.template_action_list[n].setText(template_name)
                    template_path_list.append(os.path.normpath(os.path.join(self.template_dir, file_name)))
            for n, template_path in enumerate(template_path_list):
                self.template_action_list[n].triggered.connect(ft.partial(self.insert_template, template_path))
                self.menu_templates.addAction(self.template_action_list[n])
        else:
            os.makedirs(self.template_dir, exist_ok = True)
         
    def insert_template(self, template_path):
        """ insert selected template into the editor"""
        if template_path and os.path.isfile(template_path):
            template_name  = os.path.basename(template_path)
            template_file = open(template_path, newline = '\n')
            file_text = template_file.read()
            template_file.close()
            self.sciscintilla.insert(file_text)
            self.sciscintilla.insert('# Template - {}\n'.format(template_name))
        self.verify_set_lines()
 
    def about(self):
        QMessageBox.about(self,
                          'About Orquesta',
                          """<p>author: Edgar Fuentes (<a href=\"mailto:fuentesej@gmail.com\">fuentesej@gmail.com</a>)</p>
                          <p>license: GPL 3.0</p>
                          <p>github: <a href=\"https://github.com/ej-f/orquesta\">https://github.com/ej-f/orquesta</a></p>
                          <p>version: 0.1.0</p>
                          """
                          )
         
     
    def warning(self, st):
        QMessageBox.warning(self, 'Warning', st + '\nline: {}'.format(self.sciscintilla.getLineNumber()))

def main():
    app = QApplication(sys.argv)
    app.setStyle('plastique')
    initwindow = InitWindow()
    initwindow.show()
    app.exec_()
    

if __name__ == '__main__':
    main()
