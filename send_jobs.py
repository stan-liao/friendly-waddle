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
from bs4 import BeautifulSoup
import json

print(os.getcwd())

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

def get_roles(role_text):
    soup = BeautifulSoup(role_text, "html.parser")
    role_text = soup.get_text()
    title = role_text.find("Title:")
    dpt_loc = role_text.find("Department:")
    title = role_text[title+6:dpt_loc]
    dpt = role_text[dpt_loc+11:]
    return title, dpt

def is_uni(uni):
    if len(uni) == 6 and uni[0].isalpha() and uni[1].isalpha() and uni[2:].isdigit():
        return True
    elif len(uni) == 7 and uni[0].isalpha() and uni[1].isalpha() and uni[2].isalpha() and uni[3:].isdigit():
        return True
    else:
        return False

#turn name from last, first middle to first middle last
def rework_name(name):
    name = name.split(", ")
    name = name[1] + " " + name[0]
    return name

def print_all(json_file, print_files):
    #iterate through all entries in json file
    i = 0

    for entry in json_file:
        #print each file
        to_print = print_files[i]
        i = (i+1)%len(print_files)
        
        #check if string is in form letter letter number number number number
        try:
            uni = entry["email"].split("@")[0]
        except:
            #no email entry
            continue

        role = entry["role"]
        title, dpt = get_roles(role)
        name = rework_name(entry["name"])        

        if is_uni(uni) and (title == "Student, COLUMBIA COLLEGE" or
                            title == "Student, FU FOUNDATN SCHL OF ENGINEERING & APPLIED SCIENCE:UGRAD"):
            print("found one that works?")
            text =  "Hello " + name + "\n\n"
            text += "Good luck on your " + dpt + " finals!\n\n"
            text += to_print

            #write text string to file
            with open("temp.txt", "w") as f:
                f.write(text)
            print_file("temp.txt", uni)
            return
    

#main function here
if __name__ == "__main__":
    filenames = ["job1.txt", "job2.txt"]

    print_files = []

    #read filenames into strings
    for file in filenames:
        with open(file, "r") as f:
            text = f.read()
            print_files.append(text)

    #read json into dictionary
    with open("scraper/data2.json", "r") as f:
        json_file = json.load(f)

    print_all(json_file, print_files)
