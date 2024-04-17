import numpy as np
import pymunk
import pygame
from pygame.locals import *
import pymunk.pygame_util
import Human
import math
import Newb

# GLOBAL VARIABLES
PLAYER_CATEGORY = 0b0001
WALL_CATEGORY   = 0b0010
APPLE_CATEGORY  = 0b0100
ALL_CATEGORIES  = [PLAYER_CATEGORY, WALL_CATEGORY, APPLE_CATEGORY]

class VirtualEnvironment:

    def __init__(self, players, game_mode=True):
        self.players = players  # for now this should always be a list of length 1 with one object of type Player
        self.space = pymunk.Space()
        self.space.gravity = (0, 0)
        self.game_mode = game_mode
        self.wall = None

        self.create_room()
        self.insert_players()
        if self.game_mode:
            pygame.init()
            self.screen = pygame.display.set_mode((600, 400))
            self.clock = pygame.time.Clock()
            self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
            self.running = False

    def insert_wall(self, position_x, position_y):
        pass

    def insert_apple(self, position):
        pass

    def insert_obstacle(self, position):
        pass

    def check_if_enough_space(self, shape):
        # shape = pymunk.Shape()
        pass

    def create_room(self):
        ''' Uses self.insert_players, self.insert_apple, self.inset_wall to randomly  '''

        platform_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        platform_shape = pymunk.Segment(platform_body, (0, 0), (600, 0), 5)
        platform_shape.friction = 1  # Adjust friction if needed
        platform_shape.filter = pymunk.ShapeFilter(categories=WALL_CATEGORY)
        self.wall = platform_shape
        self.space.add(platform_body, platform_shape)

        platform_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        platform_shape = pymunk.Segment(platform_body, (600, 0), (600, 400), 5)
        platform_shape.friction = 1  # Adjust friction if needed
        platform_shape.filter = pymunk.ShapeFilter(categories=WALL_CATEGORY)
        self.space.add(platform_body, platform_shape)

        platform_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        platform_shape = pymunk.Segment(platform_body, (600, 400), (0, 400), 5)
        platform_shape.friction = 1  # Adjust friction if needed
        platform_shape.filter = pymunk.ShapeFilter(categories=WALL_CATEGORY)
        self.space.add(platform_body, platform_shape)

        platform_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        platform_shape = pymunk.Segment(platform_body, (0, 400), (0, 0), 5)
        platform_shape.friction = 1  # Adjust friction if needed
        platform_shape.filter = pymunk.ShapeFilter(categories=WALL_CATEGORY)
        self.space.add(platform_body, platform_shape)

    def insert_players(self, position=(200, 200)):
        for player in self.players:
            player.body.position = position
            self.space.add(player.body, player.shape)

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

    def plot_game_state(self):
        pass


if __name__ == "__main__":
    # player = Human.Human()
    player = Newb.Newb()
    env = VirtualEnvironment(players=[player])
    env.calculate_full_simulation()
