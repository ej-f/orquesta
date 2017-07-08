#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
from PyQt4.QtCore import QProcess, QObject, QThread, SIGNAL
from PyQt4.QtGui import QApplication
from utils import utils, autowin

dep_dir = 'externals'

class Kitty(QObject):
    """manage kitty process (terminals)"""
    exe_name = 'kitty'
    DELAY = 150
    def __init__(self, ip, port, protocol, name, log_path, window_title, log_name, parent = None):
        QObject.__init__(self, parent)
        self.ip = ip
        self.port = port
        self.protocol = protocol
        self.log_path = log_path
        self.log_name = log_name
        self.id = str(os.getpid()) + name
        self.window_title = window_title        
        self.terminal = QProcess()
        self.terminal.finished.connect(self.close)
        self.terminal.stateChanged.connect(self.state)
        self.send_process = QProcess()
        self.send_process.finished.connect(self.end_send)
        
    def open(self):
        """ kitty -telnet -P 9696 hostname """
        if self.terminal.state() == QProcess.Running:
            return
        file_name = utils.set_log_name(self.log_name, self.log_path, ext = '.txt')
        args = [ '-{}'.format(self.protocol), self.ip,
                 '-P', self.port,
                 '-log', os.path.join(self.log_path, file_name),
                 '-title', self.window_title,
                 '-classname', self.id]
        while self.terminal.state() == QProcess.NotRunning:
            self.terminal.start(os.path.join(dep_dir,Kitty.exe_name), args)
            self.terminal.waitForStarted()
            QThread.msleep(Kitty.DELAY)
      
    def send(self, text):
        if self.send_process.state() == QProcess.Running:
            self.send_process.close()
        self.show_terminal()
        args = [ '-classname', self.id,
                 '-sendcmd', text]
        self.send_process.start(os.path.join(dep_dir, Kitty.exe_name), args)
        self.send_process.waitForStarted()
        self.send_process.waitForFinished()
        QThread.msleep(Kitty.DELAY)
        
    def show_terminal(self):
        if self.terminal.state() == QProcess.NotRunning:
            return
        autowin.show_window(autowin.get_qprocess_pid(self.terminal.pid()))
        QThread.msleep(Kitty.DELAY)
        
    @staticmethod
    def show_main():
        autowin.show_window(os.getpid())

    def end_send(self):
        pass
        
    def close(self):
        self.terminal.close()
        
    def state(self, st):
        print(st)


class KittysManager(QObject):
    """define the behaviour of a collections of kitty objects"""
    def __init__(self, terminals_group, log_path, elements, parent = None):
        QObject.__init__(self, parent)
        self.terminals_group = terminals_group
        self.elements = elements
        for element in self.elements.dic:
            windows_title = '{} {} {}'.format(terminals_group, element, self.elements.dic[element]['ip'])
            log_name  = '{}_{}'.format(terminals_group, element) 
            self.elements.dic[element]['process'] = Kitty(self.elements.dic[element]['ip'], 
                                                            self.elements.dic[element]['port'], 
                                                            self.elements.dic[element]['protocol'],
                                                            element, log_path, windows_title, log_name)
    def send(self, text, move_next = True):
        """ send a string to all selected terminals"""
        actives = self.elements.get_actives()
        any_closed = self.verify_selected()
        if any_closed:
            self.emit(SIGNAL('terminals_closed'), 'The following terminals are closed:\n' + ', '.join(any_closed))
        else:
            for element in actives:
                if type(text) == utils.Var:
                    self.elements.dic[element]['process'].send(text.stringOfElement(element).strip())
                else:
                    self.elements.dic[element]['process'].send(text.strip())
            if move_next:
                self.emit(SIGNAL('move_next'))
        Kitty.show_main()

    
    def verify_selected(self):
        """return a list of terminals that are selected but not running"""
        return [element for element in self.elements.get_actives() if self.elements.dic[element]['process'].terminal.state() == QProcess.NotRunning]

    
    def get_runnings(self):
        """return a list of all running terminals"""
        return [element for element in self.elements.dic if self.elements.dic[element]['process'].terminal.state() == QProcess.Running]
                
    def elements_to_close(self):
        actives = set(self.elements.get_actives())
        runnings = set(self.get_runnings())
        return list(actives & runnings)
        
    def view(self):
        actives = self.elements.get_actives()
        for element in actives:
            self.elements.dic[element]['process'].show_terminal()
        Kitty.show_main()
    
    def close(self):
        elements_to_close = self.elements_to_close()
        for element in elements_to_close:
            self.elements.dic[element]['process'].close()
        Kitty.show_main()
    
    def open(self):
        actives = self.elements.get_actives()
        for element in actives:
            self.elements.dic[element]['process'].open()             
        Kitty.show_main()
           
    def kill_all(self):
        for element in self.elements.dic:
            if self.elements.dic[element]['process'].terminal.state() == QProcess.Running:
                self.elements.dic[element]['process'].terminal.close()
                   
    def any_open(self):
        for element in self.elements.dic:
            if self.elements.dic[element]['process'].terminal.state() == QProcess.Running:
                return True
        return False

    
class Commands(QObject):
    """contain the logic that map strings (commands) into function calls """
    def __init__(self, kittysmanager, mylistwidget, init_var = {}, parent = None):
        QObject.__init__(self, parent)
        self.mylistwidget = mylistwidget
        self.kittysmanager = kittysmanager
        self.var = init_var
        self.command = None
        self.move_next = False
        self.mainsel_elements = None
        self.commanddict = {'mainsel' : self.mainsel, 
                            'sel' : self.sel, 
                            'open' : self.open, 
                            'send' : self.send,
                            'view' : self.view, 
                            '#' : self.comment, 
                            'set' : self.set,
                            'inv' : self.inv, 
                            'gsend' : self.sendg, 
                            'close' : self.close}
    
    def call(self, line, move_next = True, decrement = 2):
        self.move_next = move_next
        error = False
        try:
            self.valid_command(line)
            if self.command:
                self.commanddict[self.command](line[len(self.command):])
            else:
                self.send(line)
        except ValueError:
            error = True
        if not error and self.command != '#':
            self.emit(SIGNAL('set_tracking_mark'), decrement) 
        
    def open(self, arg):
        self.kittysmanager.open()
        self.verify_nextline()
    
    def send(self, arg):
        arg = self.line_substitution(arg)
        self.kittysmanager.send(arg, move_next = self.move_next)
    
    def sendg(self, arg):
        arg = self.line_substitution(arg)
        var = utils.Var('var', self.kittysmanager.terminals_group, arg)
        self.kittysmanager.send(var, move_next = self.move_next)
    
    def close(self, arg):
        elements_to_close = self.kittysmanager.elements_to_close()
        if elements_to_close:
            self.emit(SIGNAL('close_terminals'), 'The following terminals are running:\n{}\nDo you want to close them?'.format(', '.join(elements_to_close)))
    
    def comment(self, arg):
        self.verify_nextline()
    
    def view(self, arg):
        self.kittysmanager.view()
        self.verify_nextline()
        
    def set(self, arg):   
        args = self.parse_line(arg)
        if len(args) < 2:
            self.emit(SIGNAL('wrong_set'), 'set require two parameters')
            raise ValueError('the instruction set require two parameters')
        else:
            key = args[0]
            value =  arg[len(key)+1:].strip()
            self.var[key] = value
            self.verify_nextline()

    def sel(self, arg):
        arg = self.line_substitution(arg)
        args = self.parse_line(arg)
        if self.mainsel_elements:
            if 'all' in args:
                args = self.mainsel_elements
            else:
                args = list(set(args) & set(self.mainsel_elements))
                
        if self.mylistwidget.select_elements(args):
            self.verify_nextline()
        else:
            self.move_next = False
            raise ValueError('Invalid element names')
    
    def mainsel(self, arg):
        arg = self.line_substitution(arg)
        args = self.parse_line(arg)
        if self.mylistwidget.select_elements(args):
            self.mainsel_elements = args
            self.verify_nextline()
        else:
            self.mainsel_elements = None
            raise ValueError('Invalid element names')
        
    def reset_var(self):
        self.var = {}
        
    def inv(self, arg):
        self.mylistwidget.invert_selection()
        self.verify_nextline()
        
    @staticmethod        
    def parse_line(line):
        return line.strip().split()
        
    def line_substitution(self, arg):
        return utils.safe_dict_substitution(arg, self.var)
            
    def valid_command(self, line):
        self.command = set([line.strip().split(' ')[0]]) & set(self.commanddict.keys())
        if self.command:
            self.command = list(self.command)[0]
        else:
            self.command = None
    
    def verify_nextline(self):
        if self.move_next:
            self.emit(SIGNAL('move_next'))
            
     
if __name__ == '__main__':
    ip = '127.0.0.1'
    identifier = 'test'
    log_path = 'C:\\'
    app = QApplication(sys.argv)
    kit = Kitty(ip, '22', 'ssh', identifier, log_path, identifier, identifier)
    kit.open()
    kit.send('john')
    kit.send('doe')
    app.exec_() 


