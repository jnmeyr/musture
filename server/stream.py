import pyaudio
import numpy
import collections
import sys

class Stream:

    CHUNK = 2048
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 10

    def __enter__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
          format = pyaudio.paInt16,
          channels = Stream.CHANNELS,
          rate = Stream.RATE,
          input = True,
          frames_per_buffer = Stream.CHUNK
        )
        self.stream.start_stream()
        self.maximums = collections.deque(maxlen = 1024)

        return self

    def read(self):
        bothSignals = numpy.fromstring(self.stream.read(Stream.CHUNK), dtype = numpy.int16)
        leftSignals, rightSignals = bothSignals[0::2], bothSignals[1::2]

        return leftSignals, rightSignals

    def fft(self, signals):
        signals = numpy.fft.fft(signals)
        firstSignals, secondSignals = numpy.split(numpy.abs(signals), 2)
        secondSignals = numpy.flipud(secondSignals)
        signals = numpy.add(firstSignals, secondSignals)

        return signals

    def aggregate(self, signals):
        aggregatedSignals = []

        n = 0
        while signals.size >= 2 ** n:
            splitSignals = numpy.split(signals, [2 ** n, signals.size])
            headSignals, tailSignals = splitSignals[0], splitSignals[1]
            aggregatedSignals.append(numpy.max(headSignals))
            signals = tailSignals
            n += 1

        return aggregatedSignals

    def scale(self, leftSignals, rightSignals):
        self.maximums.append(max(numpy.max(leftSignals), numpy.max(rightSignals)))
        maximum = max(max(self.maximums), sys.float_info.min)
        leftSignals = numpy.true_divide(numpy.multiply(leftSignals, 255), maximum).astype(int)
        rightSignals = numpy.true_divide(numpy.multiply(rightSignals, 255), maximum).astype(int)

        return leftSignals, rightSignals

    def concatenate(self, leftSignals, rightSignals):
        leftSignals = numpy.flipud(leftSignals)
        signals = numpy.concatenate((leftSignals, rightSignals))

        return signals


    def listen(self):
        leftSignals, rightSignals = self.read()
        leftSignals = self.aggregate(self.fft(leftSignals))
        rightSignals = self.aggregate(self.fft(rightSignals))
        leftSignals, rightSignals = self.scale(leftSignals, rightSignals)
        signals = self.concatenate(leftSignals, rightSignals)

        return signals

    def __exit__(self, type, value, traceback):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
