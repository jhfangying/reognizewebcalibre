# -*- coding: utf-8 -*-
import sqlite3
class DB:
    conn=None
    cursor=None
    def __init__(self,path=''):
        if(path==''):
            path='metadata.db'
        self.conn=sqlite3.connect(path)
        self.cursor=self.conn.cursor()
    def rows(self,sql):
        result=self.cursor.execute(sql)
        rows=result.fetchall()
        return rows
    def first(self,sql):
        rows=self.rows(sql)
        if(len(rows)==0):
            return None
        return rows[0]
