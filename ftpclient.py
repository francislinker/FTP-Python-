from socket import *
import sys

class ftpclient(object):

    def   __init__(self,client):
        self.client = client

    def dolist(self):
        #向服务端发送请求，接收服务端消息
        self.client.send(b'L')
        data = self.client.recv(1024).decode()
        if data == 'OK':
            while True:
                filename = self.client.recv(1024).decode()
                if filename == '##':
                    break
                print('\033[32m'+filename+'\033[0m')
        else:
            print(data)

    def doget(self):
        filename = input('请输入要下载的文件名：')
        message = 'G ' + filename
        self.client.send(message.encode())
        data = self.client.recv(1024).decode()
        if data == 'OK':
            f = open(filename,'wb')
            while True:
                data = self.client.recv(1024)
                if data == b'##':
                    break
                f.write(data)
            f.close()
            print('%s 下载完成' % filename)
        else:
            print(data)
            

    def doput(self):
        filename = input('请输入要上传的文件：')
        filename2 = filename.split('/')[-1]
        try:
            f = open(filename,'rb')
        except:
            print('没有这个文件')
            return

        self.client.send(('P '+filename2).encode())
        data = self.client.recv(1024)
        if data == b'OK':
            while True:
                data = f.read(1024)
                if not data:
                    import time
                    time.sleep(0.1)
                    self.client.send(b'##')
                    break
                self.client.send(data)
            f.close()
            print('%s 上传完成' % filename2)

    def doexit(self):
        self.client.send(b'Q')
        sys.exit('谢谢使用')

def main():
    if len(sys.argv)<3:
        print('参数错误')
        return
    address = (sys.argv[1],int(sys.argv[2]))
    client = socket(AF_INET,SOCK_STREAM)
    try:
        client.connect(address)
    except Exception as e:
        print("服务器连接失败！",e)
        return
    while True:
        #创建对象，调用类内的方法
        clientobj = ftpclient(client)
        print("============我的网盘===========")
        print("***    1.查看文件列表       *****")
        print("***    2.下载文件       *****")
        print("***    3.上传文件       *****")
        print("***    4.退出网盘       *****")
        print("==============================")
        cmd = input('请做出选择（1/2/3/4')
        if cmd.strip() in ['1','2','3','4']:
            if cmd == '1':
                clientobj.dolist()
            elif cmd == '2':
                clientobj.doget()
            elif cmd == '3':
                clientobj.doput()
            else:
                clientobj.doexit()
        else:
            print('请做出正确的选择（1/2/3/4)')
        
if __name__ == "__main__":
    main()