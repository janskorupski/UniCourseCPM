import numpy as np
import pymunk
import pygame
from pygame.locals import *
import pymunk.pygame_util
import Human
import Newb
import math
import random
import time
import Net

# GLOBAL VARIABLES
PLAYER_CATEGORY = 0b0001
WALL_CATEGORY   = 0b0010
APPLE_CATEGORY  = 0b0100
ALL_CATEGORIES  = [PLAYER_CATEGORY, WALL_CATEGORY, APPLE_CATEGORY]
PLAYER_COLLISION_TYPE = 1
APPLE_COLLISION_TYPE = 2
WIDTH, HEIGHT = SIZE =  (800, 400)
CENTER = (WIDTH//2, HEIGHT//2)


class VirtualEnvironment:

    def __init__(self, players, n_obstacles=15, game_mode=False, seed=None):

        self.seed = seed
        if seed is not None:
            random.seed(seed)

        # GAME SETTINGS
        self.in_game_time = 0
        self.max_time = 600

        # GAME OBJECTS
        self.players = players  # for now this should always be a list of length 1 with one object of type Player
        self.apple = None

        # Radius of player
        self.R = self.players[0].shape.radius  # To fit everythg on the plane

        # to watch game
        self.game_mode = game_mode

        # Creates plane with walls, players, obstacles, apples
        self.create_room(n_obstacles)

        if self.game_mode: self.start_pygame() 

            
    def create_room(self, n_obstacles):

        self.space = pymunk.Space()
        
        self.space.gravity = (0, 0)
        
        self.insert_walls()
        
        self.insert_players()
        
        self.insert_apples()
        
        self.insert_obstacles(n_obstacles)

        handler = self.space.add_collision_handler(PLAYER_COLLISION_TYPE, APPLE_COLLISION_TYPE)
        handler.begin = self.player_apple_collision


    def insert_walls(self): 
        static_walls = [
            pymunk.Segment(self.space.static_body, (0, 0), (0, HEIGHT), 5), # left
            pymunk.Segment(self.space.static_body, (0, 0), (WIDTH, 0), 5), # bottom
            pymunk.Segment(self.space.static_body, (WIDTH, HEIGHT), (0, HEIGHT), 5), # top
            pymunk.Segment(self.space.static_body, (WIDTH, HEIGHT), (WIDTH, 0), 5), # right 
        ]

        for s in static_walls:
            s.friction = 1.0
            s.filter = pymunk.ShapeFilter(categories=WALL_CATEGORY)
            
        self.space.add(*static_walls)


    def insert_players(self):
        for player in self.players:
            player.body.position = self.get_position('player')
            player.shape.collision_type = PLAYER_COLLISION_TYPE
            player.space = self
            self.space.add(player.body, player.shape)


    def insert_obstacles(self, n_obstacles):

        self.obstacle_size = (self.R * 2, self.R * 2)  

        self.obstacles = []

        for obstacle in range(n_obstacles): 
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = self.get_position('obstacle')
                    # Create a box shape attached to the new body
            obstacle = pymunk.Poly.create_box(body, self.obstacle_size)
            obstacle.friction = 0
            obstacle.filter = pymunk.ShapeFilter(categories=WALL_CATEGORY)
            
            # Add the body and shape to the space and to the obstacles list
            self.space.add(body, obstacle)
            self.obstacles.append(obstacle)


    def insert_apples(self):
        
        self.apple_radius = self.R // 2 

        self.apple = pymunk.Circle(self.space.static_body, radius=self.apple_radius)
        self.apple.body.position = self.get_position('apple')
        
        self.apple.friction = .5
        self.apple.filter = pymunk.ShapeFilter(categories=APPLE_CATEGORY)
        self.apple.collision_type = APPLE_COLLISION_TYPE


        self.space.add(self.apple)
    

    def get_position(self, element:str) -> tuple[int, int]: 
        '''This function works for all objects. \n 
        It checks if specified element's shape can be fitted to the plane
        considering elements already placed in the plane'''
        
        # Not elegant. Just enlarge the shape of fitted element  
        # to make sure that they are spread wide enough  
        # Shape of element is not changed outside of the foo
        constant = 2 if element=='player' else 1 if element=='apple' else 6 

        buffer_size  = (self.R * constant,) * 2 # tuple[int, int]

      # Repeat until a free space is found
        while True:
            # Random position within the boundaries
            position = (random.randint(buffer_size[0], WIDTH - buffer_size[0]), 
                        random.randint(buffer_size[1], HEIGHT - buffer_size[1]))

            # Create a temporary shape at the position
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = position
            free_space = pymunk.Poly.create_box(body, buffer_size)
            
            # Check if it collides with anything in the space
            if not self.space.shape_query(free_space):
                return position  # Return the free position if no collisions

            # Clean up temporary objects not added to space
            del body
            del free_space

    
    def player_apple_collision(self, arbiter, space, data):
        print("Collected")
        # Optionally, remove the apple from the space if it's a one-time collectible
        space.remove(arbiter.shapes[1], arbiter.shapes[1])
        
        for player in self.players: 
            player.add_point()

        self.insert_apples()

        # return True  # Return True to process the collision


    def start_pygame(self) -> None: 
        '''display the experiment'''
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.running = False # ? 


    def calculate_step(self):
        
        for player in self.players:

            output = player.get_motor_output()
            player.body.apply_force_at_local_point((output[0], 0))
            player.body.angular_velocity = output[1]
            # print([round(num, 2) for num in player.get_sensory_input(debug=True)])
            player.body.velocity = player.body.velocity * 0.95  # this is a temporary bodge

        self.space.step(1 / 60.0)
        self.in_game_time += 1


    def calculate_full_simulation(self):
        # use self.calculate_step and player.get_motor_output in a loop until some conditions are met
        if self.game_mode:
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        running = False

                # Step the simulation
                self.calculate_step()

                # Clear the screen
                self.screen.fill((255, 255, 255))

                # Draw the space
                self.space.debug_draw(self.draw_options)

                # Update the display
                pygame.display.flip()

                # Cap the frame rate
                self.clock.tick(600)
        else:
            start_time = time.time()
            running = True
            while self.in_game_time < self.max_time:

                # Step the simulation
                self.calculate_step()



    def fitness_function(self):
        for player in self.players:

            apples_eaten = player.points

            distance_from_apple = player.body.position.get_distance(self.apple.body.position)
            max_distance = math.sqrt(WIDTH**2 + HEIGHT**2)
            distance_score = math.exp(-3*distance_from_apple/max_distance)

            fitness = apples_eaten + distance_score
            player.fitness = fitness





    def calculate_distance_from_apple(self, player):
        pass


if __name__ == "__main__":
    # player = Human.Human()
    # player = Human.Human()
    # player = Newb.Newb()
    player = Net.Net(parameters=np.random.random(900))
    # player = Net.Net(parameters=np.arange(900, dtype="float"))
    env1 = VirtualEnvironment(players=[player], game_mode=True, seed=1234)
    env1.calculate_full_simulation()
    env1.fitness_function()
    print(player.fitness)
