#!/usr/bin/env python3

import map
import socket
import struct
import time

PORT = 55002

"""
This controls the switches, lights and car speeds
Either in simulation mode or via ros2
"""
class Controller:
    def __init__(self):
        self.switches = {n:'left' for n in map.nodes.keys()}
        self.simulation = None
        self.max_voltage_motor = 300 # 1/100 V
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.hostnames = {}

        for switch in self.switches:
            self.set_switch(switch,'left') # so the switch is in a known state
    def set_sim(self, simulation):
        self.simulation = simulation
    
    # SWITCH CONTROL

    def set_switch(self,name,dir):
        self.switches[name] = dir
        if self.simulation:
            self.simulation.set_switch(name,dir)
        else:
            pass
            #TODO: implement ros2 publish

    def get_switch_state(self,name):
        return self.switches[name]
    
    # CAR CONTROL

    def add_car_controller(self,name, hostname):
        self.hostnames[name] = hostname

    def send_light_message(self, name, headlight, brake, blinker):
        if self.simulation == None:
            msg_type = 1  # Light message
            buffer = struct.pack('BBBB', msg_type, headlight, brake, blinker)
            self.send(self.hostnames[name], buffer)

    def send_motor_message(self, name, voltage):
        if voltage > self.max_voltage_motor:
            voltage = self.max_voltage_motor
        if voltage < 0:
            voltage = 0
        if self.simulation:
            self.simulation.set_motor_voltage(name, voltage)
        else:
            msg_type = 2  # Motor message
            buffer = struct.pack('BB', msg_type, voltage)
            self.send(self.hostnames[name], buffer)

    def send(self, hostname, buffer):
        max_attempts = 1
        current_attempt = 0
        timeout = 2  # Retry timeout in seconds

        while current_attempt < max_attempts:
            try:
                self.sock.sendto(buffer, (hostname, PORT))
                print("Message sent successfully.")
                return
            except socket.error as e:
                print("Error sending message:", e)
                current_attempt += 1
                if current_attempt < max_attempts:
                    print(f"Retrying in {timeout} seconds...")
                    time.sleep(timeout)
                else:
                    print("Max attempts reached. Connection failed.")
                    return
                
if __name__ == "__main__":
    import sys
    # test smartcar control
    controller = Controller()
    controller.add_car_controller("P1", "192.168.178.67")
    controller.send_motor_message("P1", int(sys.argv[4]))
    controller.send_light_message("P1", int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))
