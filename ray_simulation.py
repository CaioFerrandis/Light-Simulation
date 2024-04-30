'''
Simulation of light rays reflecting off of a concave mirror

C.F.
'''

import math

import pygame

pygame.init()

global WIDTH, HEIGHT
WIDTH, HEIGHT = (800, 600)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Light Particle Simulation! - By C.F.")

running = True
sub_steps = 8

# Define circle properties
circle_radius = WIDTH
circle_center = [0, HEIGHT/2]
circle_border = 5
center = WIDTH - 150
focus = WIDTH - 75

while running:
    mouse = pygame.mouse.get_pos()
    screen.fill((50, 50, 50))

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    # Draw center line for reference
    pygame.draw.line(screen, (200, 200, 200), [0, circle_center[1]],
                     [WIDTH, circle_center[1]], 1)
    pygame.draw.line(screen, (255, 0, 0), mouse, [mouse[0], circle_center[1]])

    # Draw circular mirror and its components
    pygame.draw.circle(screen, [255, 255, 255], circle_center, circle_radius, circle_border)
    pygame.draw.circle(screen, [255, 255, 255], [focus, circle_center[1]], 3)
    pygame.draw.circle(screen, [255, 255, 255], [center, circle_center[1]], 3)
    pygame.draw.rect(screen, [50, 50, 50], pygame.Rect(circle_center[0]-circle_radius,
                                                       circle_center[1]-circle_radius,
                                                       circle_radius, circle_radius*2))

    # Draw predicted particle trajectory
    # Towards focus of mirror
    angular_coefficient = (circle_center[1] - mouse[1]) / ((circle_radius * math.cos((mouse[1] - HEIGHT/2)/circle_radius) - circle_border) - focus)

    pygame.draw.line(screen, (255, 0, 0), (mouse[0], mouse[1]), ((circle_radius * math.cos((mouse[1] - HEIGHT/2)/circle_radius) - circle_border), mouse[1]))
    pygame.draw.line(screen, (255, 0, 0), ((circle_radius * math.cos((mouse[1] - HEIGHT/2)/circle_radius) - circle_border), mouse[1]), (focus - WIDTH, circle_center[1] + WIDTH*angular_coefficient))

    # Towards vertex of mirror
    angular_coefficient = (circle_center[1] - mouse[1]) / (circle_radius - mouse[0])

    pygame.draw.line(screen, (255, 0, 0), mouse, [circle_center[0] + circle_radius - circle_border, circle_center[1]])
    pygame.draw.line(screen, (255, 0, 0), [(mouse[0])-WIDTH - circle_border,
                                           (circle_center[1] - (mouse[1] - circle_center[1]))+(WIDTH*angular_coefficient)],
                     [circle_center[0] + circle_radius - circle_border, circle_center[1]])

    pygame.display.update()

pygame.quit()
