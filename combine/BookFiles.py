# -*- coding: utf-8 -*-
# import sqlite3
# import requests
import os
import booksdata 

class BookFiles:
    basepath=os.getcwd()+'/source/'
    def __init__(self,bookpath):
        self.bookpath=self.basepath+bookpath
        # print(self.bookpath)
    def getFiles(self):
        return os.listdir(self.bookpath)

    def getCoverPath(self):
        file=self.getBySuffix('jpg')
        if(file==None):
            file=self.getBySuffix('png')
        return file

    def getMobi(self):
        return self.getBySuffix('mobi')
    def getPDF(self):
        return self.getBySuffix('pdf')
    def getEPub(self):
        return self.getBySuffix('epub')

    def getBookFile(self):
        file=self.getEPub()
        if(file==None):
            file= self.getMobi()
        if(file==None):
            file=self.getPDF()
        return file
    #有多种格式的电子书
    def hasMultiType(self):
        typecount=0
        if(self.getMobi()!=None):
            typecount=typecount+1
        if(self.getEPub()!=None):
            typecount=typecount+1
        if(self.getPDF()!=None):
            typecount=typecount+1
        if(typecount>1):
            return True
        return False
        # if(self.getMobi()!=None and self.getEPub()!=None):
        #     return True
        # return False

    def getBySuffix(self,type):
        files=self.getFiles()
        for f in files:
            filename=f.lower()
            suffix=self.getSuffix(filename)
            if(suffix==type):
                return f
        return None
    def getSuffix(self,filename):
        arr=filename.split('.')
        return arr[len(arr)-1]

    def getFullPath(self,filename):
        return self.bookpath+'/'+filename

    def getMimeType(type):
        mimeTypes={
            'mobi':'application/octet-stream',
            'epub':'application/epub+zip',
            'jpg':'image/jpeg',
            'png':'image/png',
            'pdf':'application/pdf'
            }
        return mimeTypes[type]
        
# book=booksdata.getBook(337)
# print(book)
# bookfile= BookFiles(book['path'])
# f=bookfile.getMobi()
# print(bookfile.getFullPath(f))
# files=getCoverPath(book['path'])
# print(files)