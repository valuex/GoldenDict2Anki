# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 20:24:57 2021

@author: wei_x
"""


import urllib.request
from socket import timeout
import json
import psutil  
import os 
from pathlib import Path
import configparser
from tkinter import filedialog
from tkinter import Tk

config = configparser.ConfigParser()
fp_dir = os.path.dirname(os.path.realpath(__file__))
iniFile = os.path.join(fp_dir, "Config.ini")
def check_url( url, timeout1=5 ):
    try:
        if(urllib.request.urlopen(url,timeout=timeout1).getcode() == 200):
            return 1
    except urllib.error.URLError as e:
        return 2
    except timeout:
        return "Time out"

def process_running(prcsName):
    if(prcsName in (p.name() for p in psutil.process_iter())):
        return True
    else:
        return False
def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

def select_mdx_file():
    root = Tk()
    root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("mdx files","*.mdx"),("all files","*.*")))
    if(root.filename):                
        print (root.filename)
        mdxfilepath_win=root.filename.replace("/", "\\")
        config['Default'] = {}
        config['Default']['mdxfile'] = mdxfilepath_win    # update                        
        with open(iniFile, 'w',encoding='utf-8') as configfile:    # save
            config.write(configfile)
        root.withdraw()
        return mdxfilepath_win
    else:
        root.withdraw()
        return False
def check_mdxdb_file(mdx_file):
    mdxdb_file=Path(mdx_file+'.db')    
    if(mdxdb_file.is_file()):
        print('mdx.db file exists')
        if(mdxdb_file.stat().st_size>1):
            print('mdx.db file is effective')            
            return True
        else:
            os.rename(mdx_file+'.db', mdx_file+'.db.bk') # rename the zero size .db file as a backup
            run_mdx_server()
    else:
        run_mdx_server()
def check_config_mdx_db_3files():

#    print(iniFile)
    
    my_file = Path(iniFile)
    print("Config.ini exists")
    # file exists
    if my_file.is_file():        
        try:
            config.read(iniFile, encoding='utf-8')
            mdict=config['Default']['mdxfile']
            if(Path(mdict).is_file()):
                print('mdx file exists')
                check_mdxdb_file(mdict)
        except:
            print('can NOT find the mdx file specified in config.ini file')
            SelectedFile=select_mdx_file()
            if(SelectedFile):
                check_mdxdb_file(SelectedFile)
            else:
               print('user abort, no mdx file seleted') 

    else:
        print('Config.ini missed')
        SelectedFile=select_mdx_file()
        if(SelectedFile):
            check_mdxdb_file(SelectedFile)
        else:
           print('user abort, no mdx file seleted') 
    
def run_mdx_server():
    fp_dir = os.path.dirname(os.path.realpath(__file__))
    mdx_server= os.path.join(fp_dir, "mdx_server.exe") 
    if(Path(mdx_server).is_file()):
        print(mdx_server)
        os.startfile(mdx_server)
    else:
        print('can Not find mdx_server.exe')
def run_GD2Anki(EngWord):
    fp_dir = os.path.dirname(os.path.realpath(__file__))
    GD2Anki= os.path.join(fp_dir, "GD2Anki.exe")
    if(Path(GD2Anki).is_file()):
        GD2Anki= GD2Anki+' ' + EngWord
#        os.startfile(GD2Anki)
        print(GD2Anki)
        os.system(GD2Anki)
    else:
        print('can Not find GD2Anki.exe')
        print('  put GD2Anki_setting.exe and GD2Anki.exe under the same folder')

      
def check_model_name():
    results=invoke('modelNames')    
    if('NewWordsType' in results):
        print('NewWordsType is set correctly')
        check_model_field_name()
        return True
    else:
        creat_model()
        return False
def check_model_field_name():
    results=invoke('modelFieldNames',modelName='NewWordsType') 
    if(('Front' in results) and ('Back' in results)):
        print('Model field is  set correctly')
    else:
        print('manully update the fields name of the NewWordsType model as Front and Back')
        print('  1- Anki main window, click <Browse>')
        print('  2- <Browse> window, click <Notes> menu-->select <add Notes>')
        print('  3- <Add> window, click <Type> drop down combox-->select <NewWordsType>-->Click <choose> botton')
        print('  4- <Add> window, click <Fileds> botton-->Rename the filds names as Front and Back')
        # update_model_field_name()
def update_model_field_name():
    NewModel= {
            "name": "NewWordsType",
            "templates": {
                "My Card 1": {
                    "Front": "{{Front}}",
                    "Back": "{{Back}}"
                }
            }
        }
    results=invoke('updateModelTemplates',model=NewModel) 
    print(results)
    print('Model fields updated')
def creat_model():
    mname="NewWordsType"
    order=["Front", "Back"]
    css_style="Optional CSS with default to builtin css"
    cardTemp=[
            {
                "Name": "My Card 1",
                "Front": "{{Front}}",
                "Back": "{{Back}}"
            }
        ]
    
    result=invoke('createModel',modelName=mname,inOrderFields=order,css=css_style,cardTemplates=cardTemp)
    print(result)
    print('Model created')


if __name__ == '__main__':
    if(process_running('anki.exe')):
        print('anki runs')
    else:
        print('you should run anki first')
        os._exit(0)
    a=check_url('http://localhost:8765/')  # check ankiconnect
    if(a==1):
        print("AnkiConnect is sucessfully running")
    elif(a==2):
        print("AnkiConnect is NOT running or NOT installed")
        os._exit(0)
    else:
        print(a)
        os._exit(0)
  # check whether the NewWords deck exists  
    result = invoke('deckNames')
    if('NewWords' in result):
        print("deck--NewWords-- exists")
    else:
        invoke('createDeck', deck='NewWords')
        print("deck--NewWords-- created")
    
    
  # check whether the config.ini file exists  
    check_config_mdx_db_3files()

    check_model_name()
    run_GD2Anki("apple")