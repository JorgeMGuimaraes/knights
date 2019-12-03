#
#Processa todas as mudanças de renderização do software
#
from PPlay.window import *
from random import randint as rd

janela = None

def iniciarJanela():
    dados = open("Configs", "r")
    for linha in dados:
        config = linha.split("=")
        if config[0] == "Largura_janela"    : x = int(config[1])
        if config[0] == "Altura_janela"     : y = int(config[1])
        if config[0] == "Nome"              : nome = config[1]
    dados.close()
    janela = Window(x, y)
    janela.set_title(nome)
    #print("Janela iniciada: %s de %dx%d"%(janela.get_title, janela.width, janela.height))
    return janela

def render(jan):
    jan.update()
    return

def drawStack(gameImages):
    for gm in gameImages:
        gm.draw()
    return

def testarCores():
    return (rd(0, 255), rd(0, 255), rd(0, 255))
