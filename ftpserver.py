from socket import *
import sys
import os
from threading import Thread

address = ('0.0.0.0',8888)

def doRequest(client):
    pass

class ftpserver(object):
    pass

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