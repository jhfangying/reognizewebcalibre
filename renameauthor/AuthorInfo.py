# -*- coding: utf-8 -*-
import re
from DB import DB
class AuthorInfo:
    db=None
    def __init__(self):
        self.db=DB()
    def where(self,wherestr=''):
        if(wherestr==''):
            return ''
        return " where "+wherestr
    def sql(self,table,where):
        return "select * from "+table+self.where(where)

    def author(self,id):
        sql=self.sql('authors',"id="+str(id))
        row=self.db.first(sql)
        author=self.rowToAuthor(row)
        author['book']=self.getBooksIdByAuthorId(id)
        return author
    
    def getAll(self):
        sql=self.sql('authors',"")
        rows=self.db.rows(sql)
        authors=[]
        for row in rows:
            authors.append(self.rowToAuthor(row))
        newauthors=[]
        for author in authors:
            author["book"]=self.getBooksIdByAuthorId(author["id"])
            newauthors.append(author)
        return newauthors
    
    def rowToAuthor(self,row):
        author={"id":row[0],"name":row[1]}
        return author
    # def invalidMultiNameAuthors(self):
    #     authors=self.getAuthors()
    #     newauthors=[]
    #     for author in authors:
    #         if(self.authorWithComma(author['name'])!=None):
    #             newauthors.append(author)
    #     return newauthors
    # def invalidMultiNameAuthorsWithBooksId(self):
    #     authors=self.invalidMultiNameAuthors()
    #     authorsWithBooksId=[]
    #     for author in authors:
    #         newauthor=author
    #         newauthor["books"]=self.getBooksIdByAuthorId(author['id'])
    #         authorsWithBooksId.append(newauthor)
    #     return authorsWithBooksId
    
    # def authorWithComma(self,authorname):
    #     if(re.search(r'.*?(,).*?',authorname)!=None):
    #         return authorname
    #     return None
    
    def getBooksIdByAuthorId(self,authorid):
        # print(authorid)
        sql=self.sql('books_authors_link',"author="+str(authorid))
        rows=self.db.rows(sql)
        # print(rows)
        booksId=[]
        if(len(rows)<=0):
            return None
        for row in rows:
            booksId.append(row[1])
        return booksId
authorInfo=AuthorInfo()
# print(authorInfo.author(6))
    # def formatedName(name)