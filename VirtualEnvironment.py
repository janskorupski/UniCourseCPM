import numpy as np
import Player
import pymunk
import pygame
from pygame.locals import *
import pymunk.pygame_util
import Human


class VirtualEnvironment:

    def __init__(self, players, game_mode=True):
        self.players = players  # for now this should always be a list of length 1 with one object of type Player
        self.space = pymunk.Space()
        self.space.gravity = (0,0)
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

    def create_room(self):
        # Create a static platform (segment shape)
        platform_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        platform_shape = pymunk.Segment(platform_body, (0, 0), (600, 0), 5)
        platform_shape.friction = 1  # Adjust friction if needed
        self.wall = platform_shape
        self.space.add(platform_body, platform_shape)

        # Create a static platform (segment shape)
        platform_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        platform_shape = pymunk.Segment(platform_body, (600, 0), (600, 400), 5)
        platform_shape.friction = 1  # Adjust friction if needed
        self.space.add(platform_body, platform_shape)

        # Create a static platform (segment shape)
        platform_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        platform_shape = pymunk.Segment(platform_body, (600, 400), (0, 400), 5)
        platform_shape.friction = 1  # Adjust friction if needed
        self.space.add(platform_body, platform_shape)

        # Create a static platform (segment shape)
        platform_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        platform_shape = pymunk.Segment(platform_body, (0, 400), (0, 0), 5)
        platform_shape.friction = 1  # Adjust friction if needed
        self.space.add(platform_body, platform_shape)

    def insert_players(self):
        for player in self.players:
            player.body.position = (200, 200)
            self.space.add(player.body, player.shape)

    def calculate_step(self):
        for player in self.players:

            output = player.get_motor_output()
            player.body.apply_force_at_local_point((0, -output[0]))
            player.body.apply_force_at_local_point((0, output[2]))
            player.body.angular_velocity = output[3] - output[1]

            player.body.velocity = player.body.velocity*0.95  # this is a temporary bodge

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

    def calculate_reward(self) -> float:
        pass

    def get_sensory_data(self) -> np.ndarray:
        # dummy return
        return np.array([5., 5., 4., 3., 4., 5., 1., # odległość od punktu
                0,0,1,1,1,0,2]) # jaki rodzaj obiektu (np. 0-nic, 1-ściana, 2-jabłko)

    def plot_game_state(self):
        pass

if __name__ == "__main__":
    player = Human.Human()
    env = VirtualEnvironment(players=[player])
    env.calculate_full_simulation()