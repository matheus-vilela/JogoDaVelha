import numpy as np
import os,time
from random import *

class Tabuleiro:

    def __init__(self):
  
        self.tabuleiro = [[''] * 3 for n in range(3)]

    # -------------------------------------------------
    def salvarJogada(self):

        return '-'.join(['-'.join(x) for x in self.tabuleiro])

    # -------------------------------------------------
    def restaurar(self, data):
  
        self.tabuleiro = np.reshape(data.split('-'), (3,3)).tolist()

       # -------------------------------------------------
    def realizarJogada(self, linha, coluna, icone):

       
        if linha < 0 or linha > 2:
            raise RuntimeError('Número de linha inválido: {}'.format(linha))
        if coluna < 0 or coluna > 2:
            raise RuntimeError('Número de coluna inválido: {}'.format(coluna))
       
        if self.tabuleiro[linha][coluna] != '':
            raise RuntimeError('A posição desejada já foi utilizada.')



        self.tabuleiro[linha][coluna] = icone
        vencedor = self.verificarVencedor(icone)

        return vencedor

    # -------------------------------------------------
    def realizarJogadaRandom(self, icone):

        opcoes = []
        for linha in range(3):
            for coluna in range(3):
                if self.tabuleiro[linha][coluna] == '':
                    opcoes.append((linha, coluna))

        shuffle(opcoes)

        if len(opcoes) > 0:
            linha = opcoes[0][0]
            coluna = opcoes[0][1]

            vencedor = self.realizarJogada(linha, coluna, icone)
            return vencedor
        else:
            empate = True
            return empate

    # -------------------------------------------------
    def verificarVencedor(self, icone):

        vitoria1 = self.tabuleiro[0][0] == self.tabuleiro[0][1] == self.tabuleiro[0][2] == icone
        vitoria2 = self.tabuleiro[1][0] == self.tabuleiro[1][1] == self.tabuleiro[1][2] == icone
        vitoria3 = self.tabuleiro[2][0] == self.tabuleiro[2][1] == self.tabuleiro[2][2] == icone
        vitoria4 = self.tabuleiro[0][0] == self.tabuleiro[1][0] == self.tabuleiro[2][0] == icone
        vitoria5 = self.tabuleiro[0][1] == self.tabuleiro[1][1] == self.tabuleiro[2][1] == icone
        vitoria6 = self.tabuleiro[0][2] == self.tabuleiro[1][2] == self.tabuleiro[2][2] == icone
        vitoria7 = self.tabuleiro[0][0] == self.tabuleiro[1][1] == self.tabuleiro[2][2] == icone
        vitoria8 = self.tabuleiro[0][2] == self.tabuleiro[1][1] == self.tabuleiro[2][0] == icone
       
        posicoes = [vitoria1,vitoria2,vitoria3,vitoria4,vitoria5,vitoria6,vitoria7,vitoria8] 

        opcoes = []
        for linha in range(3):
            for coluna in range(3):
                if self.tabuleiro[linha][coluna] == '':
                    opcoes.append((linha, coluna))

        print('{} --- {}'.format(opcoes, posicoes))
           
        for vencedor in posicoes:
            if vencedor == True:
                ganhou = icone
                break
            else:
                if len(opcoes) == 0:
                    ganhou = 'empate'
                else: 
                    ganhou = False

        return ganhou





     # -------------------------------------------------
    def mostrarTabuleiro(self, geral, empate,jogador1, jogador2, msg):
        # print('{}'.format(self.tabuleiro))
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\n =====================================================\n' )
        print('                          PLACAR \n                 ')
        print('    {} - peças {} - Total de vitórias: {}'.format(jogador1[0], jogador1[1], jogador1[2]))
        print('    {} - peças {} - Total de vitórias: {}'.format(jogador2[0], jogador2[1], jogador2[2]))
        print('\n    Total de empates: {}'.format(empate))
        print('\n|=====================================================|\n' )
        print('    {} {}                 '.format(geral, msg))
        print('\n|=====================================================|' )
        print("|               +-------+-------+-------+             |")

        for linha in self.tabuleiro:
            print("|               |       |       |       |             |")
            print("|               |  {}  |  {}  |  {}  |             |".format(linha[0].center(3, ' '), linha[1].center(3, ' '), linha[2].center(3, ' ')))
            print("|               |       |       |       |             |")
            print("|               +-------+-------+-------+             |")

        print(" ----------------------------------------------------- ")   