#File Name: Main.py
import kivy
kivy.require("1.9.0")
from kivy.app import  App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

import socket


HOST = '192.168.4.1'  # Endereco IP do Servidor
PORT = 333             # Porta que o Servidor esta
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, PORT)

class Control(BoxLayout):
    def __init__(self, **kwargs):
        BoxLayout.__init__(self, **kwargs)
        self.frente.bind(on_press=self.frenteButton)
        self.atras.bind(on_press=self.atrasButton)
        self.direita.bind(on_press=self.direitaButton)
        self.esquerda.bind(on_press=self.esquerdaButton)
    
    def frenteButton(self,*args):
        print("frente")
        msg = "1"
        data = bytes(msg,"utf-8")
        udp.send(data)
    def atrasButton(self,*args):
        print("atras")
        msg = "2"
        data = bytes(msg,"utf-8")
        udp.send(data)
    def direitaButton(self,*args):
        print("direita")
        msg = "3"
        data = bytes(msg,"utf-8")
        udp.send(data)
    def esquerdaButton(self,*args):
        print("esquerda")
        msg = "4"
        data = bytes(msg,"utf-8")
        udp.send(data)

class ControlApp(App):
    def build(self):
        return Control()
    
if __name__ == '__main__':
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.connect(dest)
    ControlApp().run()