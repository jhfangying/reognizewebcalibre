# -*- coding: utf-8 -*-
import requests
import random
import booksdata
import os
from BookFiles import BookFiles
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
baseUrl='http://123.156.191.131:8083'
def login():
    loginPostUrl=baseUrl+'/login'
    postData={'next':'/','username':'admin','password':'admin123','remember_me':'on','sumbit':''}
    session= requests.Session()
    session.post(loginPostUrl,postData)
    return session
def uploadFile(book):
    uploadFileUrl=baseUrl+'/upload'
    bookFile=BookFiles(book['path'])
    file=bookFile.getBookFile()
    filepath=bookFile.getFullPath(file)
    suffix=bookFile.getSuffix(file)
    mimetype=BookFiles.getMimeType(suffix)
    fileobj=open(filepath, 'rb')
    multipart_encoder = MultipartEncoder(
        fields={
            'btn-upload': (file,fileobj,mimetype)
        },
        boundary='-----------------------------' + str(random.randint(1e28, 1e29 - 1))
    )
    # fileobj.close()
    response=session.post(uploadFileUrl,data=multipart_encoder,headers={'Content-Type': multipart_encoder.content_type})
    responseJson=json.loads(response.text)
    updateBook(responseJson['location'],book)
    
def updateCoverData(book):
    bookFile=BookFiles(book['path'])
    coverFileName=bookFile.getCoverPath()
    coverPath=bookFile.getFullPath(coverFileName)
    suffix=bookFile.getSuffix(coverFileName)
    mimetype=BookFiles.getMimeType(suffix)
    cover=(coverFileName,open(coverPath, 'rb'),mimetype)
    multipartdata=updateData(book,cover=cover)
    return multipartdata

def updateOtherFormatData(book):
    bookFile=BookFiles(book['path'])
    otherFormatFileName=bookFile.getMobi()
    otherFormatPath=bookFile.getFullPath(otherFormatFileName)
    suffix=bookFile.getSuffix(otherFormatFileName)
    mimetype=BookFiles.getMimeType(suffix)
    otherFormat=(otherFormatFileName,open(otherFormatPath, 'rb'),mimetype)
    
    multipartdata=updateData(book,otherformat=otherFormat)
    return multipartdata

def updateData(book,cover='',otherformat=''):
    # print(otherformat)
    if(cover!=''):
        otherformat=''
    if(otherformat!=''):
        cover=''
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
            'btn-upload-cover':cover,#book['author'],
            'pubdate':book['pubdate'],
            'publisher':book['publisher'],
            'languages':book['languages'],
            'btn-upload-format':otherformat,#otherFormat,#book['author']
            'detail_view':'on'
            # 'btn-upload': (files[0],open(filepath, 'rb'),'application/epub+zip')
        },
        boundary='-----------------------------' + str(random.randint(1e28, 1e29 - 1))
    )
    return multipartdata
def updateBook(url,book):
    updateUrl=baseUrl+url
    # print(updateUrl)
    bookFile=BookFiles(book['path'])
    postData=None
    if(bookFile.hasMultiType() or bookFile.getCoverPath()!=None):
        coverFileName=bookFile.getCoverPath()
        if(coverFileName!=None):
            # print('update cover')
            postData=updateCoverData(book)
            response=session.post(updateUrl,data=postData,headers={'Content-Type': postData.content_type})
        if(bookFile.hasMultiType()==True):
            # print('update format')
            postData=updateOtherFormatData(book)
            # print(postData)
            response=session.post(updateUrl,data=postData,headers={'Content-Type': postData.content_type})
    else:
        postData={
                'book_title':book['title'],
                'author_name':book['author'],
                'description':book['comments'],
                'tags':book['tags'],
                'series':book['series'],
                'series_index':book['series_index'],
                'rating':book['rating'],
                'cover_url':'',#book['author'],
                'btn-upload-cover':'',#book['author'],
                'pubdate':book['pubdate'],
                'publisher':book['publisher'],
                'languages':book['languages'],
                'btn-upload-format':'',#book['author']
                'detail_view':'on'
            }
        response=session.post(updateUrl,data=postData)
    # header=None
    # if(isinstance(postData,dict)==False):
    #     header={'Content-Type': postData.content_type}
    # response=session.post(updateUrl,data=postData,headers=header)

books=booksdata.getDiffBooks()
# print(len(books))
session=login()
path=os.getcwd()
importfile=path+'/'+'importfilelist.txt'
with open(importfile,'w') as fo:
    fo.write('')
    fo.close()
with open(importfile,'a') as fo:   
    for book in books:
        print('开始上传'+book['title'])
        uploadFile(book)
        fo.write(book['title']+','+str(book['id']))
        fo.write('\r\n')
        print('更新完成')
print('全部更新完成')
fo.close()