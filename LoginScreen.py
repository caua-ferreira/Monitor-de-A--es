import tkinter as tk
from tkinter import messagebox
import json
import os

class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x300")

        # Dados de usuários
        self.users_data_file = "users_data.json"
        self.users = self.load_users()

        # Tela de login
        self.create_login_screen()

    def load_users(self):
        # Carrega os dados de usuários do arquivo JSON
        if os.path.exists(self.users_data_file):
            with open(self.users_data_file, "r") as f:
                return json.load(f)
        else:
            return {}

    def save_users(self):
        # Salva os dados de usuários no arquivo JSON
        with open(self.users_data_file, "w") as f:
            json.dump(self.users, f)

    def create_login_screen(self):
        # Tela de login
        tk.Label(self.root, text="Login", font=("Arial", 18)).pack(pady=20)

        tk.Label(self.root, text="E-mail:").pack()
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack(pady=5)

        tk.Label(self.root, text="Senha:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Entrar", command=self.login_user).pack(pady=10)
        tk.Button(self.root, text="Criar Conta", command=self.create_signup_screen).pack(pady=5)

    def login_user(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if email in self.users and self.users[email]["password"] == password:
            self.clear_screen()
            # Aqui, chame a função que irá carregar a tela principal
            app.show_main_screen()
        else:
            messagebox.showerror("Erro", "E-mail ou senha incorretos.")


    def create_signup_screen(self):
        # Tela de cadastro
        self.clear_screen()

        tk.Label(self.root, text="Criar Conta", font=("Arial", 18)).pack(pady=20)

        tk.Label(self.root, text="Nome Completo:").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack(pady=5)

        tk.Label(self.root, text="E-mail:").pack()
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack(pady=5)

        tk.Label(self.root, text="Senha:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Cadastrar", command=self.signup_user).pack(pady=10)
        tk.Button(self.root, text="Voltar ao Login", command=self.create_login_screen).pack(pady=5)

    def signup_user(self):
        # Função de cadastro de novo usuário
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if email in self.users:
            messagebox.showerror("Erro", "Este e-mail já está cadastrado.")
        elif name == "" or email == "" or password == "":
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
        else:
            self.users[email] = {"name": name, "password": password}
            self.save_users()
            messagebox.showinfo("Sucesso", "Conta criada com sucesso!")
            self.create_login_screen()

    def clear_screen(self):
        # Função para limpar a tela atual
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginScreen(root)
    root.mainloop()
