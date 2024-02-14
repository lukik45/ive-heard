from queue import Queue
from transcriber import VoskTranscriber
from threading import Thread, Event
from word import Word

class WordProcessor:

    def __init__(self, run_flag: Event, 
                 ui_words_queue: Queue, 
                 ui_word_pressed_queue:Queue):
        self.known_words = dict()
        self.run_flag :Event = run_flag
        self.transcript_queue = Queue()
        self.ui_words_queue = ui_words_queue
        self.ui_word_pressed_queue = ui_word_pressed_queue

        self.start()


    def load_known_words(self):
        # raise NotImplementedError("Load words from database")
        pass
    
    def run_transcriber(self):
        vt = VoskTranscriber(self.transcript_queue, 
                             self.run_flag, 
                             model_size="large")
        transcriber_thread = Thread(target=vt.transcribe)
        transcriber_thread.start()

    def update_clicked_words(self):
        while True:
            self.run_flag.wait()
            while self.run_flag.is_set():
                next_word = self.ui_word_pressed_queue.get()
                self.add_to_known_words(next_word)
                print("Word added to known words")
                print(next_word)

    def interpret_words(self):
        while True:
            self.run_flag.wait()
            while self.run_flag.is_set():
                next_word = self.transcript_queue.get()
                if next_word not in self.known_words:
                    self.ui_words_queue.put(Word(next_word))
                else: 
                    self.ui_words_queue.put(self.known_words[next_word])

    def add_to_known_words(self, word: Word):
        self.known_words[word.text] = word
        word.status = 1

    def start(self):
        self.run_flag.set()
        self.load_known_words()
        self.run_transcriber()
        interpreter = Thread(target=self.interpret_words)
        interpreter.start()
        updater = Thread(target=self.update_clicked_words) 
        updater.start()


if __name__ == "__main__":

    run_flag = Event()
    dao = None
    wp = WordProcessor(dao, run_flag)
    wp.start()
    print("Done")

