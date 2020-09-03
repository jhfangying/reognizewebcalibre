# -*- coding: utf-8 -*-
#有部分需要手动处理，比如有些时候用逗号分割phd 之类头衔 会被分成2个人
import requests
import re
from AuthorInfo import AuthorInfo
from BookMeta import BookMeta
from requests_toolbelt.multipart.encoder import MultipartEncoder
class RenameAuthor:
    baseUrl='http://123.156.191.131:8083'
    session=None
    def __init__(self):
        self.login()
    def login(self):
        loginPostUrl=self.baseUrl+'/login'
        postData={'next':'/','username':'admin','password':'admin123','remember_me':'on','sumbit':''}
        self.session= requests.Session()
        self.session.post(loginPostUrl,postData)
    books=[]
    def updateBooks(self):
        print("开始更新书籍信息")
        authors=self.invalidNameAuthors()
        for author in authors:
            self.invalidAuthorBooks(author)
        for bookid in self.books:
            self.updateBook(bookid)
        # print(self.books)
        print("更新书籍信息完成")
    def invalidAuthorBooks(self,author):
        for book in author["book"]:
            if book not in self.books:
                self.books.append(book)
    def updateBook(self,bookid):
        bookmeta=BookMeta()
        book=bookmeta.getBook(bookid)
        # content=bookmeta.bookToStr(book)
        # self.log(book['author'])
        book['author']=self.formatAuthorName(book['author'])
        # formattedName=self.formatAuthorName(book['author'])+"\n"
        
        # print(formattedName)
        multipartdata=self.bookToMultipartData(book)
        url=self.baseUrl+"/admin/book/"+str(bookid)
        self.log(book['author']+"\n"+self.baseUrl+"/book/"+str(bookid)+"\n")
        self.session.post(url,data=multipartdata,headers={'Content-Type': multipartdata.content_type})
        print("｜ID:"+str(bookid)+"《"+book["title"]+"》 完成")
    def invalidNameAuthors(self):
        authorInfo=AuthorInfo()
        authors=authorInfo.getAll()
        invalidAuthors=[]
        for author in authors:
            formattedName=self.formatAuthorName(author["name"])
            if(formattedName!=author["name"]):
                author["formattedname"]=formattedName
                invalidAuthors.append(author)
        return invalidAuthors
    
    def authorWithComma(self,authorName):
        authorName=authorName.replace('，',",")
        if(re.search(r'.*?(,).*?',authorName)!=None):
            return authorName
        return None

    def formatSingleAuthorName(self,orignalAuthorName):
        authorName=orignalAuthorName.strip(" ")
        authorName=authorName.replace('【',"[").replace('】',"]")
        authorName=authorName.replace('（',"(").replace('）',")")

        # authorName=authorName.replace('(',"[",1).replace(')',"]",1)
        # authorName=authorName.replace('（',"[",1).replace('）',"]",1)
        # authorName=authorName.replace('【',"[",1).replace('】',"]",1)
        # authorName=authorName.replace('（',"(").replace('）',")")
        # authorName=authorName.replace('【',"[").replace('】',"]")
        while True:
            str=authorName
            authorName=authorName.replace(' [',"[").replace('] ',"]")
            authorName=authorName.replace(' (',"(").replace(') ',")")
            if(str==authorName):
                break
        authorName=re.sub(r'^\((.*?)\)',"[\g<1>]",authorName)
        # authorName=re.sub(r'^\')
        # authorName=authorName.replace(']&',"] &").replace('&[',"& [")
        # authorName=authorName.replace(')&',") &").replace('&(',"& (")
        return authorName
    
    def formatAuthorName(self,orignalAuthorName):
        formattedAuthorName=''
        orignalAuthorName=orignalAuthorName.replace('，',' & ');
        orignalAuthorName=orignalAuthorName.replace(',',' & ');
        # authorNameWithComma=self.authorWithComma(orignalAuthorName)
        nameArr=orignalAuthorName.split('&')
        if(len(nameArr)>0):
            for i,name in enumerate(nameArr):
                nameArr[i]=self.formatSingleAuthorName(nameArr[i])
            formattedAuthorName=' & '.join(nameArr)
        else:
            formattedAuthorName=self.formatSingleAuthorName(orignalAuthorName)
        return formattedAuthorName

    
    def bookToMultipartData(self,book):
        multipartdata=MultipartEncoder(
            fields={
                'book_title':book['title'],
                'author_name':book['author'],
                'description':book['comments'],
                'tags':book['tags'],
                'series':book['series'],
                'series_index':book['series_index'],
                'rating':book['rating'],
                'cover_url':'',#book['author'],
                'btn-upload-cover':"",#book['author'],
                'pubdate':book['pubdate'],
                'publisher':book['publisher'],
                'languages':book['languages'],
                'btn-upload-format':"",
                'detail_view':'on'
            }
        )
        return multipartdata
    def log(self,content):
        filepath='temp.txt'
        with open(filepath,'a') as fo:
            fo.write(content)
        fo.close()
    # def updateBooks(self):
    #     authors=

# goAuthorBooks(['/author/new/273','(日)东野圭吾'])
# print(getBookId('/book/4005'))
renameAuthor=RenameAuthor()
# print(renameAuthor.formatAuthorName('(德)于尔根·奈佛(Jurgen Neffe)'))
# print(renameAuthor.formatAuthorName('桑德 (Warren Sande) & 桑德 (Carter Sande)'))
# print(renameAuthor.formatAuthorName('J.K.罗琳 (J.K.Rowling)'))
# print(renameAuthor.formatAuthorName('(台湾)三毛'))
# print(renameAuthor.formatAuthorName('[美] 大卫·哈伯斯塔姆'))
# print(renameAuthor.formatAuthorName('[美] 乔治·R. R. 马丁,George R.R. Martin'))
# print(renameAuthor.formatAuthorName('[明] 罗贯中 著,[清] 毛宗岗 评点'))

# author={"id":941,"name":"(德)于尔根·奈佛(Jurgen Neffe)","book":[6159],"formattedname":"[德]于尔根·奈佛(Jurgen Neffe)"}
# renameAuthor.updateBookByAuthor(author)
# authors=renameAuthor.processAuthorNameWithComma()
# print(authors)