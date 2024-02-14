import pyaudio
from __config import *
from __utils import *
from abc import ABC, abstractmethod
from tests.test_audio import test_audio
from queue import Queue
from threading import Event
import json

class Transcriber(ABC):

    def __init__(self, transcript_queue:Queue, run_flag: Event):
        self.transcript_queue = transcript_queue
        self.run_flag = run_flag

    @abstractmethod
    def transcribe(self)->None:
        pass

    

class VoskTranscriber(Transcriber):
    def __init__(self, 
                 transcript_queue:Queue, 
                 run_flag: Event, 
                 model_size = "small"):
        """Transcribes the voice from the source and puts each confirmed word into `transcript_queue`"""
        super().__init__(transcript_queue, run_flag)

        from vosk import Model, KaldiRecognizer
        if model_size == "small":
            self.model = Model("./models/vosk-model-small-en-us-0.15")
        elif model_size == "large":
            self.model = Model("./models/vosk-model-en-us-0.22")
        else:
            raise ValueError("Invalid model size")
        
        
        self.recognizer = KaldiRecognizer(self.model, SAMPLE_RATE)
        self.recognizer.SetWords(True)  #Why?
        self.recognizer.SetPartialWords(True) #Why?
        self.p = pyaudio.PyAudio()
        test_audio(self.p)
        self.stream = self.p.open(rate=SAMPLE_RATE,
                            channels=CHANNELS,
                            format=AUDIO_FORMAT,
                            input=True,
                            input_device_index=get_input_device_index(self.p),
                            frames_per_buffer=CHUNK_SIZE)

    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        #FIXME: is it needed?

    def transcribe(self):
        confirmed_len = 0
        t1 = []
        t2 = []

        while True:
            self.run_flag.wait()
            while self.run_flag.is_set():
                data = self.stream.read(CHUNK_SIZE, exception_on_overflow = True)
                if len(data) == 0:
                    continue
                status = self.recognizer.AcceptWaveform(data)
                if status:
                    result = self.recognizer.Result()
                    #ignore the result
                    
                else:
                    confirmed_words = []
                    partial_result = json.loads(self.recognizer.PartialResult())
                    try:
                        # self.transcript_queue.put(partial_result["partial_result"])
                        t2 = partial_result["partial_result"]
                        
                        # if new partial result
                        if len(t2) < len(t1):
                            confirmed_words = t1[confirmed_len:]
                            confirmed_len = 0
                        # if partial result extended
                        elif len(t2) >= len(t1):
                            for i in range(len(t1)-1,-1,-1):
                                if t1[i]['word'] == t2[i]['word']:
                                    confirmed_words = t1[confirmed_len:i+1]
                                    confirmed_len=i+1
                                    break
                        t1 = t2

                        for word in confirmed_words:
                            self.transcript_queue.put(word['word'])
                    
                    except KeyError as e: #final result
                        continue
                            



class MockTranscriber(Transcriber):
    def __init__(self, transcript_queue:Queue, command_queue: Queue):
        super().__init__(transcript_queue, command_queue)

    def start_transcription(self):
        import time
        with open('test_data/partials.json', 'r') as f:
            partials = json.load(f)
        for item in partials:
            try:
                self.transcript_queue.put(item["partial_result"])
                print(f"transcript of length {len(item['partial_result'])} put succesfully.")
                time.sleep(1.5)
            except KeyError as ke:
                continue

def mock_transcribeAPI(transcript_queue, command_queue):
    m = MockTranscriber(transcript_queue, command_queue)
    m.start_transcription()