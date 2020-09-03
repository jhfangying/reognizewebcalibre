# -*- coding: utf-8 -*-
# import sqlite3
import re
from DB import DB
import datetime
class BookMeta:
    db=None
    def __init__(self):
        self.db=DB()
    def where(self,wherestr=''):
        if(wherestr==''):
            return ''
        return " where "+wherestr
    def sql(self,table,where):
        return "select * from "+table+self.where(where)
    def getBook(self,id):
        sql=self.sql('books',"id="+str(id))
        bookrow=self.db.first(sql)
        authors=self.getAuthors(id)
        comments=self.getComments(id)
        tags=self.getTags(id)
        series=self.getBookSeries(id)
        ratings=self.getBookRatings(id)
        pubdate=''
        publisher=self.getBookPublisher(id)
        if(bookrow[4]!='0101-01-01 00:00:00+00:00'):
            pubdate=datetime.datetime.strptime(bookrow[4],'%Y-%m-%d %H:%M:%S')
            pubdate=datetime.datetime.strftime(pubdate, '%Y-%m-%d')
        book={'id':id,
        'title':bookrow[1],
        # 'path':bookrow[9],
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
    def getAll(self):
        sql=self.sql('books',"")
        print(sql)
        rows=self.db.rows(sql)
        books=[]
        if(len(rows)==0):
            return None
        for row in rows:
            books.append(self.getBook(row[0]))
        return books
    def bookToStr(self,book):
        bookstr="《"+book["title"]+"》\n作者："+book["author"]+"\n 描述："+book["comments"]+"\n 标签："+book["tags"]+"\n评分:"+book["rating"]+"\n"
        return bookstr
    def getAuthors(self,bookid):
        sql=self.sql('books_authors_link',"book="+str(bookid))
        authorsLink=self.db.rows(sql)
        authors='';
        for link in authorsLink:
            author=self.getAuthor(link[2])
            separator='' if authors=='' else ' & '
            authors=authors+separator+author
        return authors

    def getAuthor(self,authorid):
        sql=self.sql('authors',"id="+str(authorid))
        authorRow=self.db.first(sql)
        author=authorRow[1]
        return author

    def getTags(self,bookid):
        sql=self.sql('books_tags_link',"book="+str(bookid))
        links=self.db.rows(sql)
        # print(links)
        if(len(links)==0):
            return ''
        tags='';
        for link in links:
            tag=self.getTag(link[2])
            # print(tag)
            separator='' if tags=='' else ','
            tags=tags+separator+tag
        return tags

    def getTag(self,tagid):
        sql=self.sql('tags',"id="+str(tagid))
        item=self.db.first(sql)
        # print(item)
        if(item==None):
            return ''
        return item[1]

    def getBookSeries(self,bookid):
        sql=self.sql('books_series_link',"book="+str(bookid))
        links=self.db.first(sql)
        if(links==None):
            return ''
        seriesid=links[2]
        return self.getSeries(seriesid)
    def getSeries(self,seriesid):
        sql=self.sql('series',"id="+str(seriesid))
        item=self.db.first(sql)
        return item[1]

    def getBookRatings(self,bookid):
        sql=self.sql('books_ratings_link',"book="+str(bookid))
        links=self.db.first(sql)
        if(links==None):
            return ''
        seriesid=links[2]
        return self.getRating(seriesid)

    def getRating(self,ratingid):
        sql=self.sql('ratings',"id="+str(ratingid))
        item=self.db.first(sql)
        item=int(item[1]/2)
        return item

    def getComments(self,bookid):
        sql=self.sql('comments',"book="+str(bookid))
        item=self.db.first(sql)
        # print(item)
        if(item==None):
            return ''
        return item[2]
    def getBookPublisher(self,bookid):
        sql=self.sql('books_publishers_link',"book="+str(bookid))
        links=self.db.first(sql)
        if(links==None):
            return ''
        publisherid=links[2]
        return self.getPublisher(publisherid)
    def getPublisher(self,publisherid):
        sql=self.sql('publishers',"id="+str(publisherid))
        item=self.db.first(sql)
        return item[1]
    # def getRows(self,sql):
    #     result=self.cursor.execute(sql)
    #     rows=result.fetchall()
    #     return rows
    
    # def getBookInfo(self,id):

# bookMeta=BookMeta()
# print(bookMeta.getBook(2674));