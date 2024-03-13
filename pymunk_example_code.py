import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

# Create a space
space = pymunk.Space()
space.gravity = (0, 0)  # Set gravitational force

# Create a circle body and add it to the space
radius = 30
mass = 1
moment = pymunk.moment_for_circle(mass, 0, radius)
circle_body = pymunk.Body(mass, moment)
circle_body.position = (300, 200)  # Initial position
circle_body.angular_velocity = 10
circle_shape = pymunk.Circle(circle_body, radius)
circle_shape.friction = 0.1
space.add(circle_body, circle_shape)


width = 80
height = 40
mass = 1
moment = pymunk.moment_for_box(mass, (width, height))
box_body = pymunk.Body(mass, moment)
box_body.position = (400, 200)  # Initial position for the box
box_shape = pymunk.Poly.create_box(box_body, (width, height))
space.add(box_body, box_shape)


# Create a static platform (segment shape)
platform_body = pymunk.Body(body_type=pymunk.Body.STATIC)
platform_shape = pymunk.Segment(platform_body, (0, 0), (600, 0), 5)
platform_shape.friction = 1  # Adjust friction if needed
space.add(platform_body, platform_shape)


# Create a static platform (segment shape)
platform_body = pymunk.Body(body_type=pymunk.Body.STATIC)
platform_shape = pymunk.Segment(platform_body, (600, 0), (600, 400), 5)
platform_shape.friction = 1  # Adjust friction if needed
space.add(platform_body, platform_shape)


# Create a static platform (segment shape)
platform_body = pymunk.Body(body_type=pymunk.Body.STATIC)
platform_shape = pymunk.Segment(platform_body, (600, 400), (0, 400), 5)
platform_shape.friction = 1  # Adjust friction if needed
space.add(platform_body, platform_shape)


# Create a static platform (segment shape)
platform_body = pymunk.Body(body_type=pymunk.Body.STATIC)
platform_shape = pymunk.Segment(platform_body, (0, 400), (0, 0), 5)
platform_shape.friction = 1  # Adjust friction if needed
space.add(platform_body, platform_shape)


# Create a renderer
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False


    circle_body.apply_force_at_local_point((15, -100))
    box_body.apply_force_at_local_point(-box_body.velocity)


    # Step the simulation
    space.step(1 / 60.0)

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the space
    space.debug_draw(draw_options)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()