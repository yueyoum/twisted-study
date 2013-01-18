import threading
import time

from client import send_data

def t_send(d):
    start = time.time()
    #print send_data(d).strip('\r\n')
    send_data(d)
    print 'send {0}, took {1}'.format(d, time.time() - start)

if __name__ == '__main__':
    import sys
    data = sys.argv[1:]

    start = time.time()

    threads = []
    for d in data:
        t = threading.Thread(target=t_send, args=(d,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print 'finish, took', time.time() - start
