import pygame
import random

pygame.init()

TILE = 32
GRID_W = 15
GRID_H = 10

screen = pygame.display.set_mode((GRID_W * TILE, GRID_H * TILE))
clock = pygame.time.Clock()

# Snake setup
head = [GRID_W//2, GRID_H//2]
body = [[head[0]-1, head[1]], [head[0]-2, head[1]]]
direction = [1, 0]

def spawn_apple():
    while True:
        pos = [random.randrange(GRID_W), random.randrange(GRID_H)]
        if pos != head and pos not in body:
            return pos

apple = spawn_apple()
score = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and direction != [0, 1]:
                direction = [0, -1]
            elif event.key == pygame.K_s and direction != [0, -1]:
                direction = [0, 1]
            elif event.key == pygame.K_a and direction != [1, 0]:
                direction = [-1, 0]
            elif event.key == pygame.K_d and direction != [-1, 0]:
                direction = [1, 0]

    # Move snake
    new_head = [head[0] + direction[0], head[1] + direction[1]]
    body.insert(0, head.copy())
    head = new_head

    # Apple
    if head == apple:
        apple = spawn_apple()
        score += 1
    else:
        body.pop()

    # Collision
    if (head[0] < 0 or head[0] >= GRID_W or
        head[1] < 0 or head[1] >= GRID_H or
        head in body):
        print("Game Over! Score:", score)
        running = False

    # Draw
    screen.fill((0, 0, 0))

    # Apple
    pygame.draw.rect(screen, (255, 0, 0), (apple[0]*TILE, apple[1]*TILE, TILE, TILE))

    # Body
    for b in body:
        pygame.draw.rect(screen, (0, 255, 0), (b[0]*TILE, b[1]*TILE, TILE, TILE))

    # Head
    pygame.draw.rect(screen, (0, 0, 255), (head[0]*TILE, head[1]*TILE, TILE, TILE))

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
