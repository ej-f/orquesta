# -*- coding: utf-8 -*-
import win32con
import win32gui
import win32process
import time
import ctypes
from ctypes.wintypes import DWORD, HANDLE


def get_hwnds(pid):
    """return a list of window handlers based on it process id"""
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                hwnds.append(hwnd)
        return True
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds

def show_window(pid, delay = 0.5):
    """set a windows as principal based on it's process id"""
    time.sleep(delay)
    for hwnd in get_hwnds(pid):
        win32gui.SetForegroundWindow(hwnd)
        win32gui.ShowWindow(hwnd, win32con.SW_NORMAL)
        

class WinProcInfo(ctypes.Structure):
    _fields_ = [
        ('hProcess', HANDLE),
        ('hThread', HANDLE),
        ('dwProcessID', DWORD),
        ('dwThreadID', DWORD),
        ]

def get_qprocess_pid(voidptr):
    LPWinProcInfo = ctypes.POINTER(WinProcInfo)
    lp = ctypes.cast(int(voidptr), LPWinProcInfo)
    return lp.contents.dwProcessID

if __name__ == '__main__':
    pid = 10116
    show_window(pid)