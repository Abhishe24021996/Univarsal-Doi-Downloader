# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 14:59:10 2019

@author: Abhis
"""

#creating a database while will contain all doi's that has been done or failed
import sqlite3
connection = sqlite3.connect('doi_data.db')

def create_table():
    cursor = connection.cursor()
    # This is the only place where int vs INTEGER matters—in auto-incrementing columns
    create_table = "CREATE TABLE IF NOT EXISTS doi_status (sno INTEGER PRIMARY KEY AUTOINCREMENT, doi_id NVARCHAR(150) NOT NULL UNIQUE, success INT, fail INT, comment NVARCHAR(45))"
    cursor.execute(create_table)
    connection.commit()
    print("table_created")
    
def insert_doi_status(doi,success,fail,comment):
    cursor = connection.cursor()
    insert_table = '''INSERT INTO doi_status (doi_id, success, fail, comment) VALUES(?,?,?,?);'''
    cursor.execute(insert_table,(doi,success,fail,comment))
    connection.commit()
    print("Doi entered in data.db(LOCAL)(doi_status table)")
    
def check_db_list():
    cursor = connection.cursor()
    doi_list = "Select doi_id from doi_status"
    cursor.execute(doi_list)
    li=[row[0] for row in cursor.fetchall()]
    return li

    