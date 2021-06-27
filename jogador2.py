import socket
import os
from tabuleiro import Tabuleiro

HOST = '127.0.0.1' 
PORT = 5000       
BUFFER_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (HOST, PORT)
sock.connect(server_address)

os.system('cls' if os.name == 'nt' else 'clear')
print('________________________________________________ ')
print('JOGO DA VELHA')
name = input('\nPara começar, informe o seu nome: ')
sock.sendall('{}'.format(name).encode())

os.system('cls' if os.name == 'nt' else 'clear')
print('Criando partida...')

dados1 = sock.recv(BUFFER_SIZE)
jogador1 = dados1.decode('utf-8').split('-')

vitorias1 = 0
vitorias2 = 0
empate = 0
cont = 0

while cont == 0:
    player1 = jogador1[0], 'X' if jogador1[1] == '1' else 'O',vitorias1
    player2 = name, 'O' if jogador1[1] == '1' else 'X',vitorias2
    tabuleiro = Tabuleiro()

    cont = 1
    while cont == 1:
        tabuleiro.mostrarTabuleiro('Jogador da vez >>>>>>  ', empate, player1, player2, jogador1[0])
        print('\nAguardando a jogada de {}.\n'.format(jogador1[0]))
        
        data = sock.recv(BUFFER_SIZE)
        tabuleiro.restaurar(data.decode('utf-8'))
        resposta = tabuleiro.verificarVencedor(player1[1])
        if resposta == 'empate':
            tabuleiro.mostrarTabuleiro( '>>>>>>>>>> ',empate, player1, player2,'EMPATE <<<<<<<<<<')
            print("\nDeseja jogar novamente ?\n")
            opcao = int(input("\nDigite 1 para jogar novamente, digite 2 para sair: "))
            sock.sendall('{}'.format(True if opcao == 1 else False).encode('utf-8'))
            data = sock.recv(BUFFER_SIZE)
            contJogador1 = data.decode('utf-8')
            if contJogador1 == 'True':
                if opcao == 1:
                    cont = 0
                    empate = empate+1
                    
                else:
                    opcaoGame = 0
                    break
            else:
                break
        elif resposta != False:
            tabuleiro.mostrarTabuleiro( jogador1[0],empate, player1, player2,'VENCEU <<<<<<<<<<')
        
            print("\nDeseja jogar novamente ?\n")
            opcao = int(input("\nDigite 1 para jogar novamente, digite 2 para sair: "))
            sock.sendall('{}'.format(True if opcao == 1 else False).encode('utf-8'))
            data = sock.recv(BUFFER_SIZE)
            contJogador1 = data.decode('utf-8')
            if contJogador1 == 'True':
                if opcao == 1:
                    cont = 0
                    vitorias1 = vitorias1+1
                    
                else:
                    opcaoGame = 0
                    break
            else:
                break
        
        else:
            tabuleiro.mostrarTabuleiro('Sua vez de jogar ', empate, player1, player2, '<<<<<')

            posicao_valida = True
            while posicao_valida:
                print('Faça a sua jogada:\n')
                linha = int(input('>>>Digite o número da linha (entre 0 e 2): '))
                coluna = int(input('>>>Digite o número da coluna (entre 0 e 2): '))

                posicao_valida = False
                try:
                    tabuleiro.realizarJogada(linha, coluna, '{}'.format(player2[1]))
                    tabuleiro.salvarJogada()
                except:
                    posicao_valida = True
                    print('Valores incorretos, preencha novamente.')

            resposta = tabuleiro.verificarVencedor(player2[1])
            if resposta == 'empate':
                tabuleiro.mostrarTabuleiro( '>>>>>>>>>> ',empate, player1, player2,'EMPATE <<<<<<<<<<')
                sock.sendall(tabuleiro.salvarJogada().encode('utf-8'))
                print("\nDeseja jogar novamente ?\n")
                opcao = int(input("\nDigite 1 para jogar novamente, digite 2 para sair: "))
                sock.sendall('{}'.format(True if opcao == 1 else False).encode('utf-8'))
                data = sock.recv(BUFFER_SIZE)
                contJogador1 = data.decode('utf-8')
                if contJogador1 == 'True':
                    if opcao == 1:
                        cont = 0
                        empate = empate+1
                        
                    else:
                        opcaoGame = 0
                        break
                else:
                    break
            
            elif resposta != False:
                tabuleiro.mostrarTabuleiro( '>>>>>>>>>> VOCÊ',empate, player1, player2,'VENCEU <<<<<<<<<<')
            
                sock.sendall(tabuleiro.salvarJogada().encode('utf-8'))

                print("\nDeseja jogar novamente ?\n")
                opcao = int(input("\nDigite 1 para jogar novamente, digite 2 para sair: "))
                sock.sendall('{}'.format(True if opcao == 1 else False).encode('utf-8'))
                data = sock.recv(BUFFER_SIZE)
                contJogador1 = data.decode('utf-8')
                if contJogador1 == 'True':
                    if opcao == 1:
                        cont = 0
                        vitorias2 = vitorias2+1

                    else:
                        opcaoGame = 0
                        break
                else:
                    break

            else:
                
                tabuleiro.mostrarTabuleiro( '>>>>>>>>>> ',empate, player1, player2,'EMPATE <<<<<<<<<<')
                sock.sendall(tabuleiro.salvarJogada().encode('utf-8'))
                print('------------------')
                print('Aguardando a jogada de {}.\n'.format(jogador1[0]))

