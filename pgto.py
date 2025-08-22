import tkinter as tk
from tkinter import ttk

# Serviços e preços base
servicos = {
    "Consulta": 120.00,
    "Vacinação": 80.00,
    "Internação (diária)": 200.00,
    "Cirurgia": 1500.00
}

# Formas de pagamento
formas_pagamento = ["Dinheiro", "Cartão de Crédito", "Cartão de Débito", "PIX", "Boleto"]

def abrir_janela_pagamento(master):
    janela = tk.Toplevel(master)
    janela.title("Tabela de Preços e Pagamentos")

    frame_precos = ttk.LabelFrame(janela, text="Tabela de Preços")
    frame_precos.pack(fill="both", padx=10, pady=5)

    tree = ttk.Treeview(frame_precos, columns=("Serviço", "Preço"), show="headings")
    tree.pack(fill="both", expand=True)

    tree.heading("Serviço", text="Serviço")
    tree.heading("Preço", text="Preço (R$)")
    tree.column("Serviço", width=200, anchor="w")
    tree.column("Preço", width=100, anchor="center")


    for servico, preco in servicos.items():
        tree.insert("", "end", values=(servico, f"{preco:.2f}"))

    frame_pagamento = ttk.LabelFrame(janela, text="Formas de Pagamento")
    frame_pagamento.pack(fill="both", padx=10, pady=5)

    for forma in formas_pagamento:
        ttk.Label(frame_pagamento, text=f"- {forma}").pack(anchor="w", padx=10)
    ttk.Button(janela, text="Fechar", command=janela.destroy).pack(pady=10)