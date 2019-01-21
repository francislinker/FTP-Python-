def fun():
    print('启动生成器')
    for i in range(5):
        yield 1
    print('结束生成器')

go=fun()
while True:
    try:
        print(next(go))
    # print(next(go))
    except StopIteration:
        print('程序结束')
        break