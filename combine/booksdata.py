# -*- coding: utf-8 -*-
import sqlite3
# import requests
import os
import datetime
#合并2个图书库
#先找出dest库中没有的书
path=os.getcwd()
# print('当前路径：'+path)
destConn = sqlite3.connect('metadata_dest.db')
destCursor=destConn.cursor()
sourceConn=sqlite3.connect(path+'/source/metadata.db')
sourceCursor=sourceConn.cursor()
def getSourceDataById(table,id):
    sql='SELECT * from '+table+' where id='+str(id)
    cursor=sourceConn.execute(sql)
    rows=cursor.fetchall()
    if(len(rows)==0):
        return None
    return  rows[0]

def getSourceDataLinkByBookId(table,bookid):
    linkCursor=sourceConn.execute('SELECT * from '+table+' where book='+str(bookid))
    links=linkCursor.fetchall()
    if(len(links)==0):
        return None
    return links

def getDiffBooksId():
    sourceData= sourceConn.execute('SELECT * from books')
    booksid=[]
    for row in sourceData:
        destRow=destCursor.execute('select count(0) from books where title="'+str(row[1])+'";')
        rows=destRow.fetchall();
        count=rows[0][0]
        if(count==0):
            booksid.append(row[0])
    return booksid
def getDiffBooks():
    idlist=getDiffBooksId()
    books=[]
    for id in idlist:
        book=getBook(id)
        books.append(book)
    return books
def getBook(id):
    bookrow=getSourceDataById('books',id)
    authors=getAuthors(id)
    comments=getComments(id)
    tags=getTags(id)
    series=getBookSeries(id)
    ratings=getBookRatings(id)
    pubdate=''
    publisher=getBookPublisher(id)
    if(bookrow[4]!='0101-01-01 00:00:00+00:00'):
        pubdate=datetime.datetime.strptime(bookrow[4],'%Y-%m-%d %H:%M:%S')
        # print(pubdate)
        pubdate=datetime.datetime.strftime(pubdate, '%Y-%m-%d')
    book={'id':id,
    'title':bookrow[1],
    'path':bookrow[9],
    'author':authors,
    'comments':comments,
    'tags':tags,
    'series':series,
    'series_index':str(bookrow[5]),
    'rating':str(ratings),
    'pubdate':pubdate,
    'publisher':publisher,
    'languages':'中文'}
    return book
def getAuthors(bookid):
    authorsLink=getSourceDataLinkByBookId('books_authors_link',bookid)
    authors='';
    for link in authorsLink:
        author=getAuthor(link[2])
        separator='' if authors=='' else ' & '
        authors=authors+separator+author
    return authors
def getAuthor(authorid):
    authorRow=getSourceDataById('authors',authorid)
    author=authorRow[1]
    return author

def getTags(bookid):
    links=getSourceDataLinkByBookId('books_tags_link',bookid)
    if(links==None):
        return ''
    tags='';
    for link in links:
        tag=getTag(link[2])
        separator='' if tags=='' else ','
        tags=tags+separator+tag
    return tags

def getTag(tagid):
    item=getSourceDataById('tags',tagid)
    if(item==None):
        return ''
    return item[1]

def getBookSeries(bookid):
    links=getSourceDataLinkByBookId('books_series_link',bookid)
    if(links==None):
        return ''
    seriesid=links[0][2]
    return getSeries(seriesid)
def getSeries(seriesid):
    item=getSourceDataById('series',seriesid)
    return item[1]

def getBookRatings(bookid):
    links=getSourceDataLinkByBookId('books_ratings_link',bookid)
    if(links==None):
        return ''
    seriesid=links[0][2]
    return getRating(seriesid)

def getRating(ratingid):
    item=getSourceDataById('ratings',ratingid)
    item=int(item[1]/2)
    return item

def getComments(bookid):
    item=getSourceDataById('comments',bookid)
    if(item==None):
        return ''
    return item[2]
def getBookPublisher(bookid):
    links=getSourceDataLinkByBookId('books_publishers_link',bookid)
    if(links==None):
        return ''
    publisherid=links[0][2]
    return getPublisher(publisherid)
def getPublisher(publisherid):
    item=getSourceDataById('publishers',publisherid)
    return item[1]