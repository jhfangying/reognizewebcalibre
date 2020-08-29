# -*- coding: utf-8 -*-
import sqlite3
import requests
#删除标题相同的图书
conn = sqlite3.connect('metadata.db')
c=conn.cursor()

def duplicateRemoval(list):
    newlist=[]
    for i in list:
        if i not in newlist:
            newlist.append(i)
    return newlist

cursor = c.execute("SELECT * from books")
oldtable={}
def getDeleteUrls():
    for r in cursor:
        item={"id":r[0],"title":r[1]}
        oldtable[r[0]]=item
    count=0
    dereplication=[]
    titles=[]
    for key in oldtable:
        for k in oldtable:
            if(oldtable[key]['title']==oldtable[k]['title']):
                count=count+1
                if(count>1):
                    titles.append(oldtable[key]['title'])
        count=0
    titles=duplicateRemoval(titles)
    deleteRows=[]
    for title in titles:
        duplicateRows=c.execute('SELECT * from books where title="'+title+'";')
        for row in duplicateRows:
            id=row[0]
            title=row[1]
            hasCover=row[12]
            if(hasCover==1):
                continue
            else:
                deleteRows.append({'id':id,'title':title,'has_cover':hasCover})
                break
    urls=[]
    for row in deleteRows:
        urls.append('http://123.156.191.131:8083/delete/'+str(row['id'])+'/')
    return urls

username='admin'
password='admin123'
loginposturl='http://123.156.191.131:8083/login'
postdata={'next':'/','username':'admin','password':'admin123','remember_me':'on','sumbit':''}
session= requests.Session()
session.post(loginposturl,postdata)
urls=getDeleteUrls()
for url in urls:
    response=session.get(url)
    print(response.text)
