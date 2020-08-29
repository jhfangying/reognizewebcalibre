## dereplication
去掉calibre中同名的书
### 使用方法：


## combine
合并一个库中的书到另外一个库

### 使用方法：

目标库下载放在combine目录下并改名为metadata_dest.db
源库和书籍目录下载，并直接存放到source目录下即可
设置好需要上传的目标calibre-web地址，然后运行 uploadbook.py程序就能自动把源库中有的，但是目标库中没有的书和书的元数据同步