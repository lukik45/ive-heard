import pyaudio
from abc import ABC, abstractmethod


class Transcriber(ABC):
    def __init__(self, p: pyaudio.PyAudio):
        self.p = p

    @abstractmethod
    def transcribe(self):
        pass




class VoskTranscriber(Transcriber):
    def __init__(self, p: pyaudio.PyAudio, model_size = "small"):
        super().__init__(p)
        from vosk import Model, KaldiRecognizer
        if model_size == "small":
            self.model = Model("./models/vosk-model-small-en-us-0.15")
        elif model_size == "large":
            self.model = Model("./models/vosk-model-en-us-0.22")
        else:
            raise ValueError("Invalid model size")

    def transcribe(self):
        pass