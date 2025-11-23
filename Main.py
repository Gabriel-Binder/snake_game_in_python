import pygame
import random

pygame.init()

# --- Constants ---
TILE = 32
GRID_W = 15
GRID_H = 10
SCORE_ROWS = 1  # extra row for score display

screen = pygame.display.set_mode((GRID_W * TILE, (GRID_H + SCORE_ROWS) * TILE))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 36)

# --- Snake setup ---
head = [GRID_W // 2, GRID_H // 2]
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
collision = False

# --- Game loop ---
while running:
    last_direction = direction.copy()  # track last moved direction

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and last_direction != [0, 1]:
                direction = [0, -1]
            elif event.key == pygame.K_s and last_direction != [0, -1]:
                direction = [0, 1]
            elif event.key == pygame.K_a and last_direction != [1, 0]:
                direction = [-1, 0]
            elif event.key == pygame.K_d and last_direction != [-1, 0]:
                direction = [1, 0]

    # --- Move the snake ---
    new_head = [head[0] + direction[0], head[1] + direction[1]]
    body.insert(0, head.copy())
    head = new_head
    last_direction = direction.copy()  # update after moving

    # --- Apple logic ---
    if head == apple:
        apple = spawn_apple()
        score += 1
    else:
        body.pop()

    # --- Collision check ---
    if (head[0] < 0 or head[0] >= GRID_W or
        head[1] < 0 or head[1] >= GRID_H or
        head in body):
        collision = True
        running = False

    # --- Drawing ---
    screen.fill((0, 0, 0))

    # Draw score row
    score_surf = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_surf, (10, 5))

    # Draw grid tiles with borders
    for y in range(GRID_H):
        for x in range(GRID_W):
            rect = pygame.Rect(x*TILE, (y+SCORE_ROWS)*TILE, TILE, TILE)
            pygame.draw.rect(screen, (0, 0, 0), rect)        # tile background
            pygame.draw.rect(screen, (100, 100, 100), rect, 1)  # border

    # Draw apple
    pygame.draw.rect(screen, (255, 0, 0), (apple[0]*TILE, (apple[1]+SCORE_ROWS)*TILE, TILE, TILE))

    # Draw snake body
    for b in body:
        pygame.draw.rect(screen, (0, 255, 0), (b[0]*TILE, (b[1]+SCORE_ROWS)*TILE, TILE, TILE))

    # Draw snake head
    pygame.draw.rect(screen, (0, 0, 255), (head[0]*TILE, (head[1]+SCORE_ROWS)*TILE, TILE, TILE))

    pygame.display.flip()
    clock.tick(10)

# --- Game Over display ---
if collision:
    screen.fill((0, 0, 0))  # clear screen
    # Draw grid with borders for context
    for y in range(GRID_H):
        for x in range(GRID_W):
            rect = pygame.Rect(x*TILE, (y+SCORE_ROWS)*TILE, TILE, TILE)
            pygame.draw.rect(screen, (0, 0, 0), rect)
            pygame.draw.rect(screen, (100, 100, 100), rect, 1)
    # Draw final snake and apple
    pygame.draw.rect(screen, (255, 0, 0), (apple[0]*TILE, (apple[1]+SCORE_ROWS)*TILE, TILE, TILE))
    for b in body:
        pygame.draw.rect(screen, (0, 255, 0), (b[0]*TILE, (b[1]+SCORE_ROWS)*TILE, TILE, TILE))
    pygame.draw.rect(screen, (0, 0, 255), (head[0]*TILE, (head[1]+SCORE_ROWS)*TILE, TILE, TILE))

    # Draw Game Over text in center
    game_over_surf = font.render("GAME OVER", True, (255, 0, 0))
    rect = game_over_surf.get_rect(center=(GRID_W*TILE//2, (GRID_H//2 + SCORE_ROWS)*TILE))
    screen.blit(game_over_surf, rect)
    pygame.display.flip()
    pygame.time.wait(2000)

pygame.quit()
