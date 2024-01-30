from pyaudio import paInt16

CHANNELS = 1
SAMPLE_RATE = 16000 # enough for human speech recognition
AUDIO_FORMAT = paInt16 # 16 bit per sample
# SAMPLE_SIZE = 2 # 16 bit = 2 bytes
CHUNK_SIZE = 8192 # 8192 bytes = 4096 samples = 256 ms


## Device settings
HOST_DEVICE_TYPE = "mac"