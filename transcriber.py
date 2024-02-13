import pyaudio
from __config import *
from __utils import *
from abc import ABC, abstractmethod
from tests.test_audio import test_audio
from queue import Queue
import json


    


    


class Transcriber(ABC):
    def __init__(self, transcript_queue:Queue, command_queue: Queue):
        self.transcript_queue = transcript_queue
        self.command_queue = command_queue

    @abstractmethod
    def start_transcription(self)->None:
        pass

    

class VoskTranscriber(Transcriber):
    def __init__(self, 
                 transcript_queue:Queue, 
                 command_queue: Queue,
                 p: pyaudio.PyAudio, 
                 model_size = "small"):
        
        super().__init__(transcript_queue, command_queue)

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
        self.p = p
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

    def start_transcription(self):
        while not self.command_queue.empty(): #TODO: add a command to stop the transcription
            data = self.stream.read(CHUNK_SIZE, exception_on_overflow = True)
            if len(data) == 0:
                print('no data----------------------------------')
                continue
            status = self.recognizer.AcceptWaveform(data)
            if status:
                result = self.recognizer.Result()
                #ignore the result
            else:
                partial_result = json.loads(self.recognizer.PartialResult())
                try:
                    self.transcript_queue.put(partial_result["partial_result"])
                    print(f"transcript of length {len(partial_result['partial_result'])} put succesfully.")
                        
                
                except KeyError as e: #final result
                    continue
                            
        self.__del__()


def transcribeAPI(transcript_queue, command_queue):
    p = pyaudio.PyAudio()
    test_audio(p)
    r = VoskTranscriber(transcript_queue, command_queue, p)
    r.start_transcription()



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