import pygame
import map
import config

# Colors
WHITE = (255, 255, 255)
LANES = (145, 140, 163)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255,255,0)
BLUE = (0,0,255)

def render(screen, cars, controller, selected_car):
    screen.fill(BLACK)
    # Draw the map
    for edge in map.edges:
        coordinates = [(x + config.MAP_MARGIN_LEFT, y + config.MAP_MARGIN_TOP) for x, y in config.edge_coordinates[edge]]
        pygame.draw.lines(screen, LANES, False, coordinates, 2)

    # draw status of switches
    for switch in map.nodes.keys():
        x, y = map.nodes[switch]
        x, y = x*config.MAP_SCALE+config.MAP_MARGIN_LEFT, y*config.MAP_SCALE+config.MAP_MARGIN_TOP

        box_width = 20
        box_offset = 10

        if map.node_orientation[switch] == 'north':
            if controller.get_switch_state(switch) == 'left':
                pygame.draw.rect(screen, GREEN, (x-box_offset, y-box_offset, box_offset, box_width))
                pygame.draw.rect(screen, RED, (x, y-box_offset, box_offset, box_width))
            else:
                pygame.draw.rect(screen, RED, (x-box_offset, y-box_offset, box_offset, box_width))
                pygame.draw.rect(screen, GREEN, (x, y-box_offset, box_offset, box_width))
        elif map.node_orientation[switch] == 'south':
            if controller.get_switch_state(switch) == 'left':
                pygame.draw.rect(screen, RED, (x-box_offset, y-box_offset, box_offset, box_width))
                pygame.draw.rect(screen, GREEN, (x, y-box_offset, box_offset, box_width))
            else:
                pygame.draw.rect(screen, GREEN, (x-box_offset, y-box_offset, box_offset, box_width))
                pygame.draw.rect(screen, RED, (x, y-box_offset, box_offset, box_width))
        elif map.node_orientation[switch] == 'east':
            if controller.get_switch_state(switch) == 'left':
                pygame.draw.rect(screen, GREEN, (x-box_offset, y-box_offset, box_width, box_offset))
                pygame.draw.rect(screen, RED, (x-box_offset, y, box_width, box_offset))
            else:
                pygame.draw.rect(screen, RED, (x-box_offset, y-box_offset, box_width, box_offset))
                pygame.draw.rect(screen, GREEN, (x-box_offset, y, box_width, box_offset))
        elif map.node_orientation[switch] == 'west': 
            if controller.get_switch_state(switch) == 'left':
                pygame.draw.rect(screen, RED, (x-box_offset, y-box_offset, box_width, box_offset))
                pygame.draw.rect(screen, GREEN, (x-box_offset, y, box_width, box_offset))
            else:
                pygame.draw.rect(screen, GREEN, (x-box_offset, y-box_offset, box_width, box_offset))
                pygame.draw.rect(screen, RED, (x-box_offset, y, box_width, box_offset))

    # draw cars
    for car in cars:
        edge, progress = car.position
        # given the map edge and the progress on that edge, calculate the position of the car
        coordinates = config.edge_coordinates[edge]
        # calculate the length of each edge in coordinates
        edge_lengths = config.edge_cost[edge]
        # calculate the total length of the edge
        total_length = sum(edge_lengths)
        # calculate the position of the car on the edge
        car_position = progress*total_length
        # find the edge where the car is
        edge_index = 0
        while car_position > edge_lengths[edge_index]:
            car_position -= edge_lengths[edge_index]
            edge_index += 1
        # calculate the position of the car on the edge
        (x1, y1), (x2, y2) = coordinates[edge_index], coordinates[edge_index+1]
        car_x = x1 + car_position*(x2-x1)/(edge_lengths[edge_index]+0.0001)
        car_y = y1 + car_position*(y2-y1)/(edge_lengths[edge_index]+0.0001)
        car_x, car_y = car_x + config.MAP_MARGIN_LEFT, car_y + config.MAP_MARGIN_TOP
        car.visual.x, car.visual.y = car_x, car_y
        car.visual.draw(screen)

    # draw route of selected car
    if selected_car:
        edges = list(zip(selected_car.route[:-1], selected_car.route[1:]))
        for edge in edges:
            edge = ''.join(edge)
            coordinates = [(x + config.MAP_MARGIN_LEFT, y + config.MAP_MARGIN_TOP) for x, y in config.edge_coordinates[edge]]
            pygame.draw.lines(screen, selected_car.visual.color, False, coordinates, 2)
        # now draw line from car position to first node
        edge, progress = selected_car.position
        coordinates = [(x + config.MAP_MARGIN_LEFT, y + config.MAP_MARGIN_TOP) for x, y in config.edge_coordinates[edge]]
        edge_lengths = config.edge_cost[edge]
        total_length = sum(edge_lengths)
        car_position = progress*total_length
        edge_index = 0
        while car_position > edge_lengths[edge_index]:
            car_position -= edge_lengths[edge_index]
            edge_index += 1
        # position of car on edge
        (x1, y1), (x2, y2) = coordinates[edge_index], coordinates[edge_index+1]
        car_x = x1 + car_position*(x2-x1)/(edge_lengths[edge_index]+0.0001)
        car_y = y1 + car_position*(y2-y1)/(edge_lengths[edge_index]+0.0001)
        # add all the coordinates of the edges from this edge to end of edge
        coordinates = coordinates[edge_index+1:]
        coordinates.insert(0, (car_x, car_y))
        pygame.draw.lines(screen, selected_car.visual.color, False, coordinates, 2)


    pygame.display.flip()

class CarCircle:
    def __init__(self,name):
        self.x = 0
        self.y = 0
        self.name = name
        self.radius = 10
        if name[0] == 'P':
            self.color = BLUE
        elif name[0] == 'L':
            self.color = YELLOW
        else:
            self.color = GREEN
        self.cur_color = self.color
        self.blinking = False
        self.blink_counter = 0
        self.blink_max = 10
    
    def draw(self, screen):
        if self.blinking:
            self.blink_counter += 1
            if self.blink_counter >= self.blink_max:
                self.blink_counter = 0
                if self.cur_color == self.color:
                    self.cur_color = BLACK
                else:
                    self.cur_color = self.color
        else:
            self.cur_color = self.color
        pygame.draw.circle(screen, self.cur_color, (int(self.x), int(self.y)), self.radius)