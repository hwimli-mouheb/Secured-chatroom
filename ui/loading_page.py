from PIL import Image, ImageTk
import tkinter as tk


class LoadingPage(tk.Toplevel):
    def __init__(self, text, context):
        super().__init__()
        self.context = context
        self.title("Loading..")
        self.geometry("350x300+{}+{}".format(
            int((self.winfo_screenwidth() - 300) / 2),
            int((self.winfo_screenheight() - 150) / 2)
        ))
        self.loading_text = tk.Label(self, text=text)
        self.loading_text.pack()

    def after_loading_page(self):
        connection = self.context.client.connect_with_server()
        self.destroy()
        if connection:
            self.context.deiconify()
            self.context.show_login_page()
        else:
            self.context.show_error_page()

    def show_bootstrap(self):
        self.context.withdraw()
        self.after(1000, self.after_loading_page)
        self.mainloop()
