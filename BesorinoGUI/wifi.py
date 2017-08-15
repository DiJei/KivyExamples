import socket

class WifiUDP():
    HOST = '192.168.4.255'   # Endereco IP do Servidor
    PORT = 333             # Porta que o Servidor esta
    udp  = None
    def __init__(self):
        try:
            self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.dest = (self.HOST, self.PORT)
        except socket.error, msg:
            print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]

    def connect(self):
        try:
            self.udp.connect(self.dest)
        except Exception as e:
            print("Not able to connect")
        finally:
            self.udp.close()

    def send_data(self,msg):
        data = str.encode(msg)
        try:
            self.udp.send(data)
        except socket.error, msg:
            print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]

my_socket = WifiUDP()
