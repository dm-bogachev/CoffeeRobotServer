from threading import Thread
import socket
from TcpClient import *

import logger as log

BIND_IP_TO_DUARO  = "192.168.0.248"
BIND_NAME_TO_DUARO  = "duaro"
BIND_IP_TO_TABLET = "192.168.0.234"
BIND_NAME_TO_TABLET  = "tablet"

class TcpServer(Thread):
    """description of class"""
    clients = []
    
    def __init__(self, host='localhost', port=48569, timeout=60):
        self.host = host
        self.port = port
        self.timeout = timeout
        Thread.__init__(self)

    def run(self):
        log.push('CoffeeRobot TCP/IP Server Started')
        self.listen()

    def listen(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        log.push(['CoffeeRobot TCP/IP Server Bound at IP: ',
                    self.sock.getsockname()[0], 
                    ' Port: ',
                    str(self.sock.getsockname()[1])])

        self.sock.listen(5)
        log.push('CoffeeRobot TCP/IP Server Listening')

        while True:
            client, address = self.sock.accept()
            client.settimeout(self.timeout)
            log.push(['Client connected with IP: ',
                        address[0],  
                        ' Port: ',
                        str(address[1])])

            if address[0] == BIND_IP_TO_TABLET:
                tcp_client = TcpClient(client, address, name=BIND_NAME_TO_TABLET)
            elif address[0] == BIND_IP_TO_DUARO:
                tcp_client = TcpClient(client, address, name=BIND_NAME_TO_DUARO)
            else:
                tcp_client = TcpClient(client, address)

            self.clients.append(tcp_client)
            Thread(target=self.client_handle, args=(tcp_client, )).start()

    def client_handle(self, tcp_client):
        buf_size = 4096
        while True:
            try:
                data = tcp_client.receive_from()  
                if data:
                    if tcp_client.name == BIND_NAME_TO_TABLET:
                        for client in self.clients:
                            if client.name == BIND_NAME_TO_DUARO:
                                client.send_to('RETURN: ' + data)



            except socket.timeout:
                log.push(['Client with IP: ', tcp_client.address[0], ' was disconnected!'])
                tcp_client.close()
                return False
                pass