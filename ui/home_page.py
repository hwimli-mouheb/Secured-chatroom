import tkinter as tk


class HomePage:
    def __init__(self, context):
        self.context = context

    def show(self):
        for widget in self.context.winfo_children():
            widget.destroy()
        tk.Label(self.context, text="Home", font=(
            "arial", 18, "bold"), bg=self.context.bg_color,fg="#FF3399").pack(pady=20)
        tk.Label(self.context, text=f"welcome to your chatroom {self.context.client.username}", font=(
            "arial", 18, "bold"), bg=self.context.bg_color,fg="#FF3399").pack(pady=20)
        menu_frame = tk.Frame(self.context, bg=self.context.bg_color)

        menu_frame.pack(pady=20)
        menu_frame.rowconfigure(0, weight=1)
        chat_button = tk.Button(menu_frame, text="Chat with a friend", font=("arial", 14), width=20, height=2, bg='#FF3399',
                                fg='white', command=self.context.show_chat_page)
        chat_button.grid(row=0, column=0, padx=10, pady=10,
                         sticky=tk.N + tk.S + tk.E + tk.W)
