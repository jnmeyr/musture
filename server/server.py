import multiprocessing
from Queue import Empty
import time
import os
import sys

from stream import Stream
from network import ValueConnection, ControlConnection

def listen(event, queue):
    with Stream() as stream:
        while not event.is_set():
            signals = stream.listen()
            message = bytearray()
            for signal in signals:
                message.append(signal)
            try:
                queue.get(False)
            except Empty:
                pass
            queue.put(message)

def tell(event, queue):
    with ValueConnection(sys.argv[1], 50001) as connection:
        while not event.is_set():
            try:
                message = queue.get(True, 1)
                connection.tell(message)
            except Empty:
                pass

def control(event, stdin):
    sys.stdin = stdin
    while not event.is_set():
        strings = raw_input("")
        if strings == "q":
            event.set()
        else:
            try:
                integers = map(int, strings.split())
                message = bytearray()
                for index in range(4):
                    message.append(integers[index])
                with ControlConnection(sys.argv[1], 50000) as connection:
                    connection.order(message)
            except:
                pass

if __name__ == "__main__":
    event = multiprocessing.Event()
    queue = multiprocessing.Queue(1)
    listener = multiprocessing.Process(target = listen, args = (event, queue))
    listener.start()
    teller = multiprocessing.Process(target = tell, args = (event, queue))
    teller.start()
    controller = multiprocessing.Process(target = control, args = (event, os.fdopen(os.dup(sys.stdin.fileno()))))
    controller.start()
    listener.join()
    teller.join()
    controller.join()
