import logger as log

class TcpClient():
    """description of class"""

    def __init__(self, client, address, name='TcpClient', buf_size=4096):
        self.client = client
        self.address = address
        self.name = name
        self.buf_size = 4096

    def receive_from(self):
        self.data = self.client.recv(self.buf_size).decode('utf-8')
        log.push(['Received data from ', self.address[0], ' (', self.name, ') : ', self.data])
        return self.data

    def on_receive(self):
        pass

    def send_to(self, msg):
        self.client.send(msg.encode('utf-8'))

    def close(self):
        self.client.close()

