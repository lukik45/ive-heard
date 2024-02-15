from queue import Queue
from transcriber import VoskTranscriber
from threading import Thread, Event
from word import Word
from dao import DataAccessObject

class WordProcessor:

    def __init__(self, run_flag: Event, 
                 ui_words_queue: Queue, 
                 ui_word_pressed_queue:Queue):
        self.known_words = dict()
        self.run_flag :Event = run_flag
        self.transcript_queue = Queue()
        self.ui_words_queue = ui_words_queue
        self.ui_word_pressed_queue = ui_word_pressed_queue
        self.dao = DataAccessObject()
        self.start()


    # Database methods
    def load_words(self): 
        words = self.dao.get_words()
        for word in words:
            self.known_words[word[1]] = Word(word[1], word[2], word[0])
    
    def save_words(self):
        for word in self.known_words.values():
            self.dao.insert_word(word)

    def save_word(self, word: Word, dao:DataAccessObject=None):
        if dao:
            dao.insert_word(word)
        else:
            self.dao.insert_word(word)

    def update_word(self, word: Word, dao:DataAccessObject=None):
        if dao:
            dao.update_word(word)
        else:
            self.dao.update_word(word)

    def delete_word(self, word: Word, dao:DataAccessObject=None):
        if dao:
            dao.delete_word(word)
        else:
            self.dao.delete_word(word)

    def add_to_known_words(self, word: Word):
        self.known_words[word.text] = word
        word.status = 1

    def update_clicked_words(self):
        # initialize differernt dao object to avoid threading issues
        dao = DataAccessObject()
        while True:
                # will wait until a  queue is not empty
                next_word = self.ui_word_pressed_queue.get()
                if next_word.text not in self.known_words:
                    self.add_to_known_words(next_word)
                    self.save_word(next_word, dao)
                    print(f"{next_word.text} added to known words")
                else:
                    print(f"{next_word.text} already in known words")

    # Transcriber methods
    def run_transcriber(self):
        vt = VoskTranscriber(self.transcript_queue, 
                             self.run_flag, 
                             model_size="large")
        transcriber_thread = Thread(target=vt.transcribe)
        transcriber_thread.start()

    def interpret_words(self):
        while True:
            self.run_flag.wait()
            while self.run_flag.is_set():
                next_word = self.transcript_queue.get()
                if next_word not in self.known_words:
                    self.ui_words_queue.put(Word(next_word))
                else: 
                    self.ui_words_queue.put(self.known_words[next_word])


    def start(self):
        self.run_flag.set()
        self.load_words()
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

