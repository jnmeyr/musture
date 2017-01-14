import multiprocessing
from Queue import Empty
import time
import sys

from stream import Stream
from network import Network

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
    with Network(sys.argv[1], 50001) as network:
        while not event.is_set():
            try:
                message = queue.get(True, 1)
                network.tell(message)
            except Empty:
                pass

if __name__ == "__main__":
    event = multiprocessing.Event()
    queue = multiprocessing.Queue(1)
    listener = multiprocessing.Process(target = listen, args = (event, queue))
    listener.start()
    teller = multiprocessing.Process(target = tell, args = (event, queue))
    teller.start()

    raw_input()

    event.set()
    listener.join()
    teller.join()
