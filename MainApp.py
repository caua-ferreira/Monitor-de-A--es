import tkinter as tk
from tkinter import ttk, messagebox
from AnaliseGeralScreen import AnaliseGeralScreen
from LoginScreen import LoginScreen
from PortfolioScreen import PortfolioScreen  # Certifique-se de ter criado este arquivo separado

class InvestmentMonitorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Investment Monitor")
        
        # Definir o tamanho da janela como 1920x1080
        self.geometry("1280x720")
        
        self.login_window = None  # Variável para verificar se o pop-up já está aberto

        # Cria a estrutura principal
        self.create_side_menu()
        self.create_main_area()

    def create_side_menu(self):
        # Cria um frame para o menu lateral
        self.side_menu = tk.Frame(self, bg="#333", width=200)
        self.side_menu.pack(side="left", fill="y")

        # Função para estilizar botões ao passar o mouse (hover)
        def on_hover(event, button):
            button.config(bg="blue", fg="white")

        def on_leave(event, button):
            button.config(bg="#444", fg="white")

        # Função para marcar botão como selecionado
        def select_button(button):
            for btn in self.menu_buttons.values():
                btn.config(bg="#444", fg="white")
            button.config(bg="blue", fg="white")

        # Cria os botões para cada aba no menu lateral
        self.menu_buttons = {
            "Análise Geral": tk.Button(self.side_menu, text="Análise Geral", bg="#444", fg="white", font=("Arial", 14), command=lambda: self.show_analysis_screen(select_button(self.menu_buttons["Análise Geral"]))),
            "Portfólio": tk.Button(self.side_menu, text="Portfólio", bg="#444", fg="white", font=("Arial", 14), command=lambda: self.show_portfolio_screen(select_button(self.menu_buttons["Portfólio"]))),
            "Gráficos": tk.Button(self.side_menu, text="Gráficos", bg="#444", fg="white", font=("Arial", 14), command=lambda: self.show_graph_screen(select_button(self.menu_buttons["Gráficos"]))),
            "Alertas": tk.Button(self.side_menu, text="Alertas", bg="#444", fg="white", font=("Arial", 14), command=lambda: self.show_alert_screen(select_button(self.menu_buttons["Alertas"]))),
            "Relatórios": tk.Button(self.side_menu, text="Relatórios", bg="#444", fg="white", font=("Arial", 14), command=lambda: self.show_report_screen(select_button(self.menu_buttons["Relatórios"]))),
            "Login": tk.Button(self.side_menu, text="Login", bg="#444", fg="white", font=("Arial", 14), command=lambda: self.show_login_popup()),
        }

        # Posiciona os botões no menu lateral e adiciona eventos de hover
        for btn in self.menu_buttons.values():
            btn.pack(pady=20, fill="x")
            btn.bind("<Enter>", lambda e, b=btn: on_hover(e, b))
            btn.bind("<Leave>", lambda e, b=btn: on_leave(e, b))

    def create_main_area(self):
        # Frame principal onde as telas são mostradas
        self.main_area = tk.Frame(self, bg="white")
        self.main_area.pack(side="right", expand=True, fill="both")

    def show_analysis_screen(self, selected=None):
        # Limpa a área principal e carrega a tela de análise geral
        self.clear_main_screen()
        AnaliseGeralScreen(self.main_area)

    def show_portfolio_screen(self, selected=None):
        # Limpa a área principal e carrega a tela de portfólio
        self.clear_main_screen()
        PortfolioScreen(self.main_area)


    def show_graph_screen(self, selected=None):
        # Limpa a área principal e carrega a tela de gráficos
        self.clear_main_screen()
        # Coloque aqui a chamada da tela de Gráficos

    def show_alert_screen(self, selected=None):
        # Limpa a área principal e carrega a tela de alertas
        self.clear_main_screen()
        # Coloque aqui a chamada da tela de Alertas

    def show_report_screen(self, selected=None):
        # Limpa a área principal e carrega a tela de relatórios
        self.clear_main_screen()
        # Coloque aqui a chamada da tela de Relatórios

    def show_login_popup(self):
        # Verifica se a janela de login já está aberta
        if self.login_window is not None and self.login_window.winfo_exists():
            self.login_window.lift()  # Traz a janela para a frente se ela já estiver aberta
            return

        # Cria uma nova janela de login como pop-up
        self.login_window = tk.Toplevel(self)
        self.login_window.title("Login")
        self.login_window.geometry("300x200")

        # Carregar a tela de login dentro do pop-up
        LoginScreen(self.login_window)

    def clear_main_screen(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = InvestmentMonitorApp()
    app.mainloop()
