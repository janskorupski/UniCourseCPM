import numpy as np
import pymunk
import math
# GLOBAL VARIABLES
PLAYER_CATEGORY = 0b0001
WALL_CATEGORY   = 0b0010
APPLE_CATEGORY  = 0b0100
ALL_CATEGORIES  = [PLAYER_CATEGORY, WALL_CATEGORY, APPLE_CATEGORY]

class Player:

    def __init__(self, parameters=None):
        # 'parameters' are the parameters of the neural network (weights and biases).
        # For every player, these parameters are fixed, as they will be generate by GA.
        # self.nn=new_neural_network(parameters)

        self.points = 0

        # SENSOR SETTINGS
        self.visual_resolution = 7  # number of sensors
        self.field_of_view = math.pi  # in radians
        self.rays = []

        # PYMUNK SETTINGS
        radius = 10
        mass = 1
        moment = pymunk.moment_for_circle(mass, 0, radius)
        self.body = pymunk.Body(mass, moment)

        self.shape = pymunk.Circle(self.body, radius)
        self.shape.friction = 0.1
        self.shape.filter = pymunk.ShapeFilter(categories=0b1)

    def get_motor_output(self, sensory_input: np.ndarray) -> np.ndarray:
        # the neural networks (simply the forwards propagation)
        pass

    def get_sensory_input(self, debug=False):
        # debug displays the sensor rays in the window

        sensory_input = np.array([])
        offset_angles = [self.field_of_view*(-1/2 + i/(self.visual_resolution-1)) for i in range(self.visual_resolution)]
        while len(self.rays):
            self.body.space.remove(self.rays.pop())
        for angle_offset in offset_angles:
            sensory_input = np.append(sensory_input, self.get_singular_sensor_data(angle_offset=angle_offset,
                                                                                   debug=debug))
        return sensory_input

    def get_singular_sensor_data(self, angle_offset=0, max_length=150, debug=False):
        angle = self.body.angle + angle_offset
        looking_direction = pymunk.vec2d.Vec2d(math.cos(angle), math.sin(angle))

        only_player_mask = pymunk.ShapeFilter.ALL_MASKS() ^ PLAYER_CATEGORY
        filter_mask_player = pymunk.shape_filter.ShapeFilter(mask=only_player_mask)
        query = self.body.space.segment_query_first(self.body.position,
                                                    self.body.position + looking_direction * max_length,
                                                    1,
                                                    filter_mask_player
                                                    )
        if debug:
            ray_body = pymunk.Body(body_type=pymunk.Body.STATIC)
            ray_shape = pymunk.Segment(ray_body,
                                       self.body.position,
                                       self.body.position + looking_direction * max_length,
                                       1)
            ray_shape.filter = pymunk.ShapeFilter(categories=0)
            self.rays.append(ray_shape)
            self.rays.append(ray_body)
            self.body.space.add(ray_body, ray_shape)
        if query is None:
            return np.array([1, 0])

        categories = query.shape.filter.categories
        if categories in ALL_CATEGORIES:
            return np.array([query.alpha, categories])  # currently the categories here are powers of 2 (1, 2, 4, 8, ...)
        else:
            return np.array([query.alpha, 0])

    def calculate_shortest_distance_from_apple(self):
        # Jan
        pass

    def fitness_function(self):
        return self.points + 1 - math.atan(self.calculate_shortest_distance_from_apple())/math.pi*2

