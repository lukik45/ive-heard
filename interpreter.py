
from queue import Queue
import json


class Interpreter:
    def __init__(self, transcript_queue:Queue, words_queue:Queue, command_queue:Queue) -> None:
        self.transcript_queue = transcript_queue
        self.words_queue = words_queue
        self.command_queue = command_queue
        self.confirmed_len = 0
        self.t1 = []
        self.t2 = []
        self.start()

    def populate_queue(self, words):
        for word in words:
            self.words_queue.put(word)

    def start(self):
        confirmed_words=[]
        while not self.command_queue.empty():
        # while not self.transcript_queue.empty():
            self.t2 = self.transcript_queue.get()

            # if new partial result
            if len(self.t2) < len(self.t1):
                confirmed_words = self.t1[self.confirmed_len:]
                self.confirmed_len = 0
            # if partial result extended
            elif len(self.t2) >= len(self.t1):
                for i in range(len(self.t1)-1,-1,-1):
                    if self.t1[i]['word'] == self.t2[i]['word']:
                        confirmed_words = self.t1[self.confirmed_len:i+1]
                        self.confirmed_len=i+1
                        break
            self.t1 = self.t2

            self.populate_queue(confirmed_words)
            # print([w["word"] for w in confirmed_words])    
                

def test_interpreter():
    transcript_queue = Queue()
    words_queue = Queue()
    command_queue = Queue()
    command_queue.put(True)
    interpreter = Interpreter(transcript_queue, words_queue, command_queue)

    with open('test_data/partials.json', 'r') as f:
        partials = json.load(f)
        for item in partials:
            try:
                transcript_queue.put(item["partial_result"])
                # print(f"transcript of length {len(item['partial_result'])} put succesfully.")
                print(item["partial"])
            except KeyError as ke:
                continue
    
    interpreter.start()
            
        
if __name__ == "__main__":
    test_interpreter()
    