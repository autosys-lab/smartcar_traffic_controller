import pathplanner
import map
import render
from car_controller import CarController
import config
from pid import PIDController
import time

HEADLIGHT_ON = 1
HEADLIGHT_OFF = 0
FULL_BEAM = 2
REAR_ON = 1
REAR_OFF = 0
BRAKE = 2
BLINKER_LEFT = 1
BLINKER_RIGHT = 2
BLINKER_OFF = 0
HAZARD_LIGHTS = 3



class Car:
    def __init__(self, name, position, controller):
        self.name = name
        self.hostname = None
        self.active = False
        self.position = position
        self.controller = controller
        self.state = 'waiting'
        # states: waiting, on_route, almost_there
        self.changed_switch = False
        self.visual = render.CarCircle(name)
        self.pid = PIDController(1.0, 0.0, 0.0)
        self.last_motor_voltage = 0.0

        # configuration
        self.min_distance_to_cars = 100
    
    """
    This drives the car. It should be called when the tracking has a new position for the car.
    The car will then given the previous set route drive to this destination. 
    (Checks for traffic rules etc.)
    """
    def step(self, position, speed, cars_on_same_lane, dt):
        self.position = position

        possible_to_change_switch = True
        motor_voltage = 0.0
        # here we control speed dependant stuf
        if self.active:
            if len(cars_on_same_lane) > 0:
                # there are cars on the same lane
                smallest_distance = 2000
                for other_car in cars_on_same_lane:
                    # if both cars are on the same edge
                    if map.edges[other_car.position[0]][1] == map.edges[self.position[0]][1]:
                        # there are cars in front of us on the same lane
                        possible_to_change_switch = False
                        distance_to_other_car = other_car.position[1] - self.position[1]
                        actual_distance = distance_to_other_car * sum(map.length_for_edge(self.position[0], config.MAP_SCALE))
                        if actual_distance < smallest_distance:
                            smallest_distance = actual_distance
                    else:
                        # cars are on different edges, so calculate distance to end of edge
                        distance_to_node = (1.0 - self.position[1]) * sum(map.length_for_edge(self.position[0], config.MAP_SCALE))
                        distance_node_to_other_car = other_car.position[1] * sum(map.length_for_edge(other_car.position[0], config.MAP_SCALE))
                        actual_distance = distance_to_node + distance_node_to_other_car
                        # check if we are on the same route
                        heading_node_other_car = map.edges[other_car.position[0]][1]
                        # if the heading node of the other car is the next node on our route
                        if len(self.route) > 1 and heading_node_other_car == self.route[1]:
                            if self.name == "P2" :
                                print(f"{other_car.name} is in front on other edge")
                            if actual_distance < smallest_distance:
                                smallest_distance = actual_distance
                        else:
                            # we only consider it, if the distance is less than 10, since it might be that it could come to a crash
                            if actual_distance < 10 and actual_distance < smallest_distance:
                                smallest_distance = actual_distance
                        
                # now we have the smallest distance to another car
                # use PID controller to slow down
                motor_voltage = abs(self.pid.update(self.min_distance_to_cars, smallest_distance, dt))
                if self.name == "P2" :
                    print(f"{self.name} {motor_voltage} {smallest_distance} {[car.name for car in cars_on_same_lane]}")
            else:
                # no cars on the same lane
                # check for traffc rules when near intersection
                #if position[1] > 0.9:
                motor_voltage = 300

            # set speed
            self.controller.send_motor_message(self.name, motor_voltage)
            self.last_motor_voltage = motor_voltage


        # if the car comes up to an intersection (e.g. progress is over 90%)
        # we want to change the switch and maybe need to wait for other cars
        if position[1] > 0.9 and self.state == 'on_route' and self.changed_switch == False and possible_to_change_switch: 
            self.__control_switch_for_route()
            self.changed_switch = True

        if position[1] < 0.1:
            self.changed_switch = False
            if self.state == 'almost_there':
                # we reached our destination
                self.state = 'waiting'

    def set_as_active(self, hostname):
        self.active = True
        self.hostname = hostname
        self.controller.add_car_controller(self.name, self.hostname)
        self.controller.send_light_message(self.name, HEADLIGHT_ON, REAR_ON, BLINKER_OFF)

    def __control_switch_for_route(self):
        heading_towards_node = self.route.pop(0)
        if len(self.route) == 0:
            # we are heading towards the destination
            self.state = 'almost_there'
            return
        next_intersection_node = self.route[0]
        edge_to_take = heading_towards_node + next_intersection_node # string concatenation
        direction_on_intersection = map.edges[edge_to_take][2]
        self.controller.set_switch(heading_towards_node, direction_on_intersection)

    def set_destination(self, node):
        self.route = pathplanner.plan_route_to(node, self.position[0])
        self.state = 'on_route'
        print("new route for car " + self.name + ": " + str(self.route))

    def __eq__(self, other):
        return self.name == other.name
    