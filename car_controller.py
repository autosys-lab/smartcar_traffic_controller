#!/usr/bin/env python3

import socket
import struct
import time

class CarController:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.max_voltage_motor = 300 # 1/100 V

        self.headlight = 0
        self.last_headlight = 0
        self.brake = 0
        self.last_brake = 0
        self.blinker = 0
        self.last_blinker = 0

    def turn_on_hazard_lights(self):
        self.last_blinker = self.blinker
        self.blinker = 3
        self.__send_light_message()
    
    def turn_off_hazard_lights(self):
        self.blinker = self.last_blinker
        self.__send_light_message()
    
    def turn_on_left_blinker(self):
        self.blinker = 1
        self.__send_light_message()

    def turn_on_right_blinker(self):
        self.blinker = 2
        self.__send_light_message()
    
    def turn_off_blinker(self):
        self.blinker = 0
        self.__send_light_message()

    def turn_on_headlights(self):
        self.headlight = 1
        self.__send_light_message()
    
    def turn_off_headlights(self):
        self.headlight = 0
        self.__send_light_message()
    
    def turn_on_full_beam(self):
        self.last_headlight = self.headlight
        self.headlight = 2
        self.__send_light_message()

    def turn_off_full_beam(self):
        self.headlight = self.last_headlight
        self.__send_light_message()

    def turn_on_rear_lights(self):
        self.brake = 1
        self.__send_light_message()
    
    def turn_off_rear_lights(self):
        self.brake = 0
        self.__send_light_message()

    def turn_on_brake_lights(self):
        self.last_brake = self.brake
        self.brake = 2
        self.__send_light_message()

    def turn_off_brake_lights(self):
        self.brake = self.last_brake
        self.__send_light_message()

    """
    Voltage is in 1/100 V
    """
    def change_motor_speed(self, voltage):
        if voltage > self.max_voltage_motor:
            voltage = self.max_voltage_motor
        self.__send_motor_message(voltage)


    ## Private methods

# Example usage
if __name__ == "__main__":
    car = CarController("example.com", 44556)  # Replace with the actual hostname and port
    car.change_motor_speed(100)
    car.turn_on_headlights()
    car.turn_on_rear_lights()
    car.turn_on_hazard_lights()
