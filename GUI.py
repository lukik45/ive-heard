
import tkinter as tk
import customtkinter as ctk
import queue
from threading import Thread, Event
import time
from word import Word
from word_processor import WordProcessor


transcript_queue = queue.Queue()
words_queue = queue.Queue()
word_pressed_queue = queue.Queue()
run_flag = Event()
TRANSCRIPTION_ON = False



def add_widget(text_container, root, word: Word):
    widget = ctk.CTkButton(master=root, text=word.text, width=-5, height=20,
                        command= lambda: word_pressed_queue.put(word),
                        border_color="black", border_width=0, border_spacing=0)
    text_container.configure(state="normal")
    text_container.window_create("insert",
                                  window=widget, 
                                #   padx=10, 
                                #   pady=10
                                )
    text_container.configure(state="disabled")

def update(text_container, root):
    while True:
        next_word = words_queue.get()
        add_widget(text_container, root, word=next_word)


def start_callback():
    raise NotImplementedError()

def stop_callback():
    raise NotImplementedError()


def main():
    
    root = tk.Tk()
    root.geometry("800x600")

    toolbar = tk.Frame(master=root)
    vsb = tk.Scrollbar(master=root)
    text_container = tk.Text(master=root, wrap="word", yscrollcommand=lambda *args: vsb.set(*args))
    vsb.configure(command=text_container.yview)

    toolbar.pack(side="top", fill="x")
    vsb.pack(side="right", fill="y")
    text_container.pack(side="left", fill="both", expand=True)

    start_button = tk.Button(master=toolbar, text="Start", command=start_callback )
    start_button.pack(side="left")
    stop_button = tk.Button(master=toolbar, text="Stop", command=stop_callback)
    stop_button.pack(side="left")

    # print("strating transcriber thread")
    # transcriber_thread = threading.Thread(target=transcribeAPI, args=(transcript_queue, command_queue))
    # transcriber_thread.start()

    # interpreter_thread = threading.Thread(target=Interpreter, args=(transcript_queue, words_queue, command_queue))
    # interpreter_thread.start()

    word_processor_thread = Thread(target=WordProcessor, args=(run_flag, words_queue, word_pressed_queue))
    word_processor_thread.start()

    update_thread = Thread(target=update, args=(text_container, root))
    update_thread.start()

    root.mainloop()    

if __name__ == "__main__":
    main()