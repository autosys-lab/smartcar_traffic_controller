#!/usr/bin/env python3

import pygame
import sys
import map
from controller import Controller
from simulation import Simulation
from car_tracking import CarTracking
import config
import render
import queue
import threading

class Main:
    def __init__(self, use_sim=False):
        self.controller = Controller()
        self.car_tracking = CarTracking(self.controller)
        self.selected_car = None
        self.clock = pygame.time.Clock()
        self.user_task_queue = queue.Queue()
        self.user_task_thread = threading.Thread(target=self.user_task_handler)
        self.cars_awaiting_user_input = []
        if use_sim:
            self.sim = Simulation(self.car_tracking, config.MAP_SCALE)
            self.controller.set_sim(self.sim)

    def run(self):
        self.setup()
        
        while True:
            if self.sim:
                self.sim.step()
            # first get the positions of the cars on the topological map (not real world coordinates)
            self.cars = self.car_tracking.get_cars()
            # check if there are new cars the user has to set active or dummy
            new_cars = self.car_tracking.get_unkown_cars()
            for car in new_cars:
                if self.sim:
                    self.car_tracking.make_car_active(car, "sim.local")
                    continue
                if car.name not in self.cars_awaiting_user_input:
                    print("New car detected: " + car.name)
                    self.cars_awaiting_user_input.append(car.name)
                    self.user_task_queue.put(car)
            # check for events that might adjust the routes of the cars
            self.event_handler()
            # plan the routes for the cars
            for car in self.cars:
                if car.state == 'waiting':
                    car.set_destination('B2')
            # check if action for switches is needed and execute
            render.render(self.screen, self.cars, self.controller, self.selected_car)


            self.clock.tick(30)

    def setup(self):
        pygame.init()

        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Car Traffic Controller")

        self.user_task_thread.daemon = True
        self.user_task_thread.start()

    def user_task_handler(self):
        while True:
            car = self.user_task_queue.get()
            self.get_user_input_on_car(car)

    def event_handler(self):
        #global config.SCREEN_WIDTH, config.SCREEN_HEIGHT, config.MAP_SCALE, config.MAP_MARGIN_LEFT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Exiting...")
                pygame.quit()
                sys.exit()
            # Handle window resizing
            if event.type == pygame.VIDEORESIZE:
                if event.size[0] < 800 or event.size[1] < 400:
                    continue
                config.SCREEN_WIDTH, config.SCREEN_HEIGHT = event.size
                config.MAP_SCALE = config.SCREEN_HEIGHT - 2*config.MAP_MARGIN_TOP
                config.MAP_MARGIN_LEFT = (config.SCREEN_WIDTH - 2*config.MAP_SCALE) // 2

                pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for car in self.cars:
                    circle = car.visual
                    distance = ((circle.x - mouse_x) ** 2 + (circle.y - mouse_y) ** 2) ** 0.5
                    if distance <= circle.radius:
                        # Toggle the blinking state
                        circle.blinking = not circle.blinking
                        if circle.blinking:
                            if self.selected_car:
                                self.selected_car.visual.blinking = False
                            self.selected_car = car
                        else:
                            self.selected_car = None
    
    def get_user_input_on_car(self, car):
        car.visual.blinking = True
        user_input = input("What is the hostname of " + car.name + "? (leave blank for dummy car)\n")
        if user_input == "":
            self.car_tracking.make_car_dummy(car)
            print("Car " + car.name + " is now a dummy car.")
        else:
            self.car_tracking.make_car_active(car, user_input)
            print("Car " + car.name + " is now an active car with hostname: "+user_input+".")
        car.visual.blinking = False

if __name__ == "__main__":
    main = Main(use_sim=True)
    main.run()