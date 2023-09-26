from car import Car
import map
import time

class CarTracking:
    def __init__(self, controller):
        self.cars = [] # list of cars
        self.controller = controller
        self.active_cars = [] # list of cars that are currently active
        self.dummy_cars = [] # list of cars that cannot be controlled
        self.last_update = time.time()

    def get_cars(self):
        return self.cars
    
    def get_unkown_cars(self):
        # return cars that are not in active_cars or dummy_cars
        cars = []
        for car in self.cars:
            if car.name not in self.active_cars and car.name not in self.dummy_cars:
                cars.append(car)
        return cars
    
    def make_car_active(self, car, hostname):
        self.active_cars.append(car.name)
        car.set_as_active(hostname)
    
    def make_car_dummy(self, car):
        self.dummy_cars.append(car.name)

    def update_cars(self, car_list):
        dt = time.time() - self.last_update
        self.last_update = time.time()

        for car_tuple in car_list:
            found_car = False
            for car in self.cars:
                # if the car is already tracked, update its position
                if car.name == car_tuple[0]:
                    # calculate speed of car
                    # calculate the next step of the car
                    car.step(car_tuple[1], car_tuple[2], self.get_cars_ahead(car), dt)
                    found_car = True
            if not found_car:
                self.cars.append(Car(car_tuple[0], car_tuple[1], self.controller))
    
    """
    Checks if there are cars ahead of the given car and returns a list of them.
    Looks only on current lane of the car and not on the other lanes.
    """
    def get_cars_ahead(self, car):
        cars_ahead = []
        # get edges connected to the current edge
        nodes_to_check = [map.edges[edge][1] for edge in map.get_connected_edges(car.position[0])]
        nodes_to_check.append(map.edges[car.position[0]][1])

        for other_car in self.cars:
            if other_car == car:
                continue
            if map.edges[other_car.position[0]][1] in nodes_to_check:
                # the other car is on the same lane
                if other_car.position[1] > car.position[1]:
                    cars_ahead.append(other_car)
        return cars_ahead

    def __convert_car_position(self, real_world_position):
        pass
        # TODO: convert the car positions from the real world coordinate system to the topological map
