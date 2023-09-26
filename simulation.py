from car import Car
import time
import map

class Simulation:
    def __init__(self, car_tracking, map_scale):
        self.car_tracking = car_tracking
        self.map_scale = map_scale
        self.last_step = time.time()
        self.switch_states = {
            'A1': 'left',
            'A2': 'left',
            'A3': 'right',
            'B1': 'right',
            'B2': 'left',
            'B3': 'right',
            'C1': 'right',
            'C2': 'left',
            'C3': 'left',
            'D1': 'left',
            'D2': 'left',
            'D3': 'right'
        }

        # cars already tracked, starting positions
        self.cars = [
            ("P1", ("C3A1", 0.7), 0),
            ("P2", ("B1D2", 0.4), 0),
            ("L1", ("A2B1", 0.1), 0),
            ("L2", ("D1C3", 0.7), 0),
            ("L3", ("C3A1", 0.6), 0),
        ]

        self.car_max_voltages = {
            "P1": 250,
            "P2": 300,
            "L1": 250,
            "L2": 250,
            "L3": 300
        }

    def set_switch(self,name,dir):
        self.switch_states[name] = dir
    
    def get_last_car_tracking_status(self):
        return self.car_positions
    
    def set_motor_voltage(self, car_name, voltage):
        # simulate voltage to speed
        if voltage > self.car_max_voltages[car_name]:
            voltage = self.car_max_voltages[car_name]
        speed = 0.001 * voltage**2
        for index, car in enumerate(self.cars):
            if car[0] == car_name:
                self.cars[index] = (car[0], car[1], speed)

    def step(self):
        # get the delta time between the steps
        delta_time = time.time() - self.last_step

        # calculate the new positions of the cars
        for index, car in enumerate(self.cars):
            # get length of current edge
            length = sum(map.length_for_edge(car[1][0], self.map_scale))
            # calculate step size according to length
            step_size = car[2] * delta_time / length
            # calculate new progress of the car
            progress = car[1][1] + step_size
            edge = car[1][0]
            if progress > 1.0:
                progress = progress - 1.0
                # we need to find the next edge by looking at the switch states
                current_node = map.edges[edge][1]
                direction = self.switch_states[current_node]
                for edge, (start, end, dir) in map.edges.items():
                    if start == current_node and dir == direction:
                        edge = edge
                        break
            self.cars[index] = (car[0], (edge, progress), car[2])
        # update the car tracking
        self.car_tracking.update_cars(self.cars)

        self.last_step = time.time()
    