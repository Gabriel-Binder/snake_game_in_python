import os
import random

def main():
    x = 15
    y = 10

    head = [x//2, y//2 - 1]
    body = [[x//2 - 1, y//2 - 1], [x//2 - 2, y//2 - 1]]
    direction = [1, 0]
    score = 0
    apple = []
    def spawn_apple(old_head = head):
        nonlocal  apple
        while True:
            apple = [random.randrange(x), random.randrange(y)]
            if apple != head and apple not in body:
                break

    spawn_apple()

    def draw():
        grid = [[" " for _ in range(x)] for _ in range(y)]
        grid[apple[1]][apple[0]] = "A"
        grid[head[1]][head[0]] = "H"
        for b in body:
            grid[b[1]][b[0]] = "B"

        # Color lookup table
        colors = {
            "W": "\033[107m  \033[0m",  # white
            " ": "\033[40m  \033[0m",  # black
            "A": "\033[41m  \033[0m",  # red
            "H": "\033[44m  \033[0m",  # blue
            "B": "\033[42m  \033[0m",  # green
        }
        # Render
        # Top border
        print("".join(colors["W"] for _ in range(x + 2)))

        for row in grid:
            inside = "".join(colors[cell] for cell in row)
            print(colors["W"] + inside + colors["W"])

        # Bottom border
        print("".join(colors["W"] for _ in range(x + 2)))

    def move(grow=False):
        old_head = head.copy()
        head[0] += direction[0]
        head[1] += direction[1]
        body.insert(0, old_head)
        if not grow:
            body.pop()

    def is_outside(h):
        return h[0] < 0 or h[0] >= x or h[1] < 0 or h[1] >= y

    print(score)
    draw()

    while True:
        inp = input("> ")

        match inp:
            case "w":
                if direction != [0, 1]:
                    direction = [0, -1]
            case "a":
                if direction != [1, 0]:
                    direction = [-1, 0]
            case "d":
                if direction != [-1, 0]:
                    direction = [1, 0]
            case "s":
                if direction != [0, -1]:
                    direction = [0, 1]

        if [head[0] + direction[0], head[1] + direction[1]] == apple:
            move(grow=True)
            spawn_apple()
            score += 1
        else: move()
        if is_outside(head) or head in body:
            print("Game Over\nScore: {}".format(score))
            break
        os.system("cls" if os.name == "nt" else "clear")
        print(score)
        draw()

main()