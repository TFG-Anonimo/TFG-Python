import socket
import time
import numpy as np
import array

class Receiver:
    def __init__(self, port=5555):
        self.socket = socket.socket(socket.AF_INET, # Internet
                                    socket.SOCK_DGRAM) # UDP
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1)
        ip_address = Receiver.get_pc_ip()
        self.socket.bind((ip_address, port))
        print("Listening on: ", ip_address, ":", port)

        # Discard first packets because they are noisy
        end_time = time.time() + 2.5
        
        while time.time() < end_time:
            self.socket.recv(1921*4)

    def retrieve_sound_samples(self):
        data = self.socket.recv(1921*4)
        data = array.array('f', data)
        data.byteswap()
                 
        if len(data) != 1921:
            raise ValueError("Received malformed packet")
    
        return np.array(data[1:].tolist())

    @staticmethod
    def get_pc_ip():
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.connect(("8.8.8.8", 80))
        pc_ip_address = temp_socket.getsockname()[0]
        temp_socket.close()
        return pc_ip_address