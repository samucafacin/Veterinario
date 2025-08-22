import tkinter as tk
from tkinter import ttk, messagebox
import pgto  
import pgto as pgto_module  
from psycopg2 import sql
import psycopg2

# Conectar ao PostgreSQL como superusuário
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="",
    host="localhost",
    port="5432"
)
conn.autocommit = True
cursor = conn.cursor()

# Criar o banco de dados
#cursor.execute("DROP DATABASE IF EXISTS clinica_veterinaria;")
#cursor.execute("CREATE DATABASE clinica_veterinaria;")
print("Banco 'clinica_veterinaria' criado com sucesso!")

cursor.close()
conn.close()


# Conectar ao PostgreSQL como superusuário (ex: postgres)
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="",
    host="localhost",
    port="5432"
)
conn.autocommit = True
cursor = conn.cursor()
# Conectar ao banco recém-criado
conn = psycopg2.connect(
    dbname="clinica_veterinaria",
    user="postgres",
    password="",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Tabela de clientes
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(100),
    endereco TEXT
);
""")

# Tabela de animais
cursor.execute("""
CREATE TABLE IF NOT EXISTS animais (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    especie VARCHAR(50),
    raca VARCHAR(50),
    idade INTEGER,
    cliente_id INTEGER REFERENCES clientes(id) ON DELETE CASCADE
);
""")

# Tabela de médicos veterinários
cursor.execute("""
CREATE TABLE IF NOT EXISTS medicos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    crmvet VARCHAR(50) UNIQUE
);
""")

# Tabela de procedimentos
cursor.execute("""
CREATE TABLE IF NOT EXISTS procedimentos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco NUMERIC(10,2)
);
""")

# Tabela de consultas
cursor.execute("""
CREATE TABLE IF NOT EXISTS consultas (
    id SERIAL PRIMARY KEY,
    animal_id INTEGER REFERENCES animais(id) ON DELETE CASCADE,
    medico_id INTEGER REFERENCES medicos(id),
    procedimento_id INTEGER REFERENCES procedimentos(id),
    data_consulta TIMESTAMP NOT NULL,
    observacoes TEXT
);
""")

conn.commit()
print("Tabelas criadas com sucesso!")

cursor.close()
conn.close()
def inserir_cliente(nome, telefone, email, endereco):
    conn = psycopg2.connect(dbname="clinica_veterinaria", user="postgres", password=" ", host="localhost")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (nome, telefone, email, endereco) VALUES (%s, %s, %s, %s)",
                   (nome, telefone, email, endereco))
    conn.commit()
    cursor.close()
    conn.close()
    print("Cliente inserido com sucesso!")

def listar_clientes():
    conn = psycopg2.connect(dbname="clinica_veterinaria", user="postgres", password=" ", host="localhost")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    for cliente in cursor.fetchall():
        print(cliente)
    cursor.close()
    conn.close()




# ======== Classes de Domínio ========

class Animal:
    def __init__(self, nome, idade, especie):
        self._nome = nome
        self._idade = idade
        self._especie = especie

    def emitir_som(self):
        return "Som genérico"

    def __str__(self):
        return f"{self.__class__.__name__} - {self._nome} ({self._idade} anos)"


class Cachorro(Animal):
    def emitir_som(self):
        return "🐶 Au Au!"


class Gato(Animal):
    def emitir_som(self):
        return "🐱 Miau!"


class Passaro(Animal):
    def emitir_som(self):
        return "🐦 Piu Piu!"


class Cliente:
    def __init__(self, nome, telefone):
        self.nome = nome
        self.telefone = telefone
        self.animais = []

    def adicionar_animal(self, animal):
        self.animais.append(animal)

    def __str__(self):
        return f"{self.nome} ({self.telefone})"


class Consulta:
    def __init__(self, animal, data, motivo):
        self.animal = animal
        self.data = data
        self.motivo = motivo

    def __str__(self):
        return f"{self.animal._nome} em {self.data} | {self.motivo}"


class ClinicaVeterinaria:
    def __init__(self, nome):
        self.nome = nome
        self.clientes = []
        self.consultas = []
        self.veterinarios = []
        self.diagnosticos = []  
        self.internacoes = []   
        self.cirurgias = [] 
        self.pagamentos = []   

    def cadastrar_cliente(self, cliente):
        self.clientes.append(cliente)

    def agendar_consulta(self, consulta):
        self.consultas.append(consulta)

    def cadastrar_veterinario(self, veterinario):
        self.veterinarios.append(veterinario)

    def adicionar_diagnostico(self, animal, descricao):
        self.diagnosticos.append((animal, descricao))

    def adicionar_internacao(self, animal, dias):
        self.internacoes.append((animal, dias))

    def adicionar_cirurgia(self, animal, tipo):
        self.cirurgias.append((animal, tipo))

    def registrar_pagamento(self, cliente, servico, valor, forma):
        self.pagamentos.append((cliente, servico, valor, forma))    


# ======== Interface Tkinter ========

class App:
    def __init__(self, root):
        self.clinica = ClinicaVeterinaria("🐾 Clínica Pet Feliz 🐾")

        self.root = root
        self.root.title(self.clinica.nome)
        self.root.geometry("990x640")

        # ===== Estilo =====
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#fdf6e3", foreground="black", rowheight=25, fieldbackground="#fdf6e3")
        style.map("Treeview", background=[("selected", "#ffcc80")])

        # Notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Abas
        self.frame_clientes = ttk.Frame(self.notebook)
        self.frame_animais = ttk.Frame(self.notebook)
        self.frame_consultas = ttk.Frame(self.notebook)
        self.frame_veterinario = ttk.Frame(self.notebook)
        self.frame_diagnosticos = ttk.Frame(self.notebook)
        self.frame_internacoes = ttk.Frame(self.notebook)
        self.frame_cirurgias = ttk.Frame(self.notebook)
        self.frame_pagamentos = ttk.Frame(self.notebook)

        self.notebook.add(self.frame_clientes, text="👤 Clientes")
        self.notebook.add(self.frame_animais, text="🐾 Animais")
        self.notebook.add(self.frame_consultas, text="📅 Consultas")
        self.notebook.add(self.frame_veterinario, text="👨‍⚕️ Veterinário")
        self.notebook.add(self.frame_diagnosticos, text="🩺 Diagnósticos")
        self.notebook.add(self.frame_internacoes, text="🏥 Internações")
        self.notebook.add(self.frame_cirurgias, text="🔪 Cirurgias")
        self.notebook.add(self.frame_pagamentos, text="💰 Pagamentos")

        # Montar telas
        self._montar_clientes()
        self._montar_animais()
        self._montar_consultas()
        self._montar_veterinario()
        self._montar_diagnosticos()
        self._montar_internacoes()
        self._montar_cirurgias()
        self._montar_pagamentos()   

        # Botão Relatório Geral
        ttk.Button(self.root, text="📋 Relatório Geral", command=self.mostrar_relatorio).pack(pady=(0, 8))

    # ====== CLIENTES ======
    def _montar_clientes(self):
        frm = ttk.Frame(self.frame_clientes, padding=10)
        frm.pack(fill="x")

        ttk.Label(frm, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nome_cliente = ttk.Entry(frm, width=28)
        self.entry_nome_cliente.grid(row=0, column=1, padx=5)

        ttk.Label(frm, text="Telefone:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_tel_cliente = ttk.Entry(frm, width=20)
        self.entry_tel_cliente.grid(row=0, column=3, padx=5)

        ttk.Button(frm, text="➕ Adicionar Cliente", command=self.cadastrar_cliente).grid(row=0, column=4, padx=5)

        self.tree_clientes = ttk.Treeview(self.frame_clientes, columns=("Nome", "Telefone"), show="headings", height=12)
        self.tree_clientes.heading("Nome", text="Nome")
        self.tree_clientes.heading("Telefone", text="Telefone")
        self.tree_clientes.pack(fill="both", expand=True, pady=10)

    def cadastrar_cliente(self):
        nome = self.entry_nome_cliente.get().strip()
        telefone = self.entry_tel_cliente.get().strip()
        if nome and telefone:
            cliente = Cliente(nome, telefone)
            self.clinica.cadastrar_cliente(cliente)
            self.tree_clientes.insert("", tk.END, values=(cliente.nome, cliente.telefone))
            self.entry_nome_cliente.delete(0, tk.END)
            self.entry_tel_cliente.delete(0, tk.END)
            self._atualizar_comboboxes()
        else:
            messagebox.showwarning("Erro", "Preencha todos os campos!")

    # ====== ANIMAIS ======
    def _montar_animais(self):
        frm = ttk.Frame(self.frame_animais, padding=10)
        frm.pack(fill="x")

        ttk.Label(frm, text="Cliente:").grid(row=0, column=0, padx=5)
        self.combo_clientes = ttk.Combobox(frm, values=[], width=28, state="readonly")
        self.combo_clientes.grid(row=0, column=1, padx=5)

        ttk.Label(frm, text="Nome do Pet:").grid(row=0, column=2, padx=5)
        self.entry_nome_animal = ttk.Entry(frm, width=20)
        self.entry_nome_animal.grid(row=0, column=3, padx=5)

        ttk.Label(frm, text="Idade:").grid(row=0, column=4, padx=5)
        self.entry_idade_animal = ttk.Entry(frm, width=6)
        self.entry_idade_animal.grid(row=0, column=5, padx=5)

        ttk.Label(frm, text="Tipo:").grid(row=0, column=6, padx=5)
        self.combo_tipo = ttk.Combobox(frm, values=["Cachorro 🐶", "Gato 🐱", "Pássaro 🐦"], width=16, state="readonly")
        self.combo_tipo.grid(row=0, column=7, padx=5)

        ttk.Button(frm, text="➕ Adicionar Pet", command=self.adicionar_animal).grid(row=0, column=8, padx=5)

        self.tree_animais = ttk.Treeview(self.frame_animais, columns=("Cliente", "Animal", "Idade", "Tipo"), show="headings", height=12)
        for col in ("Cliente", "Animal", "Idade", "Tipo"):
            self.tree_animais.heading(col, text=col)
        self.tree_animais.pack(fill="both", expand=True, pady=10)

    def adicionar_animal(self):
        nome_cliente = self.combo_clientes.get()
        cliente = next((c for c in self.clinica.clientes if str(c) == nome_cliente), None)
        if not cliente:
            messagebox.showwarning("Erro", "Selecione um cliente válido!")
            return

        nome_animal = self.entry_nome_animal.get().strip()
        idade_txt = self.entry_idade_animal.get().strip()
        tipo_sel = self.combo_tipo.get().strip()

        if not (nome_animal and idade_txt and tipo_sel):
            messagebox.showwarning("Erro", "Preencha todos os campos!")
            return

        try:
            idade = int(idade_txt)
        except ValueError:
            messagebox.showwarning("Erro", "Idade deve ser número!")
            return

        if "Cachorro" in tipo_sel:
            animal = Cachorro(nome_animal, idade, "Cachorro")
        elif "Gato" in tipo_sel:
            animal = Gato(nome_animal, idade, "Gato")
        else:
            animal = Passaro(nome_animal, idade, "Pássaro")

        cliente.adicionar_animal(animal)
        self.tree_animais.insert("", tk.END, values=(cliente.nome, animal._nome, animal._idade, tipo_sel))
        self.entry_nome_animal.delete(0, tk.END)
        self.entry_idade_animal.delete(0, tk.END)

        # Atualiza combos de animais quando algum cliente for selecionado
        self._sincronizar_animais_em_abas()

    # ====== CONSULTAS ======
    def _montar_consultas(self):
        frm = ttk.Frame(self.frame_consultas, padding=10)
        frm.pack(fill="x")

        ttk.Label(frm, text="Cliente:").grid(row=0, column=0, padx=5)
        self.combo_consulta_cliente = ttk.Combobox(frm, values=[], width=28, state="readonly")
        self.combo_consulta_cliente.grid(row=0, column=1, padx=5)
        self.combo_consulta_cliente.bind("<<ComboboxSelected>>", self._atualizar_animais_consulta)

        ttk.Label(frm, text="Animal:").grid(row=0, column=2, padx=5)
        self.combo_consulta_animal = ttk.Combobox(frm, values=[], width=20, state="readonly")
        self.combo_consulta_animal.grid(row=0, column=3, padx=5)

        ttk.Label(frm, text="Data:").grid(row=0, column=4, padx=5)
        self.entry_data = ttk.Entry(frm, width=12)
        self.entry_data.grid(row=0, column=5, padx=5)

        ttk.Label(frm, text="Motivo:").grid(row=0, column=6, padx=5)
        self.entry_motivo = ttk.Entry(frm, width=22)
        self.entry_motivo.grid(row=0, column=7, padx=5)

        ttk.Button(frm, text="📅 Agendar Consulta", command=self.agendar_consulta).grid(row=0, column=8, padx=5)

        self.tree_consultas = ttk.Treeview(self.frame_consultas, columns=("Cliente", "Animal", "Data", "Motivo"), show="headings", height=12)
        for col in ("Cliente", "Animal", "Data", "Motivo"):
            self.tree_consultas.heading(col, text=col)
        self.tree_consultas.pack(fill="both", expand=True, pady=10)

    def agendar_consulta(self):
        nome_cliente = self.combo_consulta_cliente.get()
        cliente = next((c for c in self.clinica.clientes if str(c) == nome_cliente), None)
        if not cliente:
            messagebox.showwarning("Erro", "Selecione um cliente!")
            return

        nome_animal = self.combo_consulta_animal.get()
        animal = next((a for a in cliente.animais if a._nome == nome_animal), None)
        if not animal:
            messagebox.showwarning("Erro", "Selecione um animal válido!")
            return

        data = self.entry_data.get().strip()
        motivo = self.entry_motivo.get().strip()
        if not (data and motivo):
            messagebox.showwarning("Erro", "Preencha todos os campos!")
            return

        consulta = Consulta(animal, data, motivo)
        self.clinica.agendar_consulta(consulta)
        self.tree_consultas.insert("", tk.END, values=(cliente.nome, animal._nome, data, motivo))
        self.entry_data.delete(0, tk.END)
        self.entry_motivo.delete(0, tk.END)

    # ====== VETERINÁRIO ======
    def _montar_veterinario(self):
        frm = ttk.Frame(self.frame_veterinario, padding=10)
        frm.pack(fill="x")

        ttk.Label(frm, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nome_veterinario = ttk.Entry(frm, width=28)
        self.entry_nome_veterinario.grid(row=0, column=1, padx=5)

        ttk.Label(frm, text="Telefone:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_tel_veterinario = ttk.Entry(frm, width=20)
        self.entry_tel_veterinario.grid(row=0, column=3, padx=5)

        ttk.Button(frm, text="➕ Adicionar Veterinário", command=self.cadastrar_veterinario).grid(row=0, column=4, padx=5)

        self.tree_veterinario = ttk.Treeview(self.frame_veterinario, columns=("Nome", "Telefone"), show="headings", height=12)
        self.tree_veterinario.heading("Nome", text="Nome")
        self.tree_veterinario.heading("Telefone", text="Telefone")
        self.tree_veterinario.pack(fill="both", expand=True, pady=10)

    def cadastrar_veterinario(self):
        nome = self.entry_nome_veterinario.get().strip()
        telefone = self.entry_tel_veterinario.get().strip()
        if nome and telefone:
            # Reutilizando a estrutura simples (nome, telefone)
            vet = Cliente(nome, telefone)
            self.clinica.cadastrar_veterinario(vet)
            self.tree_veterinario.insert("", tk.END, values=(vet.nome, vet.telefone))
            self.entry_nome_veterinario.delete(0, tk.END)
            self.entry_tel_veterinario.delete(0, tk.END)
        else:
            messagebox.showwarning("Erro", "Preencha todos os campos!")

    # ====== DIAGNÓSTICOS ======
    def _montar_diagnosticos(self):
        frm = ttk.Frame(self.frame_diagnosticos, padding=10)
        frm.pack(fill="x")

        ttk.Label(frm, text="Cliente:").grid(row=0, column=0, padx=5, pady=5)
        self.combo_diag_cliente = ttk.Combobox(frm, values=[], width=28, state="readonly")
        self.combo_diag_cliente.grid(row=0, column=1, padx=5)
        self.combo_diag_cliente.bind("<<ComboboxSelected>>", self._atualizar_animais_diag)

        ttk.Label(frm, text="Animal:").grid(row=0, column=2, padx=5, pady=5)
        self.combo_diag_animal = ttk.Combobox(frm, values=[], width=20, state="readonly")
        self.combo_diag_animal.grid(row=0, column=3, padx=5)

        ttk.Label(frm, text="Descrição:").grid(row=0, column=4, padx=5, pady=5)
        self.entry_diag = ttk.Entry(frm, width=30)
        self.entry_diag.grid(row=0, column=5, padx=5)

        ttk.Button(frm, text="➕ Adicionar", command=self.add_diagnostico).grid(row=0, column=6, padx=5)

        self.tree_diag = ttk.Treeview(self.frame_diagnosticos, columns=("Cliente", "Animal", "Descrição"), show="headings", height=12)
        for col in ("Cliente", "Animal", "Descrição"):
            self.tree_diag.heading(col, text=col)
        self.tree_diag.pack(fill="both", expand=True, pady=10)

    def add_diagnostico(self):
        nome_cliente = self.combo_diag_cliente.get()
        cliente = next((c for c in self.clinica.clientes if str(c) == nome_cliente), None)
        if not cliente:
            messagebox.showwarning("Erro", "Selecione um cliente!")
            return

        nome_animal = self.combo_diag_animal.get()
        animal = next((a for a in cliente.animais if a._nome == nome_animal), None)
        if not animal:
            messagebox.showwarning("Erro", "Selecione um Pet!")
            return

        desc = self.entry_diag.get().strip()
        if not desc:
            messagebox.showwarning("Erro", "Informe a descrição.")
            return

        self.clinica.adicionar_diagnostico(animal, desc)
        self.tree_diag.insert("", tk.END, values=(cliente.nome, animal._nome, desc))
        self.entry_diag.delete(0, tk.END)

    # ====== INTERNAÇÕES ======
    def _montar_internacoes(self):
        frm = ttk.Frame(self.frame_internacoes, padding=10)
        frm.pack(fill="x")

        ttk.Label(frm, text="Cliente:").grid(row=0, column=0, padx=5, pady=5)
        self.combo_intern_cliente = ttk.Combobox(frm, values=[], width=28, state="readonly")
        self.combo_intern_cliente.grid(row=0, column=1, padx=5)
        self.combo_intern_cliente.bind("<<ComboboxSelected>>", self._atualizar_animais_intern)

        ttk.Label(frm, text="Animal:").grid(row=0, column=2, padx=5, pady=5)
        self.combo_intern_animal = ttk.Combobox(frm, values=[], width=20, state="readonly")
        self.combo_intern_animal.grid(row=0, column=3, padx=5)

        ttk.Label(frm, text="Dias:").grid(row=0, column=4, padx=5, pady=5)
        self.entry_internacao = ttk.Entry(frm, width=10)
        self.entry_internacao.grid(row=0, column=5, padx=5)

        ttk.Button(frm, text="➕ Adicionar", command=self.add_internacao).grid(row=0, column=6, padx=5)

        self.tree_intern = ttk.Treeview(self.frame_internacoes, columns=("Cliente", "Animal", "Dias"), show="headings", height=12)
        for col in ("Cliente", "Animal", "Dias"):
            self.tree_intern.heading(col, text=col)
        self.tree_intern.pack(fill="both", expand=True, pady=10)

    def add_internacao(self):
        nome_cliente = self.combo_intern_cliente.get()
        cliente = next((c for c in self.clinica.clientes if str(c) == nome_cliente), None)
        if not cliente:
            messagebox.showwarning("Erro", "Selecione um cliente!")
            return

        nome_animal = self.combo_intern_animal.get()
        animal = next((a for a in cliente.animais if a._nome == nome_animal), None)
        if not animal:
            messagebox.showwarning("Erro", "Selecione um animal!")
            return

        dias_txt = self.entry_internacao.get().strip()
        if not dias_txt:
            messagebox.showwarning("Erro", "Informe os dias.")
            return

        try:
            dias = int(dias_txt)
        except ValueError:
            messagebox.showwarning("Erro", "Dias deve ser número!")
            return

        self.clinica.adicionar_internacao(animal, dias)
        self.tree_intern.insert("", tk.END, values=(cliente.nome, animal._nome, dias))
        self.entry_internacao.delete(0, tk.END)

    # ====== CIRURGIAS ======
    def _montar_cirurgias(self):
        frm = ttk.Frame(self.frame_cirurgias, padding=10)
        frm.pack(fill="x")

        ttk.Label(frm, text="Cliente:").grid(row=0, column=0, padx=5, pady=5)
        self.combo_cir_cliente = ttk.Combobox(frm, values=[], width=28, state="readonly")
        self.combo_cir_cliente.grid(row=0, column=1, padx=5)
        self.combo_cir_cliente.bind("<<ComboboxSelected>>", self._atualizar_animais_cir)

        ttk.Label(frm, text="Animal:").grid(row=0, column=2, padx=5, pady=5)
        self.combo_cir_animal = ttk.Combobox(frm, values=[], width=20, state="readonly")
        self.combo_cir_animal.grid(row=0, column=3, padx=5)

        ttk.Label(frm, text="Tipo:").grid(row=0, column=4, padx=5, pady=5)
        self.entry_cirurgia = ttk.Entry(frm, width=30)
        self.entry_cirurgia.grid(row=0, column=5, padx=5)

        ttk.Button(frm, text="➕ Adicionar", command=self.add_cirurgia).grid(row=0, column=6, padx=5)

        self.tree_cirurgia = ttk.Treeview(self.frame_cirurgias, columns=("Cliente", "Animal", "Tipo"), show="headings", height=12)
        for col in ("Cliente", "Animal", "Tipo"):
            self.tree_cirurgia.heading(col, text=col)
        self.tree_cirurgia.pack(fill="both", expand=True, pady=10)

    def add_cirurgia(self):
        nome_cliente = self.combo_cir_cliente.get()
        cliente = next((c for c in self.clinica.clientes if str(c) == nome_cliente), None)
        if not cliente:
            messagebox.showwarning("Erro", "Selecione um cliente!")
            return

        nome_animal = self.combo_cir_animal.get()
        animal = next((a for a in cliente.animais if a._nome == nome_animal), None)
        if not animal:
            messagebox.showwarning("Erro", "Selecione um animal!")
            return

        tipo = self.entry_cirurgia.get().strip()
        if not tipo:
            messagebox.showwarning("Erro", "Informe o tipo.")
            return

        self.clinica.adicionar_cirurgia(animal, tipo)
        self.tree_cirurgia.insert("", tk.END, values=(cliente.nome, animal._nome, tipo))
        self.entry_cirurgia.delete(0, tk.END)
    # ====== PAGAMENTOS ======
    def _montar_pagamentos(self):
        frm = ttk.Frame(self.frame_pagamentos, padding=10)
        frm.pack(fill="x")

        ttk.Label(frm, text="Cliente:").grid(row=0, column=0, padx=5, pady=5)
        self.combo_pgto_cliente = ttk.Combobox(frm, values=[], width=28, state="readonly")
        self.combo_pgto_cliente.grid(row=0, column=1, padx=5)

        ttk.Label(frm, text="Serviço:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_servico = ttk.Entry(frm, width=20)
        self.entry_servico.grid(row=0, column=3, padx=5)

        tk.Label(frm, text="Valor:").grid(row=0, column=4, padx=5, pady=5)
        self.entry_valor = ttk.Entry(frm, width=10)
        self.entry_valor.grid(row=0, column=5, padx=5)

        ttk.Label(frm, text="Forma de Pagamento:").grid(row=0, column=6, padx=5, pady=5)
        self.combo_forma_pgto = ttk.Combobox(frm, values=["Dinheiro", "Cartão", "Pix"], width=15, state="readonly")
        self.combo_forma_pgto.grid(row=0, column=7, padx=5)

        ttk.Button(frm, text="💰 Registrar Pagamento", command=self.registrar_pagamento).grid(row=0, column=8, padx=5)

    # === Treeview de Pagamentos registrados ===
        self.tree_pagamentos = ttk.Treeview(
        self.frame_pagamentos,
        columns=("Cliente", "Serviço", "Valor", "Forma"),
        show="headings",
        height=6
    )
        for col in ("Cliente", "Serviço", "Valor", "Forma"):
            self.tree_pagamentos.heading(col, text=col)
        self.tree_pagamentos.column(col, width=120, anchor="center")
        self.tree_pagamentos.pack(fill="both", expand=True, pady=10)

    # === Treeview da Tabela de Preços ===
        frame_precos = ttk.LabelFrame(self.frame_pagamentos, text="Tabela de Preços")
        frame_precos.pack(fill="both", padx=10, pady=5)

        self.tree_precos = ttk.Treeview(
        frame_precos,
        columns=("Serviço", "Preço"),
        show="headings",
        height=6
    )
        self.tree_precos.heading("Serviço", text="Serviço")
        self.tree_precos.heading("Preço", text="Preço (R$)")
        self.tree_precos.column("Serviço", width=200, anchor="w")
        self.tree_precos.column("Preço", width=100, anchor="center")
        self.tree_precos.pack(fill="both", expand=True, pady=5)

    # Inserindo os serviços fixos
        for servico, preco in {
        "Consulta": 120.00,
        "Vacinação": 80.00,
        "Internação (diária)": 200.00,
        "Cirurgia": 1500.00
    }   .items():
        
        
         self.tree_precos.insert("", "end", values=(servico, f"{preco:.2f}"))
 

    # ====== SUPORTE: Atualizações de Combos ======
    def _atualizar_comboboxes(self):
        clientes_formatados = [str(c) for c in self.clinica.clientes]
        if hasattr(self, "combo_clientes"):
            self.combo_clientes["values"] = clientes_formatados
        if hasattr(self, "combo_consulta_cliente"):
            self.combo_consulta_cliente["values"] = clientes_formatados
        if hasattr(self, "combo_diag_cliente"):
            self.combo_diag_cliente["values"] = clientes_formatados
        if hasattr(self, "combo_intern_cliente"):
            self.combo_intern_cliente["values"] = clientes_formatados
        if hasattr(self, "combo_cir_cliente"):
            self.combo_cir_cliente["values"] = clientes_formatados
        if hasattr(self, "combo_pgto_cliente"):
            self.combo_pgto_cliente["values"] = clientes_formatados

    def _carregar_animais_por_cliente(self, combo_cliente, combo_animal):
        nome_cliente = combo_cliente.get()
        cliente = next((c for c in self.clinica.clientes if str(c) == nome_cliente), None)
        if cliente:
            combo_animal["values"] = [a._nome for a in cliente.animais]
        else:
            combo_animal["values"] = []

    def _atualizar_animais_consulta(self, event=None):
        self._carregar_animais_por_cliente(self.combo_consulta_cliente, self.combo_consulta_animal)

    def _atualizar_animais_diag(self, event=None):
        self._carregar_animais_por_cliente(self.combo_diag_cliente, self.combo_diag_animal)

    def _atualizar_animais_intern(self, event=None):
        self._carregar_animais_por_cliente(self.combo_intern_cliente, self.combo_intern_animal)

    def _atualizar_animais_cir(self, event=None):
        self._carregar_animais_por_cliente(self.combo_cir_cliente, self.combo_cir_animal)
    def registrar_pagamento(self):
        nome_cliente = self.combo_pgto_cliente.get()
        cliente = next((c for c in self.clinica.clientes if str(c) == nome_cliente), None)
        if not cliente:
            messagebox.showwarning("Erro", "Selecione um cliente!")
            return

        servico = self.entry_servico.get().strip()
        valor_txt = self.entry_valor.get().strip()
        forma = self.combo_forma_pgto.get().strip()

        if not (servico and valor_txt and forma):
            messagebox.showwarning("Erro", "Preencha todos os campos!")
            return

        try:
            valor = float(valor_txt)
        except ValueError:
            messagebox.showwarning("Erro", "Valor deve ser numérico!")
            return

        # Registra o pagamento na clínica
        self.clinica.registrar_pagamento(cliente, servico, valor, forma)

        # Adiciona ao Treeview
        self.tree_pagamentos.insert("", tk.END, values=(cliente.nome, servico, f"R$ {valor:.2f}", forma))

        # Limpa os campos
        self.entry_servico.delete(0, tk.END)
        self.entry_valor.delete(0, tk.END)
        self.combo_forma_pgto.set("")

    def _sincronizar_animais_em_abas(self):
        # Se já houver um cliente selecionado em alguma aba, recarrega a lista de animais correspondente
        if getattr(self, "combo_consulta_cliente", None) and self.combo_consulta_cliente.get():
            self._atualizar_animais_consulta()
        if getattr(self, "combo_diag_cliente", None) and self.combo_diag_cliente.get():
            self._atualizar_animais_diag()
        if getattr(self, "combo_intern_cliente", None) and self.combo_intern_cliente.get():
            self._atualizar_animais_intern()
        if getattr(self, "combo_cir_cliente", None) and self.combo_cir_cliente.get():
            self._atualizar_animais_cir()

    # ====== RELATÓRIO GERAL ======
    def mostrar_relatorio(self):
        janela = tk.Toplevel(self.root)
        janela.title("📋 Relatório Geral")
        janela.geometry("1050x520")

        tree = ttk.Treeview(
            janela,
            columns=("Tipo", "Cliente", "Animal", "Info1", "Info2"),
            show="headings",
            height=20
        )
        for col in ("Tipo", "Cliente", "Animal", "Info1", "Info2"):
            tree.heading(col, text=col)
            tree.column(col, width=180 if col == "Info2" else 160, anchor="w")
        tree.pack(fill="both", expand=True)

        # Clientes
        for c in self.clinica.clientes:
            tree.insert("", tk.END, values=("Cliente", c.nome, "-", f"Telefone: {c.telefone}", "-"))

        # Animais
        for c in self.clinica.clientes:
            for a in c.animais:
                tree.insert("", tk.END, values=("Animal", c.nome, a._nome, f"Idade: {a._idade}", f"Espécie: {a._especie}"))

        # Consultas
        for consulta in self.clinica.consultas:
            # Descobre o cliente do animal
            cli = next((c for c in self.clinica.clientes if any(a is consulta.animal for a in c.animais)), None)
            cliente_nome = cli.nome if cli else "-"
            tree.insert("", tk.END, values=("Consulta", cliente_nome, consulta.animal._nome, consulta.data, consulta.motivo))

        # Diagnósticos
        for animal, desc in self.clinica.diagnosticos:
            cli = next((c for c in self.clinica.clientes if any(a is animal for a in c.animais)), None)
            cliente_nome = cli.nome if cli else "-"
            tree.insert("", tk.END, values=("Diagnóstico", cliente_nome, animal._nome, desc, "-"))

        # Internações
        for animal, dias in self.clinica.internacoes:
            cli = next((c for c in self.clinica.clientes if any(a is animal for a in c.animais)), None)
            cliente_nome = cli.nome if cli else "-"
            tree.insert("", tk.END, values=(("Internação", cliente_nome, animal._nome, f"{dias} dia(s)", "-")))

        # Cirurgias
        for animal, tipo in self.clinica.cirurgias:
            cli = next((c for c in self.clinica.clientes if any(a is animal for a in c.animais)), None)
            cliente_nome = cli.nome if cli else "-"
            tree.insert("", tk.END, values=(("Cirurgia", cliente_nome, animal._nome, tipo, "-")))
        ttk.Button(janela, text="Fechar", command=janela.destroy).pack(pady=10)


# ======== Rodar App ========
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
