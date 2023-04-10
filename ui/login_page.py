import os
import tkinter as tk
from config.message import Message
import customtkinter
from tkinter import messagebox
import ssl
import CertificateAuthority as CA
import cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509

class LoginPage:
    def __init__(self, context):
        self.context = context
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.alert_message = None

    def show(self):
        for widget in self.context.winfo_children():
            widget.destroy()
        title = tk.Label(self.context, text="Log in with your personal credentials or create an account", font=(
            "arial", 15, "bold"), bg=self.context.bg_color,fg="#FF3399")
        title.pack(pady=5)
        
        authF = tk.Frame(self.context, bg=self.context.bg_color)
        authF.pack(pady=0)
        authF.rowconfigure(0, weight=1)
        usernameL = tk.Label(
            authF, text="Username", bg=self.context.bg_color,fg="#FFFFFF", font=("Arial", 16))
        usernameL.grid(row=0, column=0, padx=20, pady=10,
                       sticky=tk.N + tk.S + tk.E + tk.W)
        usernameInput = tk.Entry(authF, textvariable=self.username)
        usernameInput.grid(row=0, column=1, padx=20, pady=10,
                           sticky=tk.N + tk.S + tk.E + tk.W)
        passwordL = tk.Label(authF, text="Password",
                             bg=self.context.bg_color,fg="#FFFFFF", font=("Arial", 16))
        passwordL.grid(row=2, column=0, padx=20, pady=10,
                       sticky=tk.N + tk.S + tk.E + tk.W)
        passwordInput = tk.Entry(authF, textvariable=self.password, show="*")
        passwordInput.grid(row=2, column=1, padx=20, pady=10,
                           sticky=tk.N + tk.S + tk.E + tk.W)
        # alert msg : error or success
        self.alert_message = tk.Label(self.context, text="", font=(
            "arial", 15), bg=self.context.bg_color)
        self.alert_message.pack()
        loginButton = tk.Button(authF, text="Login", command=self.login, font=("arial", 14),
                                bg='#FF3399',
                                fg='white')
        loginButton.grid(row=11, column=0, padx=10, pady=10,
                         sticky=tk.N + tk.S + tk.E + tk.W)
        
        registerButton = tk.Button(authF, text="Register", command=self.context.show_register_page,
                                   font=("arial", 14),
                                   bg='#FF3399',
                                   fg='white')
        registerButton.grid(row=11, column=1, padx=10,
                            pady=10, sticky=tk.N + tk.S + tk.E + tk.W)
        usernameL.grid(row=1, column=0)
        usernameInput.grid(row=1, column=1, pady=20)
        passwordL.grid(row=2, column=0)
        passwordInput.grid(row=2, column=1, pady=20)

   
    """ 
    def request_certificate(user,self):
        # Generate a certificate request for the user
        subject = x509.Name([
                x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, u"example.com"),
            ])
        csr = x509.CertificateSigningRequestBuilder().subject_name(
                subject
            ).add_extension(
                x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
                critical=False,
            ).sign(
                self.context.client.private_key,
                cryptography.hazmat.primitives.hashes.SHA256(),
                default_backend()
            )

        csr_pem = csr.public_bytes(serialization.Encoding.PEM)

        with open("certificate_request.pem", "wb") as f:
            f.write(csr_pem)
            
        CA.create_certificate_from_req(user.username,csr_pem)
        # Save the certificate request for the user
        with open(f'{user}.csr', 'wb') as f:
            f.write(cert_request)

        # Issue the certificate if it has been requested
        if os.path.exists(f'{user}.csr'):
            with open(f'{user}.csr', 'rb') as f:
                cert_request = f.read()
            cert = CA.issue_certificate(user, cert_request)
    """
        
    def login(self):
        login_object = {
            'username': self.username.get(),
            'password': self.password.get()
        }
        # self.request_certificate(self)
       
        message = Message('LOGIN', login_object)
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
            self.context.client.username = self.username.get()
            self.context.show_home_page()
        else:
            messagebox.showinfo(title="Login Error", message="Invalid credentials.Please try again.")
