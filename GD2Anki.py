# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 00:00:15 2019

@author: valuex
"""

import json
import urllib.request
import re
import sys
from mdict_query import IndexBuilder
import configparser
import winsound         # for sound  
#import time             # for sleep
import os


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

def NoteContent(FrontStr, BackStr):    
    BackStr=BackStr.replace('"','\\"')
    BackStr=BackStr.replace(u'\xa0',u' ')
    BackStr = re.sub(r'<img.*?>', '', BackStr)
#    BackStr=BackStr.replace('</span>','</span><br>')
    newnote="""
    {    
        "deckName": "NewWords",
        "modelName": "NewWordsType",
        "fields": {
            "Front": "%s",
            "Back": "%s"
        },
        "options": {
            "allowDuplicate": false
        },
        "tags": [ ]
    }
    """ % (FrontStr,BackStr)

    return newnote

if __name__ == '__main__':
    config = configparser.ConfigParser()
    # get absolute path
    fp_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    iniFile = os.path.join(fp_dir, "Config.ini")
#    print(iniFile)
    config.read(iniFile, encoding='utf-8')
    mdict=config['Default']['mdxfile']
    builder = IndexBuilder(mdict)
#    Word="abandon"
    Word=sys.argv[1]
    Meanings=builder.mdx_lookup(Word, ignorecase = True)
    record = Meanings[0]

    CardNote=NoteContent(Word, record)
#    print(CardNote)
#    t3=time.time()
    newnote=json.loads(CardNote,strict=False)
#    print(newnote)
#    t4=time.time()
    try:
        result = invoke('addNote',note=newnote)
        print(result)
        winsound.Beep(440, 250) # frequency, duration
    except:
        winsound.Beep(600, 250)
    
    
#    w=WindowsBalloonTip("Note Added", result)