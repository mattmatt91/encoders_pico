import argparse
import math
from pythonosc import dispatcher, osc_server,  udp_client
import random
import time
from threading import Thread
from time import sleep, time


class OSCDevice():
    def __init__(self):
        # init sender
        self.parser_sender = argparse.ArgumentParser()
        self.parser_sender.add_argument("--ip", default="127.0.0.1",
            help="The ip of the OSC server")
        self.parser_sender.add_argument("--port", type=int, default=4004,
            help="The port the OSC server is listening on")
        self.args_sender = self.parser_sender.parse_args()
        self.client = udp_client.SimpleUDPClient(self.args_sender.ip, self.args_sender.port)
        
        # init reciver
        self.parser_reciever = argparse.ArgumentParser()
        self.parser_reciever.add_argument("--ip",
            default="127.0.0.1", help="The ip to listen on")
        self.parser_reciever.add_argument("--port",
            type=int, default=4004, help="The port to listen on")
        args = self.parser_reciever.parse_args()

        self.dispatcher_reciever = dispatcher.Dispatcher()
        self.dispatcher_reciever.set_default_handler(self.default_handler)

        self.server = osc_server.ThreadingOSCUDPServer(
            (args.ip, args.port), dispatcher)
        print("Serving on {}".format(self.server.server_address))
        
        self.buffer = []
        
        
    def start_reciever(self):
        Thread(target=self.server.serve_forever).start()


    def send_msg(self, address="/filter", value = 0):
        self.client.send_message(address, value)
        
        
    def default_handler(self, unused_addr, args, value):
        msg = {'args': args, 'value': value, 'unused_addr': unused_addr}
        self.buffer.append(msg)
        
    def read_buffer(self):
        buf = self.buffer
        self.buffer = []
        return buf

if __name__ == '__main__':
    osc_device = OSCDevice()
    osc_device.start_reciever()
    time_start = time()
    while True:
        if time() > time_start +2:
            time_start = time()
        buffer = osc_device.read_buffer()
        if len(buffer) >0:
            print(buffer)
        


