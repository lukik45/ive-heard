
import tkinter as tk
from transcriber import transcribeAPI, mock_transcribeAPI
from interpreter import Interpreter
import queue
import threading
import time


transcript_queue = queue.Queue()
words_queue = queue.Queue()
command_queue = queue.Queue()
command_queue.put(True)
TRANSCRIPTION_ON = False


def add_widget(text_container, root, text):
    widget = tk.Label(master=root, width=12, text=text, bd=1, relief="raised",
                      bg="#5C9BD5", foreground="white", padx=4, pady=4)
    text_container.configure(state="normal")
    text_container.window_create("insert", window=widget, padx=10, pady=10)
    text_container.configure(state="disabled")

def update(text_container, root):
    while not command_queue.empty():
        next_word = words_queue.get()["word"]
        add_widget(text_container, root, text=next_word)


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

    print("strating transcriber thread")
    transcriber_thread = threading.Thread(target=transcribeAPI, args=(transcript_queue, command_queue))
    transcriber_thread.start()

    interpreter_thread = threading.Thread(target=Interpreter, args=(transcript_queue, words_queue, command_queue))
    interpreter_thread.start()

    update_thread = threading.Thread(target=update, args=(text_container, root))
    update_thread.start()

    root.mainloop()



if __name__ == "__main__":
    main()