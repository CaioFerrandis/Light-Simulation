import math

import pygame

pygame.init()

global WIDTH, HEIGHT
WIDTH, HEIGHT = (800, 600)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Light Particle Simulation!")


class Dot:
    def __init__(self, display, x, y, oldx, oldy, radius, color):
        self.display = display

        self.x = x
        self.y = y
        self.oldx = oldx
        self.oldy = oldy
        self.vx = x - oldx
        self.vy = y - oldy

        self.radius = radius
        self.color = color
        self.positions = [(x, y)]

        self.alive = True
        self.arc_collision = False

        self.dot = None

    def render(self):
        self.dot = pygame.draw.circle(self.display, self.color, (self.x, self.y), self.radius)

    def constrain_dot(self):
        # Particle dies if it collides too many times
        if self.alive:
            self.vx = self.x - self.oldx
            self.vy = self.y - self.oldy

            # Check collisions with borders of window and mirror
            if self.x < 0:
                self.positions.append((self.x, self.y))
                self.x = 0
                self. oldx = self.x + self.vx

            if self.x > self.display.get_width():
                self.positions.append((self.x, self.y))

                self.x = self.display.get_width()
                self.oldx = self.x + self.vx

            if self.y < 0:
                self.positions.append((self.x, self.y))
                self.y = 0
                self.oldy = self.y + self.vy

            if self.y > self.display.get_height():
                self.positions.append((self.x, self.y))

                self.y = self.display.get_height()
                self.oldy = self.y + self.vy

            # Check collisions with circular mirror
            dist_x = abs(circle_center[0] - self.x)
            dist_y = abs(circle_center[1] - self.y)
            distance = math.sqrt(dist_x ** 2 + dist_y ** 2)
            if abs(distance - circle_radius) <= circle_border / 2 and self.x >= circle_center[0]:
                self.positions.append((self.x, self.y))

                # Calculate new velocity components
                self.x = (math.cos(self.x - circle_center[0]) + circle_center[0])
                self.y = (math.sin(self.y - circle_center[1]) + circle_center[1])

        if len(self.positions) > 5:
            self.alive = False
            self.vx = self.vy = self.oldx = self.oldy = 0

    def update(self):
        if self.alive:
            if not self.arc_collision:
                self.vx = self.x - self.oldx
                self.vy = self.y - self.oldy

                while self.vx > 1 or self.vy > 1:
                    self.vx /= 2.5
                    self.vy /= 2.5

                self.arc_collision = False

            self.oldx = self.x
            self.oldy = self.y

            self.x += self.vx
            self.y += self.vy


def process_rays(rays, sub_steps):
    for i in rays:
        for r in range(len(i.positions)):
            if r == len(i.positions) - 1:
                break
            pygame.draw.line(i.display, i.color, i.positions[r], i.positions[r + 1])

        for n in range(sub_steps):
            i.update()
            i.constrain_dot()
        i.render()


def clear(dots):
    for i, _ in enumerate(dots):
        del dots[i]


running = True
sub_steps = 8

# List for all rays to be stored
dots = []

# Define circle properties
circle_radius = 250
circle_center = (screen.get_width() - circle_radius, screen.get_height()/2)
circle_border = 3

# Variables for ray
angle = 0
radius = 40
clicked = False
while running:
    spawn_pos = pygame.mouse.get_pos()
    screen.fill((50, 50, 50))

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.MOUSEWHEEL:
            angle -= e.y * -0.05

    keyboard = pygame.key.get_pressed()
    if keyboard[pygame.K_c]:
        clear(dots)

    if pygame.mouse.get_pressed()[0] and not clicked:
        dots.append(Dot(screen, spawn_pos[0], spawn_pos[1], spawn_pos[0] - math.cos(angle)*5,
                        spawn_pos[1] - math.sin(angle)*5, 1, (255, 0, 0)))
        clicked = True
    if not pygame.mouse.get_pressed()[0]:
        clicked = False

    # Draw circular mirror and its center
    pygame.draw.circle(screen, [255, 255, 255], circle_center, circle_radius, circle_border)
    pygame.draw.circle(screen, [255, 255, 255], circle_center, 2)
    pygame.draw.rect(screen, [50, 50, 50], pygame.Rect(circle_center[0]-circle_radius,
                                                       circle_center[1]-circle_radius,
                                                       circle_radius, circle_radius*2))

    # Draw center line for reference
    pygame.draw.line(screen, (200, 200, 200), [0, screen.get_height() / 2],
                     [screen.get_width(), screen.get_height() / 2], 1)

    # Draw all rays
    process_rays(dots, sub_steps)

    # Draw predicted particle trajectory
    pygame.draw.line(screen, (255, 0, 0), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]),
                     (pygame.mouse.get_pos()[0] + math.cos(angle)*radius, pygame.mouse.get_pos()[1] + math.sin(angle)*radius))

    # Circle to help aiming
    pygame.draw.circle(screen, (200, 200, 200), spawn_pos, radius, 1)

    pygame.display.update()

pygame.quit()
