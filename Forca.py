import tkinter as tk
from tkinter import messagebox
import random
from unidecode import unidecode  # Biblioteca para remover acentos

# Função para carregar palavras de um arquivo de texto
def carregar_palavras(arquivo):
    with open(arquivo, "r", encoding="utf-8") as f:
        return [linha.strip() for linha in f.readlines()]

# Função para sortear uma palavra aleatória
def sortear_palavra():
    return random.choice(palavras)

# Função para inicializar o jogo
def iniciar_jogo():
    global palavra_secreta, palavra_secreta_normalizada, letras_corretas, tentativas_restantes, letras_tentadas
    palavra_secreta = sortear_palavra()  # Sorteia uma nova palavra
    palavra_secreta_normalizada = unidecode(palavra_secreta)  # Remove acentos da palavra
    letras_corretas = ["_"] * len(palavra_secreta_normalizada)  # Cria uma lista com underscores para cada letra
    tentativas_restantes = 6  # Número de tentativas
    letras_tentadas = set()  # Conjunto de letras já tentadas
    canvas.delete("all")  # Limpa o canvas (remove o desenho anterior)
    desenhar_forca()  # Desenha a forca
    atualizar_interface()

# Função para desenhar a forca
def desenhar_forca():
    # Desenha a base da forca
    canvas.create_line(50, 250, 150, 250, width=3)  # Base horizontal
    canvas.create_line(100, 250, 100, 50, width=3)  # Poste vertical
    canvas.create_line(100, 50, 200, 50, width=3)  # Topo horizontal
    canvas.create_line(200, 50, 200, 100, width=3)  # Corda

# Função para desenhar o corpo
def desenhar_corpo(erros):
    if erros >= 1:
        canvas.create_oval(180, 100, 220, 140, width=3)  # Cabeça
    if erros >= 2:
        canvas.create_line(200, 140, 200, 200, width=3)  # Corpo
    if erros >= 3:
        canvas.create_line(200, 160, 170, 140, width=3)  # Braço esquerdo
    if erros >= 4:
        canvas.create_line(200, 160, 230, 140, width=3)  # Braço direito
    if erros >= 5:
        canvas.create_line(200, 200, 170, 230, width=3)  # Perna esquerda
    if erros >= 6:
        canvas.create_line(200, 200, 230, 230, width=3)  # Perna direita

# Função para atualizar a interface gráfica
def atualizar_interface():
    # Exibe a palavra normalizada (sem acentos)
    label_palavra.config(text=" ".join(letras_corretas))
    label_tentativas.config(text=f"Tentativas restantes: {tentativas_restantes}")
    label_letras_tentadas.config(text=f"Letras tentadas: {', '.join(letras_tentadas)}")
    desenhar_corpo(6 - tentativas_restantes)  # Desenha o corpo com base nos erros

# Função para processar o palpite do jogador
def processar_palpite():
    palpite = entry_palpite.get().lower()
    palpite_normalizado = unidecode(palpite)  # Remove acentos do palpite
    entry_palpite.delete(0, tk.END)

    if palpite_normalizado in letras_tentadas:
        messagebox.showinfo("Aviso", "Você já tentou essa letra!")
        return

    letras_tentadas.add(palpite_normalizado)

    # Verifica se o palpite está na palavra secreta normalizada
    if palpite_normalizado in palavra_secreta_normalizada:
        for i, letra in enumerate(palavra_secreta_normalizada):
            if letra == palpite_normalizado:
                letras_corretas[i] = palavra_secreta_normalizada[i]  # Atualiza a letra correta
        if "_" not in letras_corretas:
            messagebox.showinfo("Parabéns!", "Você acertou a palavra!")
            iniciar_jogo()  # Reinicia o jogo
    else:
        global tentativas_restantes
        tentativas_restantes -= 1
        if tentativas_restantes == 0:
            atualizar_interface()
            janela.update()  # Força a atualização da interface gráfica
            messagebox.showinfo("Fim de jogo", f"Você perdeu! A palavra era: {palavra_secreta}")
            iniciar_jogo()  # Reinicia o jogo

    atualizar_interface()

# Carrega as palavras do arquivo
palavras = carregar_palavras("palavras.txt")

# Configuração da interface gráfica
janela = tk.Tk()
janela.title("Jogo da Forca")

# Canvas para desenhar a forca e o corpo
canvas = tk.Canvas(janela, width=300, height=300, bg="white")
canvas.pack()

# Label para exibir a palavra oculta (sem acentos)
label_palavra = tk.Label(janela, text="", font=("Arial", 24))
label_palavra.pack(pady=20)

# Label para exibir o número de tentativas restantes
label_tentativas = tk.Label(janela, text="", font=("Arial", 14))
label_tentativas.pack()

# Label para exibir as letras já tentadas
label_letras_tentadas = tk.Label(janela, text="", font=("Arial", 14))
label_letras_tentadas.pack()

# Campo de entrada para o palpite do jogador
entry_palpite = tk.Entry(janela, font=("Arial", 14))
entry_palpite.pack(pady=10)

# Botão para enviar o palpite
botao_palpite = tk.Button(janela, text="Tentar", font=("Arial", 14), command=processar_palpite)
botao_palpite.pack()

# Botão para reiniciar o jogo
botao_reiniciar = tk.Button(janela, text="Reiniciar", font=("Arial", 14), command=iniciar_jogo)
botao_reiniciar.pack(pady=10)

# Inicializa o jogo
iniciar_jogo()

# Inicia a interface gráfica
janela.mainloop()