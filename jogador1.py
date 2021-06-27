import random
import socket
import os
import time
from tabuleiro import Tabuleiro


HOST = '127.0.0.1' 
PORT = 5000       
BUFFER_SIZE = 1024 

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (HOST, PORT)
sock.bind(server_address)

sock.listen(1)


os.system('cls' if os.name == 'nt' else 'clear')
print('________________________________________________ ')
print('JOGO DA VELHA')

name = input('\nPara começar, informe o seu nome: ')

icon = 0
while icon == 0:
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\n________________________________________________ ')
    print('Jogador: '+ name)
    icon = int(input('\n\nEscolha com qual peça irá jogar:\n\nDigite 1 para o "X"\nDigite 2 para a "Bola"\n\nDigite a opção desejada: '))
    if icon < 1 or icon > 2:
        icon = 0
        print('Opção inválida, verifique as opcoes disponiveis.')


opcaoGame = 0
while opcaoGame == 0:
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\n____________________________________________ ')
    print('Jogador: '+ name)
    if icon == 1 :
        print('Icone escolhido: X')
    else:
        print('Icone escolhido: Bola')


    print('\n\nProximo passo, selecione a opcao de jogo:')
    opcaoGame = int(input('\n\nDigite 1 - Jogo multiplayer\nDigite 2 - Jogo singleplayer\n\nDigite a opção desejada: '))
    if opcaoGame < 1 or opcaoGame > 2:
        opcaoGame = 0
        print('Opção inválida')

vitorias1 = 0
vitorias2 = 0
empate = 0

while opcaoGame == 1:

    os.system('cls' if os.name == 'nt' else 'clear')
    print('Aguardando a conexao do jogador2...')
    connection, client_address = sock.accept()
    dados = connection.recv(BUFFER_SIZE)
    jogador2 = dados.decode('utf-8')

    os.system('cls' if os.name == 'nt' else 'clear')
    print('O jogador {} conectou...'.format(jogador2))
    time.sleep(1.5)

    connection.sendall('{}-{}'.format(name, icon).encode())

    cont = 0
    while cont == 0:
        tabuleiro = Tabuleiro()
        player1 = name, 'X' if icon == 1 else 'O',vitorias1
        player2 = jogador2, 'O' if icon == 1 else 'X',vitorias2

        if random.randint(1,2) == 1:
            tabuleiro.mostrarTabuleiro('Jogador da vez >>>>>>  ', empate, player1, player2, name)
            posicao_valida = True
            while  posicao_valida:
                print('Faça a sua jogada:\n')
                linha = int(input('>>>Digite o número da linha (entre 0 e 2): '))
                coluna = int(input('>>>Digite o número da coluna (entre 0 e 2): '))

                posicao_valida = False
                try:
                    tabuleiro.realizarJogada(linha, coluna, player1[1])
                    tabuleiro.salvarJogada()
                except:
                    posicao_valida = True
                    print('Valores incorretos, preencha novamente.')

            tabuleiro.mostrarTabuleiro('Jogador da vez >>>>>>  ', empate, player1, player2, jogador2)
            print('\nAguardando a jogada de {}.'.format(jogador2))

            connection.sendall(tabuleiro.salvarJogada().encode('utf-8'))
        else:
            tabuleiro.mostrarTabuleiro('Jogador da vez >>>>>>  ', empate, player1, player2, jogador2)
            connection.sendall(tabuleiro.salvarJogada().encode('utf-8'))

        cont = 1
        while cont == 1:
            data = connection.recv(BUFFER_SIZE)

            if not data:
                print('{} desconectou.'.format(jogador2))
                break  

            tabuleiro.restaurar(data.decode('utf-8'))
            resposta = tabuleiro.verificarVencedor(player2[1])
            if resposta == 'empate':
                tabuleiro.mostrarTabuleiro( '>>>>>>>',empate, player1, player2,'EMPATE')
                print("\nDeseja jogar novamente ?\n")
                opcao = int(input("\nDigite 1 para jogar novamente, digite 2 para sair: "))
                contJogador2 = connection.recv(BUFFER_SIZE)
                continua = contJogador2.decode('utf-8')
                if continua ==  'True':
                    if opcao == 1:
                        cont = 0
                        empate = empate+1
                        connection.sendall('{}'.format(True).encode('utf-8'))
                        break
                    
                    else:
                        opcaoGame = 0
                        connection.sendall('{}'.format(False).encode('utf-8'))
                        break
                else:
                    break

            elif resposta == False:
                tabuleiro.mostrarTabuleiro('Jogador da vez >>>>>>  ', empate, player1, player2, name)
            
                posicao_valida = True
                while  posicao_valida:
                    print('\nFaça a sua jogada:\n')
                    linha = int(input('>>>Digite o número da linha (entre 0 e 2): '))
                    coluna = int(input('>>>Digite o número da coluna (entre 0 e 2): '))

                    posicao_valida = False
                    try:
                        tabuleiro.realizarJogada(linha, coluna,  '{}'.format('X' if icon == 1 else 'O'))
                        tabuleiro.salvarJogada()
                    except:
                        posicao_valida = True
                        print('Valores incorretos, preencha novamente.')

            else:
                tabuleiro.mostrarTabuleiro( jogador2,empate, player1, player2,'VENCEU <<<<<<<<<<')
            
                print("\nDeseja jogar novamente ?\n")
                opcao = int(input("\nDigite 1 para jogar novamente, digite 2 para sair: "))
                contJogador2 = connection.recv(BUFFER_SIZE)
                continua = contJogador2.decode('utf-8')
            
                if continua ==  'True':
                    if opcao == 1:
                        cont = 0
                        vitorias2 = vitorias2+1
                        connection.sendall('{}'.format(True).encode('utf-8'))
                        break
                    
                    else:
                        opcaoGame = 0
                        connection.sendall('{}'.format(False).encode('utf-8'))
                        break
                else:
                    break


            resposta = tabuleiro.verificarVencedor(player1[1])
            if resposta == 'empate':
                tabuleiro.mostrarTabuleiro( '>>>>>>>',empate, player1, player2,'EMPATE')
                connection.sendall(tabuleiro.salvarJogada().encode('utf-8'))
                print("\nDeseja jogar novamente ?\n")
                opcao = int(input("\nDigite 1 para jogar novamente, digite 2 para sair: "))
                contJogador2 = connection.recv(BUFFER_SIZE)
                continua = contJogador2.decode('utf-8')
                if continua ==  'True':
                    if opcao == 1:
                        cont = 0
                        empate = empate+1
                        connection.sendall('{}'.format(True).encode('utf-8'))
                        break
                    
                    else:
                        opcaoGame = 0
                        connection.sendall('{}'.format(False).encode('utf-8'))
                        break
                else:
                    break
            elif resposta != False:
                tabuleiro.mostrarTabuleiro( name,empate, player1, player2,'VENCEU <<<<<<<<<<')
                connection.sendall(tabuleiro.salvarJogada().encode('utf-8'))
                print("\nDeseja jogar novamente ?\n")
                opcao = int(input("\nDigite 1 para jogar novamente, digite 2 para sair: "))
                contJogador2 = connection.recv(BUFFER_SIZE)
                continua = contJogador2.decode('utf-8')

                if continua ==  'True':
                    if opcao == 1:
                        cont = 0
                        vitorias1 = vitorias1+1
                        connection.sendall('{}'.format(True).encode('utf-8'))
                        break
                    else:
                        opcaoGame = 0
                        connection.sendall('{}'.format(False).encode('utf-8'))
                        break
                else:
                    break

            else:
                tabuleiro.mostrarTabuleiro('Jogador da vez >>>>>>  ', empate, player1, player2, jogador2)
                connection.sendall(tabuleiro.salvarJogada().encode('utf-8'))
                print('\nAguardando a jogada de {}.'.format(jogador2))





while opcaoGame == 2:
     
        tabuleiro = Tabuleiro()
        cont = 0
        player1 = name, 'X' if icon == 1 else 'O',vitorias1
        player2 = 'Máquina', 'O' if icon == 1 else 'X',vitorias2

        
        while cont == 0:

            tabuleiro.mostrarTabuleiro('Jogador da vez >>>>>>  ', empate, player1, player2, name)
            print('\nFaça a sua jogada:')
            jogada = True
            while jogada:
                linha = int(input('>>>Digite o número da linha (entre 0 e 2): '))
                coluna = int(input('>>>Digite o número da coluna (entre 0 e 2): '))

                jogada = False
                try:
                    if (tabuleiro.realizarJogada(linha, coluna, player1[1] )) == False:
                        tabuleiro.salvarJogada()
                        tabuleiro.mostrarTabuleiro('Jogador da vez >>>>>>  ', empate, player1, player2, 'A máquina')
                        print('\nAguarde a jogada do oponente...')
                    
                    else:
                        break
                except:
                    jogada = True
                    print('Valores incorretos, preencha novamente.')
            
            verificar = tabuleiro.verificarVencedor(player1[1])
            if verificar != False:

                tabuleiro.mostrarTabuleiro(name, empate, player1, player2, 'VENCEU <<<<<<<<<<<<<')

                print("\nDeseja jogar novamente ?\n")
                opcao = int(input("\nDigite 1 para jogar novamente, digite 2 para sair: "))
                if opcao == 1:
                    cont = 1
                    vitorias1 = vitorias1+1
                    break
                else:
                    opcaoGame = 0
                    break

            emp = tabuleiro.realizarJogadaRandom(player2[1])
            if emp == True:
                tabuleiro.mostrarTabuleiro('EMPATE', empate, player1, player2, '')

                print("\nDeseja jogar novamente ?\n")
                opcao = int(input("\nDigite 1 para jogar novamente, digite 2 para sair: \n"))
                if opcao == 1:
                    cont = 1
                    empate = empate+1
                    break
                else:
                    opcaoGame = 0
                    break

            verificar = tabuleiro.verificarVencedor(player2[1])
            if verificar != False:
                tabuleiro.mostrarTabuleiro('A Máquina', empate, player1, player2, 'VENCEU <<<<<<<<')
            
                print("\nDeseja jogar novamente ?\n")
                opcao = int(input("\nDigite 1 para jogar novamente, digite 2 para sair: "))
                if opcao == 1:
                    cont = 1
                    vitorias2 = vitorias2+1
                    break
                else:
                    opcaoGame = 0
                    break

            else:
                    tabuleiro.salvarJogada()
                    time.sleep(2)
                  

 
