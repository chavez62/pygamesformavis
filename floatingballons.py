import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Balloon class
class Balloon:
    def __init__(self):
        self.x = random.randint(50, 750)
        self.y = 600
        self.size = random.randint(30, 50)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.speed = random.uniform(1, 3)

# Confetti class
class Confetti:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(3, 7)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-3, 1)
        self.life = 60  # Frames until it fades out

balloons = [Balloon() for _ in range(5)]
confetti_particles = []
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for balloon in balloons[:]:
                if ((mx - balloon.x) ** 2 + (my - balloon.y) ** 2) ** 0.5 < balloon.size:
                    # Add confetti when balloon pops
                    for _ in range(50):  # Number of confetti pieces
                        confetti_particles.append(Confetti(balloon.x, balloon.y))
                    balloons.remove(balloon)
                    balloons.append(Balloon())  # Replace popped balloon

    # Update balloons
    screen.fill((135, 206, 235))  # Sky blue background
    for balloon in balloons:
        balloon.y -= balloon.speed
        if balloon.y < -50:
            balloons.remove(balloon)
            balloons.append(Balloon())
        pygame.draw.circle(screen, balloon.color, (int(balloon.x), int(balloon.y)), balloon.size)
        pygame.draw.line(screen, (0, 0, 0), (int(balloon.x), int(balloon.y) + balloon.size), 
                         (int(balloon.x), int(balloon.y) + balloon.size + 20), 2)  # String

    # Update and draw confetti
    for particle in confetti_particles[:]:
        particle.x += particle.speed_x
        particle.y += particle.speed_y
        particle.life -= 1
        if particle.life <= 0:
            confetti_particles.remove(particle)
        else:
            pygame.draw.circle(screen, particle.color, (int(particle.x), int(particle.y)), particle.size)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()