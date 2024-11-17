import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import yfinance as yf
from tkcalendar import Calendar
import time

class PortfolioScreen:
    def __init__(self, main_area):
        self.main_area = main_area
        self.portfolio_assets = []  # Lista para armazenar os ativos do portfólio
        self.total_value = 0  # Inicializa o valor total
        self.total_pl = 0  # Inicializa o P&L total
        self.setup_header()
        self.setup_main_area()

        # Atualizar os preços a cada 5 minutos (300000 milissegundos)
        self.update_prices()

    def setup_header(self):
        # Cabeçalho da tela de portfólio com valor total e P&L total
        header_frame = tk.Frame(self.main_area, bg="lightgray", height=80)
        header_frame.pack(fill="x")

        self.total_value_label = tk.Label(header_frame, text="Valor Total: R$ 0.00", font=("Arial", 18), bg="lightgray", fg="green")
        self.total_value_label.pack(side="left", padx=20)

        self.total_pl_label = tk.Label(header_frame, text="P&L Total: R$ 0.00", font=("Arial", 18), bg="lightgray", fg="green")
        self.total_pl_label.pack(side="right", padx=20)

        # Botão de atualizar valores
        tk.Button(header_frame, text="Atualizar Valores", command=self.update_prices).pack(side="right", padx=20)

    # Criação dos botões "Editar" e "Excluir" dentro do setup_main_area
    def setup_main_area(self):
        table_frame = tk.Frame(self.main_area)
        table_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Cria um frame para os botões "Adicionar", "Editar" e "Excluir"
        button_frame = tk.Frame(table_frame)
        button_frame.pack(fill="x", padx=10, pady=5)

        # Botão para adicionar ativo
        self.add_button = tk.Button(button_frame, text="Adicionar Ação", command=self.add_portfolio_popup, bg="#4CAF50")
        self.add_button.pack(side="left", padx=5)

        # Botões "Editar" e "Excluir" inicialmente desabilitados
        self.edit_button = tk.Button(button_frame, text="Editar", state="disabled", command=self.edit_selected_asset, bg="#ADD8E6")
        self.edit_button.pack(side="left", padx=5)

        self.delete_button = tk.Button(button_frame, text="Excluir", state="disabled", command=self.delete_selected_asset, bg="#FF6347")
        self.delete_button.pack(side="left", padx=5)

        # Adiciona a barra de rolagem horizontal e vertical
        scroll_x = tk.Scrollbar(table_frame, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")

        scroll_y = tk.Scrollbar(table_frame, orient="vertical")
        scroll_y.pack(side="right", fill="y")

        # Configuração da tabela do portfólio
        self.asset_tree = ttk.Treeview(table_frame, columns=("Código", "Nome", "Bolsa", "Preço Atual", "Alteração", "% Alteração", "Quantidade", "Valor Atual", "Preço Compra", "P&L", "P&L Total", "Hora"), show="headings", xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        self.asset_tree.heading("Código", text="Código")
        self.asset_tree.heading("Nome", text="Nome da Ação")
        self.asset_tree.heading("Bolsa", text="Bolsa (opcional)")
        self.asset_tree.heading("Preço Atual", text="Preço Atual")
        self.asset_tree.heading("Alteração", text="Alteração no Preço")
        self.asset_tree.heading("% Alteração", text="% da Alteração")
        self.asset_tree.heading("Quantidade", text="Nº de Ações")
        self.asset_tree.heading("Valor Atual", text="Valor Atual")
        self.asset_tree.heading("Preço Compra", text="Preço de Compra")
        self.asset_tree.heading("P&L", text="P&L")
        self.asset_tree.heading("P&L Total", text="P&L Total")
        self.asset_tree.heading("Hora", text="Hora da Compra")

        # Detecta o clique na linha e habilita os botões "Editar" e "Excluir"
        self.asset_tree.bind("<ButtonRelease-1>", self.on_select)

        scroll_x.config(command=self.asset_tree.xview)
        scroll_y.config(command=self.asset_tree.yview)

        self.asset_tree.pack(fill="both", expand=True)


    def add_portfolio_popup(self):
        # Pop-up para adicionar ativo ao portfólio
        self.add_portfolio_window = tk.Toplevel()
        self.add_portfolio_window.title("Adicionar Ação ao Portfólio")
        self.add_portfolio_window.geometry("400x600")

        tk.Label(self.add_portfolio_window, text="Código do Ativo:").pack(pady=10)
        self.asset_code_entry = tk.Entry(self.add_portfolio_window)
        self.asset_code_entry.pack(pady=5)

        tk.Label(self.add_portfolio_window, text="Quantidade:").pack(pady=10)
        self.asset_quantity_entry = tk.Entry(self.add_portfolio_window)
        self.asset_quantity_entry.pack(pady=5)

        tk.Label(self.add_portfolio_window, text="Valor de Compra:").pack(pady=10)
        self.asset_price_entry = tk.Entry(self.add_portfolio_window)
        self.asset_price_entry.pack(pady=5)

        # Seletor de Data de Compra
        tk.Label(self.add_portfolio_window, text="Data de Compra:").pack(pady=10)
        self.purchase_date_entry = Calendar(self.add_portfolio_window, selectmode="day", year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.purchase_date_entry.pack(pady=5)

        # Campo para inserir a hora da compra
        tk.Label(self.add_portfolio_window, text="Hora da Compra (HH:MM):").pack(pady=10)
        self.purchase_time_entry = tk.Entry(self.add_portfolio_window)
        self.purchase_time_entry.insert(0, datetime.now().strftime("%H:%M"))  # Preenche com o horário atual por padrão
        self.purchase_time_entry.pack(pady=5)

        btn_frame = tk.Frame(self.add_portfolio_window)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Adicionar", command=self.confirm_add_portfolio).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cancelar", command=self.add_portfolio_window.destroy).pack(side="right", padx=10)


    def confirm_add_portfolio(self):
        try:
            symbol = self.asset_code_entry.get().upper()
            quantity = int(self.asset_quantity_entry.get())
            purchase_price = float(self.asset_price_entry.get())

            stock = yf.Ticker(symbol + ".SA")
            stock_info = stock.info
            name = stock_info.get('longName', 'N/A')
            last_close = stock.history(period="1d")['Close'][-1]

            # Obter a data e hora de compra do popup
            purchase_date = self.purchase_date_entry.get_date()
            purchase_time = self.purchase_time_entry.get()

            # Concatenar a data e a hora para criar o datetime completo no formato correto (DD/MM/YYYY HH:MM)
            purchase_datetime = datetime.strptime(f"{purchase_date} {purchase_time}", "%d/%m/%Y %H:%M")


            # Adicionar a data de cadastro
            registration_datetime = datetime.now()

            self.portfolio_assets.append({
                "symbol": symbol,
                "name": name,
                "quantity": quantity,
                "purchase_price": purchase_price,
                "time": purchase_datetime.strftime("%H:%M:%S"),
                "registration_time": registration_datetime.strftime("%m/%d/%y %H:%M")  # Salva a data e hora de cadastro
            })

            total_value = quantity * last_close
            price_change = last_close - purchase_price
            percent_change = (price_change / purchase_price) * 100
            total_pl = price_change * quantity

            # Inserir dados na tabela com as colunas ajustadas
            item_id = self.asset_tree.insert("", "end", values=(
                symbol,
                name,
                "BVMF",  # Bolsa (opcional)
                f"R$ {last_close:.2f}",  # Preço Atual
                f"R$ {price_change:.2f}",  # Alteração no preço
                f"{percent_change:.2f}%",  # % Alteração
                quantity,
                f"R$ {total_value:.2f}",  # Valor Atual
                f"R$ {purchase_price:.2f}",  # Preço de Compra
                f"R$ {total_pl:.2f}",  # P&L Total
                purchase_datetime.strftime("%m/%d/%y %H:%M"),  # Data e hora da compra
                registration_datetime.strftime("%m/%d/%y %H:%M")  # Data de cadastro
            ))

            # Aplica cor ao valor de Alteração e P&L Total
            self.apply_color_to_value(item_id, price_change, 4)  # Alteração no preço
            self.apply_color_to_value(item_id, total_pl, 9)  # P&L Total

            # Fechar o popup após adicionar o ativo
            self.add_portfolio_window.destroy()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar ativo {symbol}: {str(e)}")


    def apply_color_to_value(self, item_id, value, column):
        """
        Aplica cor verde para valores positivos e vermelha para valores negativos em uma coluna específica.
        :param item_id: ID do item na Treeview
        :param value: Valor a ser avaliado
        :param column: Índice da coluna onde aplicar a cor
        """
        if value >= 0:
            self.asset_tree.tag_configure('positive', foreground='green')
            self.asset_tree.item(item_id, tags=('positive',))
        else:
            self.asset_tree.tag_configure('negative', foreground='red')
            self.asset_tree.item(item_id, tags=('negative',))

    def update_prices(self):
        # Atualiza os preços dos ativos e recalcula o valor total e P&L
        for i, asset in enumerate(self.portfolio_assets):
            try:
                stock = yf.Ticker(asset["symbol"] + ".SA")
                data = stock.history(period="1d")
                if not data.empty:
                    last_close = data['Close'][-1]
                    price_change = last_close - asset["purchase_price"]
                    percent_change = (price_change / asset["purchase_price"]) * 100
                    total_value = asset["quantity"] * last_close
                    total_pl = price_change * asset["quantity"]

                    # Atualiza os valores na tabela
                    self.asset_tree.item(self.asset_tree.get_children()[i], values=(
                        asset["symbol"],
                        asset["name"],
                        "BVMF",  # Bolsa (opcional)
                        f"R$ {last_close:.2f}",  # Preço Atual
                        f"R$ {price_change:.2f}",  # Alteração no preço
                        f"{percent_change:.2f}%",  # % Alteração
                        asset["quantity"],
                        f"R$ {total_value:.2f}",  # Valor Atual
                        f"R$ {asset['purchase_price']:.2f}",  # Preço de Compra
                        f"R$ {price_change:.2f}",  # P&L
                        f"R$ {total_pl:.2f}",  # P&L Total
                        asset["time"]
                    ))
            except Exception as e:
                print(f"Erro ao atualizar o preço do ativo {asset['symbol']}: {e}")

        self.update_total_values()

        # Agendar a próxima atualização para daqui 5 minutos
        self.main_area.after(300000, self.update_prices)

    def update_total_values(self):
        # Recalcula o valor total e P&L total de todo o portfólio
        self.total_value = 0
        self.total_pl = 0
        for asset in self.portfolio_assets:
            try:
                # Atualiza o preço atual da ação
                stock = yf.Ticker(asset["symbol"] + ".SA")
                last_close = stock.history(period="1d")['Close'].iloc[-1]  # Obtém o preço de fechamento do último dia

                # Calcula o valor total da ação (preço atual * quantidade)
                total_value = asset["quantity"] * last_close
                self.total_value += total_value

                # Calcula o P&L total (diferença do preço de compra e preço atual * quantidade)
                price_change = last_close - asset["purchase_price"]
                total_pl = price_change * asset["quantity"]
                self.total_pl += total_pl

            except Exception as e:
                print(f"Erro ao calcular valores do ativo {asset['symbol']}: {e}")

        # Atualiza os labels do cabeçalho com o valor total e P&L total calculados
        self.total_value_label.config(text=f"Valor Total: R$ {self.total_value:.2f}")
        pl_color = "green" if self.total_pl >= 0 else "red"
        self.total_pl_label.config(text=f"P&L Total: R$ {self.total_pl:.2f}", fg=pl_color)

    def update_all_values(self):
        # Loop através dos itens na tabela e atualiza seus valores
        for item in self.asset_tree.get_children():
            symbol = self.asset_tree.item(item, "values")[0]  # Coluna do código do ativo
            self.update_asset_value(symbol, item)

    def update_asset_value(self, symbol, item):
        # Função para buscar o valor atualizado do ativo
        try:
            stock = yf.Ticker(symbol + ".SA")
            data = stock.history(period="1d")
            if not data.empty:
                latest_price = data['Close'][-1]
                self.asset_tree.set(item, "Preço Atual", f"R$ {latest_price:.2f}")
            else:
                raise ValueError(f"Sem dados para o ativo {symbol}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar os dados de {symbol}: {str(e)}")


    def on_select(self, event):
        # Função para selecionar a linha da tabela
        selected_item = self.asset_tree.focus()  # Captura o item selecionado
        if selected_item:
            self.selected_asset = self.asset_tree.item(selected_item)['values']  # Obtém os valores do item selecionado
            self.edit_button.config(state="normal")  # Habilita o botão "Editar"
            self.delete_button.config(state="normal")  # Habilita o botão "Excluir"
        else:
            self.edit_button.config(state="disabled")  # Desabilita o botão "Editar" se nada estiver selecionado
            self.delete_button.config(state="disabled")  # Desabilita o botão "Excluir"


    def delete_selected_asset(self):
        # Abre o pop-up de confirmação para excluir o ativo
        if self.selected_asset:
            answer = messagebox.askokcancel("Excluir", f"Tem certeza de que deseja excluir {self.selected_asset[1]}?")
            if answer:
                selected_item = self.asset_tree.focus()
                if selected_item:
                    self.asset_tree.delete(selected_item)  # Exclui o item da tabela
                    # Aqui também removemos o ativo da lista de ativos
                    self.portfolio_assets = [asset for asset in self.portfolio_assets if asset['symbol'] != self.selected_asset[0]]
                    self.update_total_values()  # Atualiza os valores totais após a exclusão



    def edit_selected_asset(self):
        if self.selected_asset:
            self.edit_window = tk.Toplevel()
            self.edit_window.title("Editar Ação")
            self.edit_window.geometry("300x250")

            tk.Label(self.edit_window, text="Quantidade:").pack(pady=5)
            self.edit_quantity_entry = tk.Entry(self.edit_window)
            self.edit_quantity_entry.insert(0, self.selected_asset[6])  # Quantidade
            self.edit_quantity_entry.pack(pady=5)

            tk.Label(self.edit_window, text="Preço de Compra:").pack(pady=5)
            self.edit_price_entry = tk.Entry(self.edit_window)
            self.edit_price_entry.insert(0, self.selected_asset[8])  # Preço de Compra
            self.edit_price_entry.pack(pady=5)

            tk.Label(self.edit_window, text="Data da Compra:").pack(pady=5)
            self.edit_date_entry = tk.Entry(self.edit_window)
            self.edit_date_entry.insert(0, self.selected_asset[11])  # Data da Compra (caso precise)
            self.edit_date_entry.pack(pady=5)


            btn_frame = tk.Frame(self.edit_window)
            btn_frame.pack(pady=10)
            tk.Button(btn_frame, text="Salvar", command=self.save_edited_asset).pack(side="left", padx=5)
            tk.Button(btn_frame, text="Cancelar", command=self.edit_window.destroy).pack(side="right", padx=5)


    def save_edited_asset(self):
        # Salva as alterações feitas na ação selecionada
        updated_quantity = int(self.edit_quantity_entry.get())
        updated_price = float(self.edit_price_entry.get().replace("R$", "").replace(",", "").strip())  # Remover "R$" e espaços
        updated_date = self.selected_asset[11]  # Caso você precise manter a data
        
        # Pegar o preço atual, removendo a máscara "R$" antes de converter para float
        current_price = float(self.selected_asset[3].replace("R$", "").replace(",", "").strip())

        # Atualizar o item na tabela
        selected_item = self.asset_tree.focus()
        if selected_item:
            # Atualiza a linha da tabela com os novos valores
            self.asset_tree.item(selected_item, values=(
                self.selected_asset[0],  # Código
                self.selected_asset[1],  # Nome
                self.selected_asset[2],  # Bolsa
                f"R$ {current_price:.2f}",  # Preço Atual
                self.selected_asset[4],  # Alteração no Preço
                self.selected_asset[5],  # % Alteração
                updated_quantity,  # Quantidade
                f"R$ {updated_quantity * current_price:.2f}",  # Valor Atual
                f"R$ {updated_price:.2f}",  # Preço de Compra
                self.selected_asset[9],  # P&L
                self.selected_asset[10],  # P&L Total
                updated_date  # Data da Compra
            ))

        self.edit_window.destroy()
        self.update_total_values()  # Recalcula o valor total e P&L


