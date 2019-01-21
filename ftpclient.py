from socket import *
import sys

class ftpclient(object):
    pass

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
        print("============我的网盘===========")
        print("***    1.查看文件列表       *****")
        print("***    1.下载文件       *****")
        print("***    1.上传文件       *****")
        print("***    1.退出网盘       *****")
        print("==============================")
        cmd = input('请做出选择（1/2/3/4')
        
if __name__ == "__main__":
    main()