import map 

MAP_SCALE = 1000
MAP_MARGIN_LEFT = 50
MAP_MARGIN_TOP = 50
SCREEN_WIDTH, SCREEN_HEIGHT = 2*MAP_SCALE + 2*MAP_MARGIN_LEFT, MAP_SCALE + 2*MAP_MARGIN_TOP

edge_coordinates = {edge: map.coordinates_for_edge_line(edge, MAP_SCALE) for edge in map.edges}
edge_cost = {edge: map.length_for_edge(edge, MAP_SCALE) for edge in map.edges}