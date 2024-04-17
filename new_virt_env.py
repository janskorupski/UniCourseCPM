import numpy as np
import pymunk
import pygame
from pygame.locals import *
import pymunk.pygame_util
import Human
import Newb
import math
import random

# GLOBAL VARIABLES
PLAYER_CATEGORY = 0b0001
WALL_CATEGORY   = 0b0010
APPLE_CATEGORY  = 0b0100
ALL_CATEGORIES  = [PLAYER_CATEGORY, WALL_CATEGORY, APPLE_CATEGORY]
PLAYER_COLLISION_TYPE = 1
APPLE_COLLISION_TYPE = 2
WIDTH, HEIGHT = SIZE =  (800,400) 
CENTER = (WIDTH//2, HEIGHT//2)


class VirtualEnvironment:

    def __init__(self, players, n_obstacles=15, game_mode=True):

        self.players = players  # for now this should always be a list of length 1 with one object of type Player

        # Radius of player
        self.R = self.players[0].shape.radius  # To fit everyth. on the plane
        
        # Creates plane with walls, players, obstacles, apples
        self.create_room(n_obstacles)

        # to watch game
        self.game_mode = game_mode  


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

        apple = pymunk.Circle(self.space.static_body, radius=self.apple_radius, 
                              offset=self.get_position('apple'))
        
        apple.friction = .5
        apple.filter = pymunk.ShapeFilter(categories=APPLE_CATEGORY)
        apple.collision_type = APPLE_COLLISION_TYPE 

        self.space.add(apple)
    

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
            print(1)

    
    def player_apple_collision(self, arbiter, space, data):
        print("Collected")
        # Optionally, remove the apple from the space if it's a one-time collectible
        # space.remove(arbiter.shapes[0], arbiter.shapes[1].body, arbiter.shapes[1])
        # self.insert_apple(self)
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
                self.clock.tick(60)


    def calculate_distance_from_apple(self, player):
        pass


if __name__ == "__main__":
    # player = Human.Human()
    player = Newb.Newb()
    env = VirtualEnvironment(players=[player])
    env.calculate_full_simulation()
