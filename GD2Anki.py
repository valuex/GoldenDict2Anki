# -*- coding: utf-8 -*-
"""
updated on Sun Augst 19th 20:00:15 2023
1. support multiple user dicts
2. support user to set deck 
3. can load seperate CSS into line, so that it shows good in Anki.

Created on Mon Oct 28 00:00:15 2019

@author: valuex
"""

import json
import urllib.request
import re
from mdict_query import IndexBuilder
import configparser
import os
import css_inline
from lxml import html, etree
import sys,io
import bs4   #BeautifulSoup 
import tkinter.messagebox
import copy
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')


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

def NoteContent(dic_deck,FrontStr, BackStr):    
    BackStr=BackStr.replace('"','\\"')
    BackStr=BackStr.replace(u'\xa0',u' ')
    BackStr = re.sub(r'<img.*?>', '', BackStr)
#    BackStr=BackStr.replace('</span>','</span><br>')
    newnote="""
    {    
        "deckName": "%s",
        "modelName": "%s",
        "fields": {
            "%s": "%s",
            "%s": "%s"
        },
        "options": {
            "allowDuplicate": false
        },
        "tags": ["GoldenDict"]
    }
    """ % (dic_deck["dname"],dic_deck["mname"],dic_deck["cfname"],FrontStr,dic_deck["cbname"],BackStr)

    return newnote

def consolidate_CSS_into_HTML(strHtml):
    soup = bs4.BeautifulSoup(strHtml,features="lxml")
    stylesheets = soup.findAll("link", {"rel": "stylesheet"})
    for s in stylesheets:
        t = soup.new_tag('style')
        if(os.path.isfile(s["href"])):
            c = bs4.element.NavigableString(open(s["href"]).read())
            t.insert(0,c)
            t['type'] = 'text/css'
            s.replaceWith(t)
        else:
            print("css file" + s["href"] + "not found")
            continue
    return str(soup)

def merge_html(origin_doc, new_doc):
    soup_orgin_doc = get_soup(origin_doc)
    soup_newdoc = get_soup(new_doc)
    b = soup_orgin_doc.new_tag('hr')
    # b.append('----')
    soup_orgin_doc.body.append(b)
    for element in soup_newdoc.body:
        soup_orgin_doc.body.append(copy.copy(element))
    return str(soup_orgin_doc)
def get_soup(strInput):
    b_soup = bs4.BeautifulSoup(strInput,features="lxml")
    try:
        b_soup_body=b_soup.body
    except:        
        html_content=str_to_html(strInput)
        b_soup = bs4.BeautifulSoup(html_content,features="lxml")
    return b_soup

def str_to_html(strInput):
    html_body=""
    list_txt=strInput.splitlines()
    for line in list_txt:
        body_line="<p>" + line + "</p>\n"
        html_body=html_body + body_line
    html_prefix="<html><head></head><body>"
    html_sufix="</body></html>"
    html_doc=html_prefix+html_body+html_sufix
    return html_doc

if __name__ == '__main__':
    All_Meanings=""
    config = configparser.ConfigParser()
    # get absolute path
    fp_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    iniFile = os.path.join(fp_dir, "Config.ini")
    if(not os.path.isfile(iniFile)):
        tkinter.messagebox.showerror(title="Error", message="No ini file found")
        exit()
    config.read(iniFile, encoding='utf-8')
    mdict_files=config['Dicts']
    for dict_file in mdict_files:
        mdict=mdict_files[dict_file] 
        # https://note.nkmk.me/en/python-os-basename-dirname-split-splitext/#get-the-extension-without-dot-period
        ext_without_dot = os.path.splitext(mdict)[1][1:]
        if(ext_without_dot!="mdx"):
            tkinter.messagebox.showerror(title="Ini setting Error", message="Dict file is not mdx")
            exit()
        mdict_short_name= os.path.splitext(os.path.basename(mdict))[0]
        builder = IndexBuilder(mdict)
        # Word="count"
        Word=sys.argv[1]
        Meanings_In_This_Dict=builder.mdx_lookup(Word, ignorecase = True)
        # str_content = Meanings.decode('utf-8')
        Meanings='\n' . join(Meanings_In_This_Dict)
        Meanings="<H1>"+mdict_short_name+"</H1>"+Meanings
        Meanings_with_CSS=consolidate_CSS_into_HTML(Meanings)
        Meanings_with_CSS_inlined = css_inline.inline(Meanings_with_CSS)
        if (All_Meanings==""):
            All_Meanings=Meanings_with_CSS_inlined
        else:
            All_Meanings=merge_html(All_Meanings, Meanings_with_CSS_inlined)

    # fp = open("2.html","w", encoding='utf-8')
    # fp.write(All_Meanings)
    # for item in Meanings:
    #     fp.write(item)
    # fp.write("</html>\n")
    # fp.close()
    try:
        deck_name=config['Deck']['DeckName']
        modle_name=config['Deck']['ModelName']
        card_front_name=config['Deck']['CardFrontName']
        card_back_name=config['Deck']['CardBackName']
    except:
        tkinter.messagebox.showerror(title="Ini setting Error", message="Missing Deck/Model/CardFront/CardBack setting")
        exit()
    user_card_template={"dname":deck_name,"mname":modle_name,"cfname":card_front_name,"cbname":card_back_name}
    CardNote=NoteContent(user_card_template,Word, All_Meanings)
    newnote=json.loads(CardNote,strict=False)

    try:
        result = invoke('addNote',note=newnote)
        print(result)
    except:
        AlertWhenFails=config['Config']['AlertWhenFails']
        if(AlertWhenFails):
            tkinter.messagebox.showerror(title="Oops", message="Something went wrong...")
            exit()
    
    
