from pyaudio import paInt16

CHANNELS = 1
SAMPLE_RATE = 16000 # enough for human speech recognition
AUDIO_FORMAT = paInt16 # 16 bit per sample
# SAMPLE_SIZE = 2 # 16 bit = 2 bytes
CHUNK_SIZE = 8192 # 8192 bytes = 4096 samples = 256 ms
# CHUNK_SIZE = 4096 # 4096 bytes = 2048 samples = 128 ms


## Device settings
HOST_DEVICE_TYPE = "mac"

DATABASE_PATH = "local1.db"


# not needed for now
# AUTOSAVE_ON = True
# AUTOSAVE_INTERVAL = 10 # seconds