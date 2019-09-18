import sys
from scbooks import api_unpaywall
from db import create_table
from db import insert_doi_status
from db import check_db_list
from extractor import cermine_process
from extractor import processing_text
import mysql.connector
import glob
import shutil

from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')
host = config.get('main', 'host')
user = config.get('main', 'user')
password = config.get('main', 'password')
db = config.get('main', 'db')

###Inserting new row in RA
def insert_RA(doi,titl,auth,abst,materi,affl,mate):
    db = mysql.connector.connect(host=host,  # your host name is often 'localhost'
                     user=user,            
                     passwd=password,  
                     db=db,
                     autocommit=True)
    with db.cursor() as cur:
	    query = "INSERT INTO research_article(research_article_doi,research_article_title,research_article_authors,research_article_abstract,research_article_keywords,research_article_affliations,research_material_section) VALUES (%s,%s,%s,%s,%s,%s,%s);"
	    try: 
	        cur.execute(query,(doi,titl,auth,abst,materi,affl,mate))
	    except Exception as e:
	        print(e) 
    
        
        

####Read the input file contining the doi's in correct form:::i/p--van.txt
file_list_of_dois = sys.argv[0]
with open("van.txt","r") as f: 
	listi=f.read()
doi_list = listi.split()



#intiate
j=0
##a lacal db to check doi's status
create_table()
already_doi = check_db_list()
#check if it is available for download or not 
for doi in doi_list:
    if doi in already_doi:
        print("already cheacked(LOCAL)")
        continue
    #check if doi not in db
    flag = api_unpaywall(doi,j)
    if flag == 0: 
        print("downloads not found in any API")
        insert_doi_status(doi,success=0,fail=1,comment="not found anywhere")
        continue
    elif flag == 1:
        print("Finally started")
        directory = 'pyf'+str(j)
        j+=1
        if glob.glob(directory+'/'+directory+'.pdf'):
            cermine_process(directory) #ADD CONDITION HEE IF DONE OR NOT THEN APPEND IT TO THE DATA BASE
            filename = directory + ".cermxml"
            if glob.glob(directory+'/'+filename):
                titl, auth, abst, materi, affl, mate = processing_text(directory)
                if materi:
                    insert_RA(doi, titl, auth, abst, materi, affl, mate)
                    insert_doi_status(doi,success=1,fail=0,comment="successful")
                    shutil.rmtree(directory)
                else:
                    print("no material keywords extracted")
                    shutil.rmtree(directory)
                    #append it with material not extracted
                    insert_doi_status(doi,success=0,fail=1,comment="no keywords found")
            else:
                print("cermine doesnot create cermxml file, not found") 
                shutil.rmtree(directory)
                #append in database
                insert_doi_status(doi,success=0,fail=1,comment="no cermxml file found")
        else:
            print("no download file was found")
            shutil.rmtree(directory)
            #append in local that no dwonload file was found
            insert_doi_status(doi,success=0,fail=1,comment="no download file was found")
        
        
