# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 21:43:47 2023

@author: Stan
"""


#assumes pawprint is your default printer 
import os
import win32ui
import win32com.client
from bs4 import BeautifulSoup
import json
import argparse
import pandas as pd

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
    #strip whitespace from end of name
    name = name.strip()
    name = name.split(", ")
    name = name[1] + " " + name[0]
    return name

#reads a json from a directory, parses it into a dataframe
def read_dir_json(json_file):
    df = pd.DataFrame(columns=["name", "email", "uni", "title", "department"])
    my_list = []
    for entry in json_file:
        dict = {}

        #check if valid email address
        try:
            dict["uni"] = entry["email"].split("@")[0]
        except:
            #invalid email entry
            continue
        role = entry["role"]
        dict["title"], dict["dpt"] = get_roles(role)
        name = rework_name(entry["name"])   
        dict["name"] = entry["name"]
        my_list.append(dict)
    
    #list of dicts to dataframe
    df = pd.DataFrame.from_dict(my_list)
    return df

def print_all(json_file, print_files, start_name):
    #iterate through all entries in json file
    i = 0
    if(start_name != ""):
        seen = False
    df = read_dir_json(json_file)
    #iterate through dataframe
    for entry in df.itertuples():
        to_print = print_files[i]
        i = (i+1)%len(print_files)
        
        if is_uni(entry.uni) and (entry.title == "Student, COLUMBIA COLLEGE" or
                                    entry.title == "Student, FU FOUNDATN SCHL OF ENGINEERING & APPLIED SCIENCE:UGRAD"):
            text = "Hi " + entry.name + "\n\n"
            text += "Good luck on your " + entry.department + " finals!\n\n"
            text += "----------------------------------------\n\n"
            text += to_print 
            with open("temp.txt", "w") as f:
                f.write(text)
            if seen:
                print_file("temp.txt", entry["uni"])
            if entry.name == start_name:
                seen = True
        
    return
   

#main function here
if __name__ == "__main__":
    #take in args from command line
    parser = argparse.ArgumentParser(description='Send jobs to printer.')
    parser.add_argument('--startname', "-name", type=str, default="", help='if restarting program, enter name of last person printed')
    parser.add_argument("--files", "-f", type=str, nargs="+", default=["job1.txt", "job2.txt"], help="list of files to print")
    parser.add_argument("--datafile", type=str, default="scraper/data2.json", help="json file to read from")

    args = parser.parse_args()

    print_files = []

    #read filenames into strings
    for file in args.files:
        with open(file, "r") as f:
            text = f.read()
            print_files.append(text)

    #read json into dictionary
    with open(args.datafile, "r") as f:
        json_file = json.load(f)

    print_all(json_file, print_files, args.startname)

