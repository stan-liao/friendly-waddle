# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 21:43:47 2023

@author: Stan
"""


#assumes pawprint is your default printer 
import os
import win32ui
import win32com.client
import time

#prints filename to destination uni
def print_file(filename, uni):
    #currently syntax only works with windows
    os.startfile(filename, "print")
    current_window = ""
    while current_window != "MainForm":
        try:    
            current_window = win32ui.GetForegroundWindow().GetWindowText()
        except:
            continue
        
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys(uni+"{ENTER}")
    
    return


start = time.perf_counter()
print_file("test.docx", "")
end = time.perf_counter()

print(end - start)