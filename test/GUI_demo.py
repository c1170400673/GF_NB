import multiprocessing
import queue
import sys
import threading
import time
import tkinter as tk


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


class RedirectText(object):
    def __init__(self, console):
        self.console = console

    def write(self, string):
        self.console.write(string)
        sys.__stdout__.write(string)


class RedirectError(object):
    def __init__(self, console):
        self.console = console

    def write(self, string):
        self.console.write(string)
        sys.__stderr__.write(string)


class TimePrinter(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def reset(self):
        global time_printer
        new_time_printer = TimePrinter(self.queue)
        time_printer.stop()
        time_printer = new_time_printer

    def run(self):
        while not self.stop_event.is_set():
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            self.queue.put(current_time)
            time.sleep(0.5)


def print_time(qe):
    while True:
        try:
            message = qe.get(block=False)
            sys.stdout.write(message + '\n')
        except queue.Empty:
            break


root = tk.Tk()
root.title("Time Printer")
console = Console(root)
console.pack(fill='both', expand=True)
sys.stdout = RedirectText(console)
sys.stderr = RedirectError(console)

output_queue = multiprocessing.Queue()
time_printer = TimePrinter(output_queue)


def start():
    global time_printer
    if time_printer is None:
        time_printer = TimePrinter(output_queue)
        time_printer.start()
    elif not time_printer.is_alive():
        time_printer.reset()
        time_printer.start()
    root.after(1000, print_time, output_queue)


def stop():
    time_printer.stop()


def reset():
    global time_printer
    if time_printer is not None:
        time_printer.reset()


def quit_app():
    global time_printer
    if time_printer is not None:
        time_printer.stop()
    output_queue.close()
    output_queue.join_thread()
    root.destroy()


button_frame = tk.Frame(root)
button_frame.pack(expand=True, anchor=tk.CENTER)

button_start = tk.Button(button_frame, text="Start", command=start)
button_start.pack(side=tk.LEFT, padx=5, pady=5, anchor=tk.CENTER)

button_stop = tk.Button(button_frame, text="Stop", command=stop)
button_stop.pack(side=tk.LEFT, padx=5, pady=5, anchor=tk.CENTER)

button_reset = tk.Button(button_frame, text="Reset", command=reset)
button_reset.pack(side=tk.LEFT, padx=5, pady=5, anchor=tk.CENTER)

button_quit = tk.Button(button_frame, text="Quit", command=quit_app)
button_quit.pack(side=tk.LEFT, padx=5, pady=5, anchor=tk.CENTER)

while True:
    try:
        root.update_idletasks()
        root.update()
        print_time(output_queue)
    except KeyboardInterrupt:
        time_printer.stop()
        break

root.mainloop()
