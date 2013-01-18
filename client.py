import socket

def send_data(data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 8080))
    s.sendall(data + '\r\n')

    res = []
    while True:
        _res = s.recv(1024)
        if not _res:
            break
        res.append(_res)

    return ''.join(res)



if __name__ == '__main__':
    import sys
    data = sys.argv[1:]

    print "sending", data
    for d in data:
        print send_data(d)
