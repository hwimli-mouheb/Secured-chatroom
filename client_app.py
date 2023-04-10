import tkinter as tk
from config.client import Client
from ui.chat import ChatPage
from ui.error_page import ErrorPage
from ui.loading_page import LoadingPage
from ui.login_page import LoginPage
from ui.home_page import HomePage
from ui.register_page import RegisterPage



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.client = Client(self.log_chat_message)
        self.bg_color = "#333333"
        self.title("Client")
        self.geometry("600x450+{}+{}".format(
            int((self.winfo_screenwidth() - 400) / 2),
            int((self.winfo_screenheight() - 500) / 2)
        ))
        self.configure(bg=self.bg_color)
        self.loading_page = LoadingPage("Connecting...", self)
        self.error_page = ErrorPage("Error connecting", self)
        self.login_page = LoginPage(self)
        self.register_page = RegisterPage(self)
        self.home_page = HomePage(self)
        self.chat_page = ChatPage(self)

        self.bootstrap()

    def bootstrap(self):
        self.loading_page.show_bootstrap()

    def show_error_page(self):
        self.error_page.show()

    def show_login_page(self):
        self.login_page.show()

    def show_register_page(self):
        self.register_page.show()

    def show_home_page(self):
        self.home_page.show()

    def show_chat_page(self):
        self.chat_page.show()

    def log_chat_message(self, *message):
        text = ' '.join(map(str, message))
        self.chat_page.chat_log.insert(tk.INSERT, text)



App().mainloop()
