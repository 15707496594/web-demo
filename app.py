# -*- coding: utf-8 -*-

import socket


def f1(request):
    return 'f1'


def f2(request):
    return 'f2'


routers = {
    '/f1': f1,
    '/f2': f2,
}


def run():
    sock = socket.socket()
    sock.bind(('127.0.0.1', 8080))
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        # 有人来请求了
        # 获取用户发送的散户局
        data = str(conn.recv(8096), encoding='utf-8')
        headers, bodies = data.split('\r\n\r\n')
        temp_list = headers.split('\r\n')
        method, url, protocol = temp_list[0].split(' ')
        conn.send(b'HTTP/1.1 200 OK\r\n\r\n')  # 响应头，返回byte类型
        func_name = None
        for router, func in routers.items():
            if router == url:
                func_name = func
                break
        if func_name:
            response = func_name(data)
        else:
            response = '404 Not Found'
        conn.send(bytes(response, encoding='utf-8'))
        conn.close()


if __name__ == '__main__':
    run()
