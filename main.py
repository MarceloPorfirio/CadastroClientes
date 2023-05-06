import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Cria uma conexão com o banco de dados
conn = sqlite3.connect('clientes.db')

# Cria a tabela "clientes"
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        telefone TEXT NOT NULL
    )
""")
conn.commit()

# Cria uma janela
janela = tk.Tk()
janela.title('Cadastro de Clientes')

# Define os rótulos e campos de entrada
tk.Label(janela, text='Nome').grid(row=0, column=0)
nome_entry = tk.Entry(janela)
nome_entry.grid(row=0, column=1)

tk.Label(janela, text='Email').grid(row=1, column=0)
email_entry = tk.Entry(janela)
email_entry.grid(row=1, column=1)

tk.Label(janela, text='Telefone').grid(row=2, column=0)
telefone_entry = tk.Entry(janela)
telefone_entry.grid(row=2, column=1)




# Define a função de inserção no banco de dados
def inserir():
    nome = nome_entry.get()
    email = email_entry.get()
    telefone = telefone_entry.get()
    
    # Executa o comando SQL para inserir os dados
    cursor = conn.cursor()
    sql = "INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)"
    cursor.execute(sql, (nome, email, telefone))
    conn.commit()
    
    # Limpa os campos de entrada após a inserção
    nome_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    telefone_entry.delete(0, tk.END)
    
    # Exibe uma mensagem de sucesso
    messagebox.showinfo('Sucesso', 'Cadastro realizado com sucesso!')

# Cria o botão de cadastro
cadastro_button = tk.Button(janela, text='Cadastrar', command=inserir)
cadastro_button.grid(row=3, column=1)

def selecionar_usuarios():
    global tv
    
    # Executa o comando SQL para selecionar todos os usuários
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    usuarios = cursor.fetchall()
    
    # Cria uma nova janela com uma TreeView para exibir os usuários selecionados
    usuarios_janela = tk.Toplevel()
    usuarios_janela.title('Usuários cadastrados')
    tv = ttk.Treeview(usuarios_janela, columns=(1, 2, 3, 4), show='headings')
    tv.heading(1, text='ID')
    tv.heading(2, text='Nome')
    tv.heading(3, text='E-mail')
    tv.heading(4, text='Telefone')
    tv.pack()
    
    # Preenche a TreeView com os usuários selecionados
    for usuario in usuarios:
        tv.insert('', 'end', values=usuario)

selecionar_button = tk.Button(janela, text='Selecionar usuários', command=selecionar_usuarios)
selecionar_button.grid(row=4,column=1)




# Inicia a janela
janela.mainloop()
