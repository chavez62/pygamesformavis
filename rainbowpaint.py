import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

color = [255, 0, 0]  # Start with red
prev_pos = None
running = True
canvas_cleared = False  # Track reset state

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            screen.fill((255, 255, 255))  # White flash
            pygame.display.flip()
            pygame.time.wait(150)  # Slightly longer flash (150ms)
            screen.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))  # Random color
            pygame.display.flip()
            canvas_cleared = True  # Mark as cleared
            prev_pos = None  # Reset drawing position

    # Cycle colors
    if color[0] == 255 and color[1] < 255 and color[2] == 0: color[1] += 5
    elif color[1] == 255 and color[0] > 0: color[0] -= 5
    elif color[1] == 255 and color[2] < 255: color[2] += 5
    elif color[2] == 255 and color[1] > 0: color[1] -= 5
    elif color[2] == 255 and color[0] < 255: color[0] += 5
    elif color[0] == 255 and color[2] > 0: color[2] -= 5

    mx, my = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:  # Left click draws
        if canvas_cleared:
            prev_pos = (mx, my)  # Start fresh after reset
            canvas_cleared = False
        if prev_pos:
            pygame.draw.line(screen, color, prev_pos, (mx, my), 10)
        prev_pos = (mx, my)
    else:
        prev_pos = None  # Clear prev_pos when not clicking

    pygame.display.flip()
    clock.tick(60)

pygame.quit()