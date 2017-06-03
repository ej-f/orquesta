# -*- coding: utf-8 -*-
import os, re
import configparser
from collections import OrderedDict

def set_log_name(file_name, path = './', ext = '.txt'):
    """ if the log file already exist, return the name with a numeric prefix"""
    exists = lambda  name : os.path.isfile(os.path.normpath(os.path.join(path, name + ext)))
    if exists(file_name):
        i = 0
        fileaux = file_name
        while exists(fileaux):
            i += 1
            fileaux = file_name + '_{}'.format(i)
        return fileaux + ext
    else:
        return file_name + ext


class Var():
    extention = '.txt'
    def __init__(self, path, terminals_group, string):
        self.dic = self.conf2dict(terminals_group, path)
        self.string = string
    
    def conf2dict(self, group, path):
        parser = configparser.SafeConfigParser(interpolation = configparser.ExtendedInterpolation())
        parser.read(os.path.join(path, group + self.extention))
        dic = {}
        for section in parser.sections():
            dic[section] = {}
            dic[section]['id'] = section
            for name, _ in parser.items(section):   
                dic[section][name] = parser.get(section, name)
        return dic
    
    def elementDic(self, element):
        if 'global' in self.dic:
            aux = {keys:values for keys, values in self.dic['global'].items()}
            for key, values in self.dic[element].items():
                aux[key] = values
            return aux
        return self.dic[element]
    
    def stringOfElement(self, element):
        try:
            return safe_dict_substitution(self.string, self.elementDic(element))
        except KeyError:
            return self.string
    
    class NoGlobal(Exception):
        def __init__(self):
            print('\'global\' must be included')

def safe_dict_substitution(format_str, dic):
    for e in dic:
        if '$' + e  in format_str:
            format_str = re.sub('\$' + e , dic[e], format_str)
    return format_str


cfgdir = './cfg'

class Elements():
    def __init__(self, platform):
        self.dic = self.conf2dict(platform)
    
    def conf2dict(self, group):
        """return a dictionary from a configuration file"""
        parser = configparser.SafeConfigParser()
        parser.read(cfgdir + '/' + group + '.cfg')
        dic = OrderedDict()
        for section in parser.sections():
            dic[section] = {}
            dic[section]['ip'] = parser.get(section, 'ip')
            dic[section]['protocol'] = parser.get(section, 'protocol', fallback = 'ssh')
            dic[section]['active'] = False
            if dic[section]['protocol'] == 'ssh':
                dic[section]['port'] = parser.get(section, 'port', fallback = '22')
            else:
                dic[section]['port'] = parser.get(section, 'port', fallback = '23')
            dic[section]['process'] = None
            for name, value in parser.items(section):
                if name not in dic[section]:
                    dic[section][name] = value
        return dic
    
    def getDic(self, key = 'process'):
        """return the list of processes of all active terminal"""
        return [self.dic[terminal][key] for terminal in self.dic if self.dic[terminal]['active']]
    
    def get_actives(self):
        """return the names of all active elements"""
        return [element for element in self.dic if self.dic[element]['active']]


if __name__ == '__main__':
    pass


    
    
