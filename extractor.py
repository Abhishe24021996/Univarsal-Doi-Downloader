# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 15:04:03 2019

@author: Abhis
"""
import subprocess
from tools import text_cleaner
# from tools import regsub_clean
# from tools import lemm
# from tools import spac
# from tools import rem_af_spac
import subprocess
from lxml import html
import re


def external_command(cmd):
    process = subprocess.Popen(cmd.split(' '),
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    # wait for the process to terminate
    out, err = process.communicate()
    errcode = process.returncode
    return errcode, out, err

def cermine_process(directory):
    command='java -cp cermine-impl-1.13-jar-with-dependencies.jar pl.edu.icm.cermine.ContentExtractor -path '+ directory
    external_command(command)


def extraction(directory):
    #filenames=glob.glob("file/*.cermxml")
    cerm = directory+".cermxml"
    #cerm = filename.replace(".pdf",".cermxml")
    regexpNS="http://exslt.org/regular-expressions"
    f =open(directory+'/'+cerm,'r',encoding="utf8")
    page = f.read()
    tree = html.fromstring(page)
    f.close()
    try: 
        abst = list(map(str,tree.xpath('//abstract/p/text()')))
        abst = ' '.join(abst).strip()
    except: abst = ''
    try: 
        titl = list(map(str,tree.xpath('//title-group/article-title/text()')))
        titl = ' :::: '.join(titl)
    except: titl='' 
    try: 
        auth = list(map(str,tree.xpath('//contrib-group/contrib[@contrib-type="author"]/string-name/text()')))
        auth=' :::: '.join(auth)
    except: auth =''
    try: 
        affl = list(map(str,tree.xpath('//aff/institution/text()')))
        affl = ' :::: '.join(affl)
    except: affl=''
    mate=''
    try:
       try: mate1=list(map(str,tree.xpath('//sec[re:test(title,"m\s?e\s?t\s?h\s?o\s?d\s?s?\s?|m\s?a\s?t\s?e\s?r\s?i\s?a?\s?l?\s?s?\s?","i")]/p/text()',namespaces={'re':regexpNS})))
       except: mate1=[] 
       
       try: mate2=list(map(str,tree.xpath('//sec[re:test(title,"m\s?e\s?t\s?h\s?o\s?d\s?s?\s?|m\s?a\s?t\s?e\s?r\s?i\s?a?\s?l?\s?s?\s?","i")]/sec/p/text()',namespaces={'re':regexpNS})))
       except: mate2=[]
       if len(mate1)>len(mate2):
           mate=' '.join(mate1).strip()
       else: mate=' '.join(mate2).strip()
       
       if len(mate)==0:
           mate =re.findall('<p>(m\s?e\s?t\s?h\s?o\s?d\s?s?\s?(.+\n)+|m\s?a\s?t\s?e\s?r\s?i\s?a\s?l\s?s?\s?(.+\n)+).+<sec id.+>',page,re.I)[0]
           mate = ' '.join(mate).strip()
    except: mate=''
    
# =============================================================================
#     title.append(titl)
#     author.append(auth)
#     affliation.append(affl)
#     material.append(mate)
# =============================================================================
    #names.append(doi)
    #df = df.append({'DOI':doi, 'title':titl, 'affliation':affl, 'author':auth, 'material': mate},ignore_index=True)
    #shutil.rmtree(directory)
    return mate, titl, affl, auth, abst


def processing_text(directory):
    mate, titl, affl, auth, abst = extraction(directory)
    mate = text_cleaner.__run__(mate)
    # lisli = tokenise(mate)
    # regword = regsub_clean(lisli)
    # lisli=lemm(regword)
    # regword = spac(lisli)
    # materi = rem_af_spac(regword)
    print('text processing compleated, ready to be inserted in Smart Sales app RA')
    print('mate:   ',mate)
    return titl, auth, abst, materi, affl, mate


    
    
