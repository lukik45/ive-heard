from queue import Queue
from transcriber import VoskTranscriber
from threading import Thread, Event

class WordProcessor:

    def __init__(self, dao, run_flag: Event):
        self.known_words = {}
        self.run_flag :Event = run_flag
        self.words_queue = Queue()
        self.transcript_queue = Queue()
        self.dao = dao
    


    def load_known_words(self):
        # raise NotImplementedError("Load words from database")
        pass
    
    def run_transcriber(self):
        vt = VoskTranscriber(self.transcript_queue, 
                             self.run_flag, 
                             model_size="large")
        transcriber_thread = Thread(target=vt.transcribe)
        transcriber_thread.start()

    def listen_to_words(self):
        while True:
            while self.run_flag.is_set():
                next_word = self.transcript_queue.get()
                print(next_word)

    def start(self):
        self.run_flag.set()
        self.load_known_words()
        self.run_transcriber()
        self.listen_to_words()


if __name__ == "__main__":

    run_flag = Event()
    dao = None
    wp = WordProcessor(dao, run_flag)
    wp.start()
    print("Done")

