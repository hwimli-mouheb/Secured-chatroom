import tkinter as tk
from tkinter import ttk
import logging

from config.server import Server


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Chatroom Server")
        self.geometry("700x500")
        self.resizable()
        self.configure(bg='black')

        self.log_text = tk.Text(
            self, wrap=tk.WORD, bg='black', fg='blue', font=('arial', 30))
        self.log_text.pack(expand=True, fill='both',padx=50, pady=50)

        self.log_scrollbar = ttk.Scrollbar(self, command=self.log_text.yview)
        self.log_scrollbar.pack(side=tk.RIGHT, fill='y')

        self.log_text.configure(yscrollcommand=self.log_scrollbar.set)

        self.log_handler = logging.StreamHandler(self)
        self.log_handler.setFormatter(logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(message)s"))
        self.logger = logging.getLogger()
        self.logger.addHandler(self.log_handler)
        self.logger.setLevel(logging.DEBUG)

        self.server = Server(self.write_log)

    def write_log(self, *message):
        text = ' '.join(map(str, message))
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, text + '\n')
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)


App().mainloop()
