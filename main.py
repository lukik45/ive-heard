import __utils
from __test import __test_all
from __config import *
import pyaudio
from threading import Thread





if __name__ == '__main__':
    p = pyaudio.PyAudio()
    __test_all(p)


