import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yfinance as yf
from datetime import datetime
import pandas as pd

class AnaliseGeralScreen:
    def __init__(self, main_area):
        self.main_area = main_area
        self.setup_header()
        self.setup_main_area()

    def setup_header(self):
        total_valor_carteira = 100000  # Valor fictício
        total_pl = 5000  # Valor fictício
        header_frame = tk.Frame(self.main_area, bg="lightgray", height=80)
        header_frame.pack(fill="x")

        valor_cor = "green" if total_valor_carteira >= 0 else "red"
        pl_cor = "green" if total_pl >= 0 else "red"
        valor_simbolo = "+" if total_valor_carteira >= 0 else "-"
        pl_simbolo = "+" if total_pl >= 0 else "-"

        tk.Label(header_frame, text=f"Valor Total da Carteira: {valor_simbolo} R$ {total_valor_carteira:,.2f}", font=("Arial", 18), bg="lightgray", fg=valor_cor).pack(side="left", padx=20)
        tk.Label(header_frame, text=f"P&L Total: {pl_simbolo} R$ {total_pl:,.2f}", font=("Arial", 18), bg="lightgray", fg=pl_cor).pack(side="right", padx=20)

    def setup_main_area(self):
        table_frame = tk.Frame(self.main_area)
        table_frame.pack(pady=20, padx=20, fill="both", expand=True)

        btn_frame = tk.Frame(table_frame)
        btn_frame.pack(fill="x", padx=10, pady=5)
        tk.Button(btn_frame, text="Adicionar Ativo Manualmente", command=self.add_asset_popup).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Importar Ativos", command=self.show_import_popup).pack(side="right", padx=5)

        # Tabela com as novas colunas
        self.asset_tree = ttk.Treeview(table_frame, columns=("Código", "Nome", "Data", "Open", "High", "Low", "Close", "Volume", "Dividends", "Stock Splits", "Hora", "Observações"), show="headings")
        self.asset_tree.heading("Código", text="Código")
        self.asset_tree.heading("Nome", text="Nome da Ação")
        self.asset_tree.heading("Data", text="Data")
        self.asset_tree.heading("Open", text="Abertura")
        self.asset_tree.heading("High", text="Alta")
        self.asset_tree.heading("Low", text="Baixa")
        self.asset_tree.heading("Close", text="Fechamento")
        self.asset_tree.heading("Volume", text="Volume")
        self.asset_tree.heading("Dividends", text="Dividendos")
        self.asset_tree.heading("Stock Splits", text="Stock Splits")
        self.asset_tree.heading("Hora", text="Hora")
        self.asset_tree.heading("Observações", text="Observações")
        self.asset_tree.pack(fill="both", expand=True)

    def add_asset_popup(self):
        self.add_asset_window = tk.Toplevel()
        self.add_asset_window.title("Adicionar Ativo")
        self.add_asset_window.geometry("400x400")

        tk.Label(self.add_asset_window, text="Código do Ativo:").pack(pady=10)
        self.asset_code_entry = tk.Entry(self.add_asset_window)
        self.asset_code_entry.pack(pady=5)

        tk.Button(self.add_asset_window, text="Buscar Dados", command=self.fetch_asset_data).pack(pady=10)

        tk.Label(self.add_asset_window, text="Nome da Ação:").pack(pady=10)
        self.asset_name_label = tk.Label(self.add_asset_window, text="")
        self.asset_name_label.pack(pady=5)

        tk.Label(self.add_asset_window, text="Preço Atual:").pack(pady=10)
        self.asset_price_label = tk.Label(self.add_asset_window, text="")
        self.asset_price_label.pack(pady=5)

        tk.Label(self.add_asset_window, text="Observações:").pack(pady=10)
        self.asset_obs_entry = tk.Entry(self.add_asset_window)
        self.asset_obs_entry.pack(pady=5)

        btn_frame = tk.Frame(self.add_asset_window)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Adicionar", command=self.confirm_add_asset).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cancelar", command=self.add_asset_window.destroy).pack(side="right", padx=10)

    def fetch_asset_data(self):
        symbol = self.asset_code_entry.get().upper() + ".SA"
        try:
            stock = yf.Ticker(symbol)
            # Buscar o histórico da ação com base no último dia útil
            data = stock.history(period="1d")  # Obtém os dados do último dia útil

            if not data.empty:
                # Pega as informações do último dia
                last_day = data.iloc[-1]
                date_str = last_day.name.strftime("%Y-%m-%d")  # Converte o índice para string
                open_price = last_day['Open']
                high_price = last_day['High']
                low_price = last_day['Low']
                close_price = last_day['Close']
                volume = last_day['Volume']
                dividends = last_day['Dividends']
                stock_splits = last_day['Stock Splits']

                # Preenche os labels e guarda os dados
                self.asset_data = {
                    "symbol": symbol,
                    "name": stock.info.get('longName', symbol),
                    "date": date_str,
                    "open": open_price,
                    "high": high_price,
                    "low": low_price,
                    "close": close_price,
                    "volume": volume,
                    "dividends": dividends,
                    "stock_splits": stock_splits,
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "observations": self.asset_obs_entry.get()
                }

                # Atualiza os labels com as informações da ação
                self.asset_name_label.config(text=self.asset_data['name'])
                self.asset_price_label.config(text=f"R$ {close_price:.2f}")
            else:
                raise ValueError(f"Dados não disponíveis para o ativo {symbol}.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar dados para {symbol}: {str(e)}")

    def confirm_add_asset(self):
        if self.asset_name_label['text'] != "":
            self.asset_tree.insert("", "end", values=(
                self.asset_code_entry.get().upper(),
                self.asset_name_label['text'],
                self.asset_data['date'],
                f"R$ {self.asset_data['open']:.2f}",
                f"R$ {self.asset_data['high']:.2f}",
                f"R$ {self.asset_data['low']:.2f}",
                f"R$ {self.asset_data['close']:.2f}",
                self.asset_data['volume'],
                self.asset_data['dividends'],
                self.asset_data['stock_splits'],
                self.asset_data['time'],
                self.asset_data['observations']
            ))
            self.add_asset_window.destroy()
        else:
            messagebox.showerror("Erro", "Por favor, busque os dados do ativo antes de adicionar.")

    def show_import_popup(self):
        self.import_window = tk.Toplevel()
        self.import_window.title("Importar Ativos")
        self.import_window.geometry("400x200")

        tk.Label(self.import_window, text="Escolha uma opção:", font=("Arial", 14)).pack(pady=20)
        tk.Button(self.import_window, text="Baixar Template", command=self.download_template).pack(pady=10)
        tk.Button(self.import_window, text="Fazer Upload", command=self.upload_assets).pack(pady=10)

    def download_template(self):
        template_data = {'Código': ['MGLU3', 'PETR4', 'VALE3']}
        df = pd.DataFrame(template_data)
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Download Completo", "Template baixado com sucesso.")

    def upload_assets(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            df = pd.read_excel(file_path)
            imported_count = 0
            for _, row in df.iterrows():
                symbol = row['Código'].upper() + ".SA"
                self.asset_code_entry.delete(0, tk.END)
                self.asset_code_entry.insert(0, row['Código'].upper())  # Apenas o código sem o sufixo .SA
                self.fetch_asset_data()
                if self.asset_name_label['text'] != "":
                    self.confirm_add_asset()
                    imported_count += 1
            messagebox.showinfo("Importação Completa", f"{imported_count} ativos foram importados com sucesso.")
            self.import_window.destroy()
