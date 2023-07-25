import multiprocessing
import queue
import sys
import threading
import time
import tkinter as tk
from tkinter import ttk


class Console(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.text = tk.Text(self, wrap='word')
        self.text.pack(fill='both', expand=True)
        self.text.config(state='disabled')

    def write(self, message):
        self.text.config(state='normal')
        self.text.insert('end', str(message))
        self.text.see('end')
        self.text.config(state='disabled')

    def clear(self):
        self.text.config(state='normal')
        self.text.delete(1.0, 'end')
        self.text.config(state='disabled')


class RedirectText(object):
    def __init__(self, console):
        self.console = console

    def write(self, string):
        self.console.write(string)
        sys.__stdout__.write(string)

    def flush(self):
        pass


class RedirectError(object):
    def __init__(self, console):
        self.console = console

    def write(self, string):
        self.console.write(string)
        sys.__stderr__.write(string)

    def flush(self):
        pass


class TimePrinter(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.stop_event = threading.Event()
        self.reset_event = threading.Event()
        self.pause_event = threading.Event()
        self.pause_event.set()

    def stop(self):
        self.stop_event.set()

    def reset(self):
        self.reset_event.set()

    def pause(self):
        self.pause_event.clear()

    def resume(self):
        self.pause_event.set()

    def run(self):
        while not self.stop_event.is_set() and not self.reset_event.is_set():
            worker(self.queue)


def worker(queue):
    for i in range(11):
        while True:
            if time_printer.pause_event.is_set():
                break
        if time_printer.stop_event.is_set() or time_printer.reset_event.is_set():
            queue.put("停止任务")
            break
        queue.put(str(i))
        time.sleep(0.1)


def print_time(qe):
    while True:
        try:
            message = qe.get(block=False)
            sys.stdout.write(message + '\n')
        except queue.Empty:
            break


def start():
    global time_printer
    if time_printer is None:
        time_printer = TimePrinter(output_queue)
        print("A")
        time_printer.start()
    elif not time_printer.is_alive() and not time_printer.stop_event.is_set() and not time_printer.reset_event.is_set():
        print("B")
        time_printer.start()
    elif time_printer.stop_event.is_set():
        time_printer = TimePrinter(output_queue)
        print("C")
        time_printer.start()
    elif time_printer.reset_event.is_set():
        time_printer = TimePrinter(output_queue)
        print("D")
        time_printer.start()
    # root.after(20000, print_time, output_queue)


def pause():
    global time_printer
    print("暂停任务")
    time_printer.pause()


def resume():
    global time_printer
    time_printer.resume()


def stop():
    global time_printer
    if time_printer is not None:
        time_printer.stop()
    while not output_queue.empty():
        output_queue.get()


def clear():
    console.clear()


def reset():
    global time_printer
    time_printer.reset()
    if time_printer.is_alive():
        time.sleep(0.1)
    new_time_printer = TimePrinter(output_queue)
    time_printer = new_time_printer
    print("重置了任务")
    time_printer.start()


def quit_app():
    global time_printer
    if time_printer is not None and time_printer.pause_event.is_set():
        time_printer.stop()
    elif time_printer is not None and time_printer.pause_event is not True:
        time_printer.resume()
        time.sleep(0.1)
        time_printer.stop()
    output_queue.close()
    output_queue.join_thread()
    root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Time Printer")
    console = Console(root)
    # console.pack(fill='both', expand=True)
    console.pack(side='right', padx=5, expand=True, fill='y')
    sys.stdout = RedirectText(console)
    sys.stderr = RedirectError(console)
    output_queue = multiprocessing.Queue()
    time_printer = TimePrinter(output_queue)
    button_frame = tk.Frame(root)
    button_frame.pack(side='left', padx=5, expand=True)

    combo_frame = tk.Frame(root)
    combo_frame.pack(side='right', padx=8, expand=True)
    keys = ["January", "February", "March", "April"]
    comboExample = ttk.Combobox(combo_frame, values=keys)
    comboExample.pack(padx=8)
    comboExample.current(0)

    button_start = tk.Button(button_frame, text="Start", command=start, width=10, height=1)
    button_start.pack(padx=5, pady=5)

    button_stop = tk.Button(button_frame, text="Stop", command=stop, width=10, height=1)
    button_stop.pack(padx=5, pady=5)

    button_start = tk.Button(button_frame, text="Pause", command=pause, width=10, height=1)
    button_start.pack(padx=5, pady=5)

    button_start = tk.Button(button_frame, text="Resume", command=resume, width=10, height=1)
    button_start.pack(padx=5, pady=5)

    button_reset = tk.Button(button_frame, text="Reset", command=reset, width=10, height=1)
    button_reset.pack(padx=5, pady=5)

    clear_button = tk.Button(button_frame, text='Clear', command=clear, width=10, height=1)
    clear_button.pack(padx=5, pady=5)

    button_quit = tk.Button(button_frame, text="Quit", command=quit_app, width=10, height=1)
    button_quit.pack(padx=5, pady=5)

    while True:
        try:
            root.update_idletasks()
            root.update()
            print_time(output_queue)
        except KeyboardInterrupt:
            time_printer.stop()
            break

    root.mainloop()
