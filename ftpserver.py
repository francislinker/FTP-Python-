from socket import *
import sys
import os
from threading import Thread
import time

address = ('0.0.0.0',8888)
filedir = '/home/tarena/project/download/'

def doRequest(client):
    #创建对象，每个客户端都有一个单独的对象来处理功能
    serverobj = ftpserver(client)
    #接收客户端的请求
    while True:
        message = client.recv(1024).decode()
        msglist = message.split(' ')
        if msglist[0] == 'L':
            serverobj.dolist()
        if msglist[0] == 'G':
            serverobj.doget(msglist[-1])
        if msglist[0] == 'P':
            serverobj.doput(msglist[-1])
        elif msglist[0] == 'Q':
            serverobj.doexit()

class ftpserver(object):
    def __init__(self,client):
        self.client = client

    def dolist(self):
        
        filelist = os.listdir(filedir)
        if not filelist:
            self.client.send('文件库为空'.encode())
            
            time.sleep(0.1)
        else:
            self.client.send(b'OK')
            #发送文件名到客户端
            for file in filelist:
                #判断是否为普通文件
                if os.path.isfile(filedir+file) and file[0] != '.':
                    self.client.send(file.encode())
                    time.sleep(0.1)

            self.client.send(b'##')
            time.sleep(0.1)

    def doget(self,filename):
        try:
            f = open(filedir+filename,'rb')
        except:
            self.client.send('文件不存在'.encode())
            return
        
        #文件已正常打开
        self.client.send(b'OK')
        time.sleep(0.1)
        #发送文件的内容
        while True:
            data = f.read(1024)
            if not data:
                self.client.send(b'##')
                time.sleep(0.1)
                break
            self.client.send(data)
            #发送完毕后关闭文件
            f.close()

    def doput(self,filename):
        try:
            f = open(filedir+filename,'wb')
        except:
            self.client.send('上传失败'.encode())
            return
        self.client.send(b'OK')
        while True:
            data = self.client.recv(1024)
            if data == b'##':
                break
            f.write(data)
        f.close()

    def doexit(self):
        sys.exit(0)

def main():
    server = socket(AF_INET,SOCK_STREAM)
    server.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    server.bind(address)
    server.listen(10)
    print('正在等待客户端连接......')

    while True:
        try:
            client,addr = server.accept()
            print('客户端已连接：',addr)
        except KeyboardInterrupt:
            sys.exit("服务器已经断开！")
        except Exception as e:
            print(e)
            continue
        t = Thread(target=doRequest,args=(client,))
        t.setDaemon(True)
        t.start()
        
if __name__ == "__main__" :
    main()