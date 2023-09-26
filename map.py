offset = 0.05

nodes = {
    "A1": (1.0+offset, 0.0),
    "A2": (1.0-2*offset, 0.0+offset),
    "A3": (1.0, 0.0+2*offset),
    "B1": (1.0-offset, 0.5-offset),
    "B2": (1.0-2*offset, 0.5+offset),
    "B3": (1.0, 0.5+2*offset),
    "C1": (1.0-offset, 1.0-2*offset),
    "C2": (1.0+offset, 1.0-offset),
    "C3": (1.0-2*offset, 1.0),
    "D1": (0.0, 0.5-offset),
    "D2": (0.0+2*offset, 0.5),
    "D3": (0.0+offset, 0.5+2*offset)
}

node_orientation = {
    "A1": "west",
    "A2": "east",
    "A3": "north",
    "B1": "south",
    "B2": "east",
    "B3": "north",
    "C1": "south",
    "C2": "west",
    "C3": "east",
    "D1": "south",
    "D2": "west",
    "D3": "north"
}

# with respect to direction of travel
edges = {
    "A1B1": ("A1", "B1", 'left'),
    "A1D1": ("A1", "D1", 'right'),
    "A2B1": ("A2", "B1", 'right'),
    "A2C2": ("A2", "C2", 'left'),
    "A3C2": ("A3", "C2", 'right'),
    "A3D1": ("A3", "D1", 'left'),

    "B1C1": ("B1", "C1", 'left'),
    "B1D2": ("B1", "D2", 'right'),
    "B2C1": ("B2", "C1", 'right'),
    "B2A3": ("B2", "A3", 'left'),
    "B3A3": ("B3", "A3", 'right'),
    "B3D2": ("B3", "D2", 'left'),

    "C1D3": ("C1", "D3", 'right'),
    "C1A1": ("C1", "A1", 'left'),
    "C2D3": ("C2", "D3", 'left'),
    "C2B3": ("C2", "B3", 'right'),
    "C3B3": ("C3", "B3", 'left'),
    "C3A1": ("C3", "A1", 'right'),

    "D1B2": ("D1", "B2", 'left'),
    "D1C3": ("D1", "C3", 'right'),
    "D2A2": ("D2", "A2", 'right'),
    "D2C3": ("D2", "C3", 'left'),
    "D3A2": ("D3", "A2", 'left'),
    "D3B2": ("D3", "B2", 'right')
}

edge_cost = {}

# additional nodes to layout the road more precisely
edge_layout = {
    # roads
    "A1D1": [(0.0,0.0)],
    "A3D1": [(1.0,0.0),(0.0,0.0)],
    "D3A2": [(0.0+offset,0.0+offset)],
    "D2A2": [(0.0+offset, 0.5),(0.0+offset,0.0+offset)],

    "C3A1": [(2.0,1.0), (2.0,0.5), (1.5,0.5), (1.5,0.0)],
    "C1A1": [(1.0-offset, 1.0),(2.0,1.0), (2.0,0.5), (1.5,0.5), (1.5,0.0)],
    "A2C2": [(1.5-offset,0.0+offset), (1.5-offset,0.5+offset), (2.0-offset,0.5+offset), (2.0-offset,1.0-offset)],
    "A3C2": [(1.0,0.0+offset),(1.5-offset,0.0+offset), (1.5-offset,0.5+offset), (2.0-offset,0.5+offset), (2.0-offset,1.0-offset)],

    "D1C3": [(0.0,1.0)],
    "D2C3": [(0.0,0.5),(0.0,1.0)],
    "C2D3": [(0.0+offset,1.0-offset)],
    "C1D3": [(1.0-offset,1.0-offset),(0.0+offset,1.0-offset)],

    "B2A3": [(1.0,0.5+offset)],
    "A2B1": [(1.0-offset,0.0+offset)],
    "A1B1": [(1.0-offset, 0.0)],

    "B2C1": [(1.0-offset,0.5+offset)],
    "C2B3": [(1.0,1.0-offset)],
    "C3B3": [(1.0,1.0)],

    "B1D2": [(1.0-offset,0.5)],
    "B3D2": [(1.0,0.5)],
    "D3B2": [(0.0+offset,0.5+offset)],
    "D1B2": [(0.0,0.5+offset)],
}

# given a list of nodes, all the coordinates are returned for the edge between them
# the edge_layout will be used to make corners at these points with a 45 deg angled line
def coordinates_for_edge_line(edge, map_scale):
    start, end,_ = edges[edge]
    start_x, start_y = nodes[start]
    start_x, start_y = start_x*map_scale, start_y*map_scale
    coordinates = [(start_x, start_y)]
    if edge in edge_layout:
        addtitional_nodes = edge_layout[edge] + [nodes[end]]
        # given the start point and the additional_nodes, create two coordinates per node so that a line between them is 45 deg
        angle_line_length = 2*map_scale*offset-1
        for node in addtitional_nodes:
            x, y = node
            x, y = x*map_scale, y*map_scale
            # check direction of edge between start and current node
            if start_x < x:
                # going right
                if (x-start_x) > 2*map_scale*offset:
                    coordinates.append((start_x + angle_line_length, start_y))
                if (x-start_x) < angle_line_length:
                    angle_line_length = map_scale*offset
                else:
                    angle_line_length = 2*map_scale*offset-1
                coordinates.append((x - angle_line_length, y))
            elif start_x > x:
                # going left
                if (start_x-x) > 2*map_scale*offset:
                    coordinates.append((start_x - angle_line_length, start_y))
                if (start_x-x) < angle_line_length:
                    angle_line_length = map_scale*offset
                else:
                    angle_line_length = 2*map_scale*offset-1
                coordinates.append((x + angle_line_length, y))
            elif start_y < y:
                # going down
                if (y-start_y) > 2*map_scale*offset:
                    coordinates.append((start_x, start_y + angle_line_length))
                if (y-start_y) < angle_line_length:
                    angle_line_length = map_scale*offset
                else:
                    angle_line_length = 2*map_scale*offset-1
                coordinates.append((x, y - angle_line_length))
            elif start_y > y:
                # going up
                if (start_y-y) > 2*map_scale*offset:
                    coordinates.append((start_x, start_y - angle_line_length))
                if (start_y-y) < angle_line_length:
                    angle_line_length = map_scale*offset
                else:
                    angle_line_length = 2*map_scale*offset-1
                coordinates.append((x, y + angle_line_length))
            start_x, start_y = x, y  
    end_x, end_y = nodes[end]
    end_x, end_y = end_x*map_scale, end_y*map_scale
    coordinates.append((end_x, end_y))
    return coordinates

def length_for_edge(edge, map_scale):
    coordinates = coordinates_for_edge_line(edge, map_scale)
    edge_lengths = [((x1-x2)**2 + (y1-y2)**2)**0.5 for (x1, y1), (x2, y2) in zip(coordinates[:-1], coordinates[1:])]
    return edge_lengths

def get_connected_edges(edge):
    end_node_of_edge = edges[edge][1]
    connected_edges = []
    for edge_name, (start, end, _) in edges.items():
        if start == end_node_of_edge:
            connected_edges.append(edge_name)
    return connected_edges