'''
Python编写一个文件读写程序（命令行程序），程序运行时读取record.log文件里面的信息并显示出来，同时还能接收用户的输入并将用户输入的信息写入到record.log的文件中（以追加方式写入，且用户可以反复输入信息，直到用户输入exit或者quit退出程序），写入格式如下：

你好啊！ --- 2015-06-1111:30:58
hello！who are you? --- 2015-06-11 11:32:29

注意：文件操作很容易发生异常，该捕获到的异常信息尽量捕获并处理
'''
import time
ISOTIMEFORMAT='%Y-%m-%d %X'
while True:
    line = input('请输入退出请输入exit：')
    if line == 'exit':break
    try:
        with open('record.log','a') as f:
            now = time.strftime( ISOTIMEFORMAT, time.localtime() )
            f.write('%s  --- %s \n' % (line,now))
    except IOError as err:
        print("File error: %s" % str(err))
