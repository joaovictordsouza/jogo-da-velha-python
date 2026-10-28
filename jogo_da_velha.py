"""
Jogo da Velha com interface gráfica (Tkinter)
Tkinter já vem instalado com o Python, não precisa instalar nada.
Para jogar: python jogo_da_velha.py
"""

import tkinter as tk

# 1) CORES (mude aqui e o jogo inteiro muda)
PAPEL = "#f4f7fa"
GRAFITE = "#2b2d33"
AZUL = "#1f3a93"       # cor do X
VERMELHO = "#d64045"   # cor do O
DESTAQUE = "#fff2b8"   # casas vencedoras

# 2) AS 8 COMBINAÇÕES QUE DÃO VITÓRIA (índices das casas)
#    0 | 1 | 2
#    3 | 4 | 5
#    6 | 7 | 8
COMBINACOES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # linhas
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # colunas
    (0, 4, 8), (2, 4, 6),             # diagonais
]

# 3) ESTADO DO JOGO: tudo que o jogo precisa "lembrar"
#    Usamos dicionários para poder alterar os valores dentro das funções.
estado = {
    "tabuleiro": [""] * 9,  # 9 casas vazias
    "jogador": "X",         # de quem é a vez
    "acabou": False,        # o jogo terminou?
}
placar = {"X": 0, "O": 0, "empate": 0}

# 4) JANELA E COMPONENTES (widgets)
janela = tk.Tk()
janela.title("Jogo da Velha")
janela.configure(bg=PAPEL, padx=24, pady=16)
janela.resizable(False, False)

tk.Label(janela, text="Jogo da Velha", font=("Arial", 26, "bold"),
         bg=PAPEL, fg=GRAFITE).pack()

lbl_placar = tk.Label(janela, font=("Arial", 13), bg=PAPEL, fg=GRAFITE)
lbl_placar.pack(pady=(4, 0))

lbl_status = tk.Label(janela, font=("Arial", 16), bg=PAPEL, fg=GRAFITE)
lbl_status.pack(pady=8)

# Moldura escura: o espaço (padx/pady) entre as casas vira as linhas do jogo
moldura = tk.Frame(janela, bg=GRAFITE, padx=3, pady=3)
moldura.pack()

# Criamos 9 casas. Usamos Label (e não Button) para as cores
# funcionarem igual no Windows, Mac e Linux.
casas = []
for i in range(9):
    casa = tk.Label(moldura, text="", width=4, height=2, bg=PAPEL,
                    font=("Arial", 36, "bold"), cursor="hand2")
    casa.grid(row=i // 3, column=i % 3, padx=3, pady=3)
    # i=i "congela" o valor de i para esta casa (senão todas usariam o último i)
    casa.bind("<Button-1>", lambda evento, i=i: jogar(i))
    casas.append(casa)


# 5) FUNÇÕES DO JOGO
def jogar(posicao):
    """Executa uma jogada na posição clicada."""
    # Ignora cliques inválidos
    if estado["acabou"] or estado["tabuleiro"][posicao] != "":
        return

    jogador = estado["jogador"]
    estado["tabuleiro"][posicao] = jogador
    desenhar()

    combinacao = verificar_vitoria()

    if combinacao:
        estado["acabou"] = True
        placar[jogador] += 1
        destacar_vitoria(combinacao)
        lbl_status.config(text=f"Jogador {jogador} venceu!")
    elif "" not in estado["tabuleiro"]:
        # Sem casas vazias e sem vencedor = empate
        estado["acabou"] = True
        placar["empate"] += 1
        lbl_status.config(text="Deu velha! Empate.")
    else:
        # Troca a vez
        estado["jogador"] = "O" if jogador == "X" else "X"
        lbl_status.config(text=f"Vez do jogador {estado['jogador']}")

    atualizar_placar()


def verificar_vitoria():
    """Devolve a combinação vencedora, ou None se ninguém ganhou ainda."""
    t = estado["tabuleiro"]
    for a, b, c in COMBINACOES:
        if t[a] != "" and t[a] == t[b] == t[c]:
            return (a, b, c)
    return None


def desenhar():
    """Copia o estado do tabuleiro para a tela."""
    for i, casa in enumerate(casas):
        simbolo = estado["tabuleiro"][i]
        cor = AZUL if simbolo == "X" else VERMELHO
        casa.config(text=simbolo, fg=cor, bg=PAPEL)


def destacar_vitoria(combinacao):
    for i in combinacao:
        casas[i].config(bg=DESTAQUE)


def atualizar_placar():
    lbl_placar.config(
        text=f"X: {placar['X']}     Empates: {placar['empate']}     O: {placar['O']}"
    )


def nova_partida():
    estado["tabuleiro"] = [""] * 9
    estado["jogador"] = "X"
    estado["acabou"] = False
    desenhar()
    lbl_status.config(text="Vez do jogador X")


def zerar_placar():
    placar.update({"X": 0, "O": 0, "empate": 0})
    atualizar_placar()
    nova_partida()


# 6) BOTÕES
frame_botoes = tk.Frame(janela, bg=PAPEL)
frame_botoes.pack(pady=(14, 0))
tk.Button(frame_botoes, text="Nova partida", command=nova_partida,
          font=("Arial", 12)).pack(side="left", padx=4)
tk.Button(frame_botoes, text="Zerar placar", command=zerar_placar,
          font=("Arial", 12)).pack(side="left", padx=4)

# 7) COMEÇAR
atualizar_placar()
nova_partida()
janela.mainloop()  # mantém a janela aberta, esperando os cliques
