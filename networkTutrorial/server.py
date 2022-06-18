import socket
from _thread import *
import pickle
from game import Game

server = "192.168.0.104"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

# Armazena os endereços de ip dos clientes conectados
connected = set()
# Armazena os jogos
games = {}
# Acompanhará o id atual
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    # Dessa forma o jogador sabe se é o 1 ou o 2
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            # dado recebido do cliente
            data = conn.recv(4096).decode()

            # Toda volta no loop é verificado se o jogo ainda existe
            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    # Se o dado enviado for reset, o jogador vai querer jogar outra vez
                    if data == "reset":
                        game.resetWent()
                    # Se o dado enviado for get, o jogador vai querer um jogo do servidor
                    elif data != "get":
                        game.play(p, data)

                    # Empacota o jogo e envia para os clientes
                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    # Se algo der errado no loop, o jogo será apagado
    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


# Continuamente procura por conexões
while True:
    # A conexão é aceita
    conn, addr = s.accept()
    print("Connected to:", addr)

    # Acompanha quantos jogadores estão conectados ao mesmo tempo
    idCount += 1
    # Jogador atual
    p = 0
    # A cada 2 pessoas que se conectam ao jogo, o gameId é incrementado
    gameId = (idCount - 1)//2
    # Dependendo da quantidade de jogadores conectados
    # se você for o jogador 1 ou 2, ele criará uma nova sessão de jogo
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))
