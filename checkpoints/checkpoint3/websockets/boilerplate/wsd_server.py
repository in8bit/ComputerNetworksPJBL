#!/usr/bin/python
# File: wsd_server.py
# websocket duplex communication example
# Author: Bob Gailer
# May 10, 2018
# Added by Zheng:
# creat a folder: D:\websocketd
# put both websocketd.exe and this file to that folder
# windows command line: D:\websocketd>websocketd --port=8080 --devconsole python wsd_server.py
from sys import stdout, stdin
import threading
from time import sleep

n = 2 # initial sleep time

def send(t):
    # send string to web page
    stdout.write(t+'\n')
    stdout.flush()

# start a thread to receive & echo back strings from web page
# and to change sleep time
def receive():
    global n
    while True:
        t = stdin.readline().strip()
        if not t:
            break
        send(t)
        if t.isdigit():
            n = int(t) # change global sleep time
t0 = threading.Thread(target=receive)
t0.start()

# start a thread to send words to web page
def send_stuff():
    for word in "Now is the time for all good men to come to the Kool-Aid".split():
        sleep(n)
        send(word)
t1 = threading.Thread(target=send_stuff)
t1.start()

# suspend main thread until worker threads are done
t0.join()
t1.join()