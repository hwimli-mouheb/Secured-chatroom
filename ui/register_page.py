import tkinter as tk
import json
from config.message import Message


class RegisterPage:
    def __init__(self, context):
        self.context = context
        self.username = tk.StringVar()
        self.name = tk.StringVar()
        self.id_ = tk.StringVar()
        self.password = tk.StringVar()
        self.alert_message = None

    def show(self):
        for widget in self.context.winfo_children():
            widget.destroy()
        title = tk.Label(self.context, text="Create an account", font=(
            "arial", 20, "bold"),
                         bg=self.context.bg_color,fg="#FF3399")
        title.pack(pady=5)
        self.alert_message = tk.Label(self.context, text="", font=(
            "arial", 15), bg=self.context.bg_color)
        self.alert_message.pack()

        registerF = tk.Frame(self.context, bg=self.context.bg_color)
        registerF.pack(pady=5)
        registerF.columnconfigure(0, weight=1)

        idL = tk.Label(
            registerF, text="ID", bg=self.context.bg_color,fg="#FFFFFF", font=("Arial", 16))
        idL.grid(row=0, column=0, padx=10, pady=10,
                 sticky=tk.N + tk.S + tk.E + tk.W)
        idInput = tk.Entry(registerF, textvariable=self.id_)
        idInput.grid(row=0, column=1, padx=10, pady=10,
                     sticky=tk.N + tk.S + tk.E + tk.W)
        usernameL = tk.Label(
            registerF, text="Username", bg=self.context.bg_color,fg="#FFFFFF", font=("Arial", 16))
        usernameL.grid(row=2, column=0, padx=10, pady=0,
                       sticky=tk.N + tk.S + tk.E + tk.W)
        usernameInput = tk.Entry(registerF, textvariable=self.username)
        usernameInput.grid(row=2, column=1, padx=10, pady=10,
                           sticky=tk.N + tk.S + tk.E + tk.W)
        passwordL = tk.Label(registerF, text="Password",
                             bg=self.context.bg_color,fg="#FFFFFF", font=("Arial", 16))
        passwordL.grid(row=3, column=0, padx=10, pady=10,
                       sticky=tk.N + tk.S + tk.E + tk.W)
        passwordInput = tk.Entry(
            registerF, textvariable=self.password, show="*")
        passwordInput.grid(row=3, column=1, padx=10, pady=10,
                           sticky=tk.N + tk.S + tk.E + tk.W)
        register_button = tk.Button(registerF, text="Register", command=self.register,
                                    font=("arial", 14),
                                    bg='#FF3399',
                                    fg='white')
        register_button.grid(row=4, column=0, padx=10,
                             pady=10, sticky=tk.N + tk.S + tk.E + tk.W)
        login_button = tk.Button(registerF, text="Login", command=self.context.show_login_page,
                                 font=("arial", 14),
                                 bg='#FF3399',
                                 fg='white')
        login_button.grid(row=4, column=1, padx=10, pady=10,
                          sticky=tk.N + tk.S + tk.E + tk.W)

    def register(self):
        register_object = {
            'name': self.name.get(),
            'id_': self.id_.get(),
            'username': self.username.get(),
            'password': self.password.get()
        }
        message = Message('REGISTER', register_object)
        Message.send_encrypted_message(
            self.context.client.server_socket,
            self.context.client.server_public_key,
            message.to_json()
        )
        server_message = Message.receive_and_decrypt(
            self.context.client.server_socket,
            self.context.client.private_key
        )
        if server_message and server_message == 'OK':
            self.context.show_login_page()
            self.context.login_page.alert_message.configure(
                text="Account created, please log in", fg="green")
        else:
            self.alert_message.configure(text="Error", fg="red")
