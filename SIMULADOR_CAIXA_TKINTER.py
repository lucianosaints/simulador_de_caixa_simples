import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class CaixaSupermercado(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🛒 SIMULADOR CAIXA SIMPLES")
        self.geometry("1000x600")
        self.resizable(False, False)
        self.configure(bg="#f5f5f5")

        # Itens do mercado
        self.itens = {
            1: ("Arroz 5kg", 15.50),
            2: ("Feijão 1kg", 12.30),
            3: ("Macarrão", 8.90),
            4: ("Rosquinha Mabel", 6.90),
            5: ("Leite 1L", 4.50),
            6: ("Óleo 900ml", 9.20),
            7: ("Açúcar 1kg", 4.70),
            8: ("Café 500g", 12.90),
        }

        # Variáveis
        self.nome = tk.StringVar()
        self.saldo = tk.DoubleVar(value=0.0)
        self.saldo_input = tk.StringVar()
        self.total = 0.0

        self._montar_tela_inicial()

    def _montar_tela_inicial(self):
        frame = tk.Frame(self, bg="#f5f5f5")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        title = tk.Label(frame, text="💰 SIMULADOR DE CAIXA SIMPLES", font=("Segoe UI", 24, "bold"), bg="#f5f5f5")
        title.pack(pady=(0, 25))

        lbl_nome = tk.Label(frame, text="Nome do Cliente:", font=("Segoe UI", 12), bg="#f5f5f5")
        lbl_nome.pack(anchor="w")
        tk.Entry(frame, textvariable=self.nome, font=("Segoe UI", 12), width=40).pack(fill=tk.X, pady=(0, 15))

        lbl_saldo = tk.Label(frame, text="Saldo Inicial (R$):", font=("Segoe UI", 12), bg="#f5f5f5")
        lbl_saldo.pack(anchor="w")
        tk.Entry(frame, textvariable=self.saldo_input, font=("Segoe UI", 12), width=20).pack(fill=tk.X, pady=(0, 20))

        tk.Button(frame, text="Entrar no Caixa", font=("Segoe UI", 12, "bold"), bg="#4caf50", fg="white",
                  activebackground="#45a049", padx=10, pady=5, command=lambda: self._iniciar(frame)).pack(pady=10)

    def _iniciar(self, frame_inicial):
        nome = self.nome.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Informe o nome do cliente.")
            return
        try:
            s = float(self.saldo_input.get().replace(",", "."))
            if s <= 0:
                raise ValueError
        except Exception:
            messagebox.showwarning("Aviso", "Saldo inicial inválido.")
            return

        self.saldo.set(s)
        frame_inicial.destroy()
        self._montar_tela_caixa()

    def _montar_tela_caixa(self):
        container = tk.Frame(self, bg="#f5f5f5")
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Header
        header = tk.Frame(container, bg="#f5f5f5")
        header.pack(fill=tk.X, pady=(0, 10))
        tk.Label(header, text=f"Cliente: {self.nome.get()}", font=("Segoe UI", 16, "bold"), bg="#f5f5f5").pack(side=tk.LEFT)
        self.lbl_saldo = tk.Label(header, text=f"Saldo: R$ {self.saldo.get():.2f}", font=("Segoe UI", 14), bg="#f5f5f5")
        self.lbl_saldo.pack(side=tk.RIGHT)

        # Corpo
        body = tk.Frame(container, bg="#f5f5f5")
        body.pack(fill=tk.BOTH, expand=True)

        # Lado esquerdo: Produtos
        left = tk.LabelFrame(body, text="Produtos", font=("Segoe UI", 12, "bold"), bg="#f5f5f5", fg="#333")
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0,10), pady=5)
        cols = 2
        for idx, (cod, (nome, preco)) in enumerate(self.itens.items()):
            btn = tk.Button(left, text=f"{nome}\nR$ {preco:.2f}", font=("Segoe UI", 11),
                            bg="#2196f3", fg="white", activebackground="#1976d2",
                            width=20, height=2, command=lambda c=cod: self._adicionar_ao_carrinho(c))
            r, c = divmod(idx, cols)
            btn.grid(row=r, column=c, padx=5, pady=5)

        # Lado direito: Carrinho + extrato
        right = tk.Frame(body, bg="#f5f5f5")
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Carrinho
        tree_frame = tk.LabelFrame(right, text="Carrinho", font=("Segoe UI", 12, "bold"), bg="#f5f5f5", fg="#333")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0,5))

        self.tree = ttk.Treeview(tree_frame, columns=("produto", "preco"), show="headings", height=12)
        self.tree.heading("produto", text="Produto")
        self.tree.heading("preco", text="Preço (R$)")
        self.tree.column("produto", anchor="w", width=300)
        self.tree.column("preco", anchor="center", width=100)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        # Rodapé carrinho
        footer = tk.Frame(right, bg="#f5f5f5")
        footer.pack(fill=tk.X, pady=5)

        self.lbl_total = tk.Label(footer, text=f"Total: R$ {self.total:.2f}", font=("Segoe UI", 14, "bold"), bg="#f5f5f5")
        self.lbl_total.pack(side=tk.LEFT, padx=10)

        tk.Button(footer, text="Remover selecionado", font=("Segoe UI", 11), bg="#f44336", fg="white",
                  command=self._remover_item).pack(side=tk.RIGHT, padx=5)
        tk.Button(footer, text="Limpar carrinho", font=("Segoe UI", 11), bg="#ff9800", fg="white",
                  command=self._limpar_carrinho).pack(side=tk.RIGHT, padx=5)
        tk.Button(footer, text="🧾 Finalizar", font=("Segoe UI", 12, "bold"), bg="#4caf50", fg="white",
                  command=self._finalizar).pack(side=tk.RIGHT, padx=5)

    # Ações
    def _adicionar_ao_carrinho(self, codigo):
        produto, preco = self.itens[codigo]
        saldo_atual = float(self.saldo.get())
        if saldo_atual < preco:
            messagebox.showerror("Erro", f"Saldo insuficiente para comprar {produto}.")
            return
        self.saldo.set(saldo_atual - preco)
        self.total += preco
        self.tree.insert("", tk.END, values=(produto, f"{preco:.2f}"))
        self._atualizar_labels()

    def _remover_item(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Carrinho", "Nenhum item selecionado.")
            return
        for item_id in sel:
            produto, preco_str = self.tree.item(item_id, "values")
            preco = float(preco_str.replace(",", "."))
            self.saldo.set(float(self.saldo.get()) + preco)
            self.total -= preco
            self.tree.delete(item_id)
        self._atualizar_labels()

    def _limpar_carrinho(self):
        for item_id in self.tree.get_children():
            _, preco_str = self.tree.item(item_id, "values")
            preco = float(preco_str.replace(",", "."))
            self.saldo.set(float(self.saldo.get()) + preco)
            self.tree.delete(item_id)
        self.total = 0.0
        self._atualizar_labels()

    def _finalizar(self):
        # Janela de extrato/nota fiscal
        extrato_win = tk.Toplevel(self)
        extrato_win.title("🧾 Nota Fiscal / Extrato")
        extrato_win.geometry("400x500")
        extrato_win.configure(bg="#f5f5f5")

        title = tk.Label(extrato_win, text="======= NOTA FISCAL =======", font=("Segoe UI", 14, "bold"), bg="#f5f5f5")
        title.pack(pady=10)

        st = scrolledtext.ScrolledText(extrato_win, font=("Segoe UI", 12))
        st.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        st.insert(tk.END, f"Cliente: {self.nome.get()}\n\n")
        if self.tree.get_children():
            for item_id in self.tree.get_children():
                produto, preco_str = self.tree.item(item_id, "values")
                st.insert(tk.END, f"{produto} - R$ {preco_str}\n")
        else:
            st.insert(tk.END, "Nenhuma compra realizada.\n")
        st.insert(tk.END, f"\nTotal gasto: R$ {self.total:.2f}\n")
        st.insert(tk.END, f"Saldo final: R$ {float(self.saldo.get()):.2f}\n")
        st.insert(tk.END, "==============================\n")
        st.configure(state="disabled")

        tk.Button(extrato_win, text="Fechar", font=("Segoe UI", 12), bg="#2196f3", fg="white",
                  command=lambda: [extrato_win.destroy(), self.destroy()]).pack(pady=10)

    def _atualizar_labels(self):
        self.lbl_saldo.config(text=f"Saldo: R$ {float(self.saldo.get()):.2f}")
        self.lbl_total.config(text=f"Total: R$ {self.total:.2f}")


if __name__ == "__main__":
    app = CaixaSupermercado()
    app.mainloop()
