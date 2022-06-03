import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.104"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    # Retorna o jogador
    def getP(self):
        return self.p

    def connect(self):
        try:
            # Conecta ao cliente
            self.client.connect(self.addr)
            # Decodifica a mensagem recebida
            # Cada cliente, por padrão, acha que é o jogador 1, por isso é importante decodificar
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            # Envia os dados codificados como string para o servidor
            self.client.send(str.encode(data))
            # Recebe de volta os dados do objeto
            return pickle.loads(self.client.recv(2048 * 2))
        except socket.error as e:
            print(e)
