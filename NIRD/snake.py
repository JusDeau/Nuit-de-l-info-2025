"""
Simple Snake game made with pygame.
Features:
- Pink snake with a stylised deer head (drawn with pygame primitives) as the head.
- Food that appears randomly on the grid.
- Score display and speed increase as snake eats food.
- Game over screen with ability to restart (R) or quit (Esc / close window).

Controls:
- Arrow keys or WASD to move.

Requirements:
- Python 3.8+
- pygame (pip install pygame)

Save this file as `snake_pygame.py` and run: python snake_pygame.py
"""

import sys
import random
import pygame
from pygame.math import Vector2

# -------- Constants --------
CELL_SIZE = 24
GRID_WIDTH = 5
GRID_HEIGHT = 10
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10
INITIAL_SNAKE_LENGTH = 4

# Colors
BG_COLOR = (30, 30, 30)
GRID_COLOR = (40, 40, 40)
SNAKE_BODY_COLOR = (255, 120, 200)  # pink
SNAKE_BORDER = (200, 70, 160)
FOOD_COLOR = (250, 220, 100)
TEXT_COLOR = (230, 230, 230)

# Directions
UP = Vector2(0, -1)
DOWN = Vector2(0, 1)
LEFT = Vector2(-1, 0)
RIGHT = Vector2(1, 0)

# -------- Helper functions --------

def grid_to_pixel(pos):
    """Convert a Vector2 grid position to top-left pixel coordinate."""
    return int(pos.x * CELL_SIZE), int(pos.y * CELL_SIZE)


# -------- Game Classes --------
class Food:
    def __init__(self, occupied: set):
        self.position = Vector2(0, 0)
        self.respawn(occupied)

    def respawn(self, occupied: set):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            p = Vector2(x, y)
            if (x, y) not in occupied:
                self.position = p
                break

    def draw(self, surf: pygame.Surface):
        px, py = grid_to_pixel(self.position)
        rect = pygame.Rect(px + 4, py + 4, CELL_SIZE - 8, CELL_SIZE - 8)
        pygame.draw.rect(surf, FOOD_COLOR, rect, border_radius=4)


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.body = [Vector2(start_x - i, start_y) for i in range(INITIAL_SNAKE_LENGTH)]
        self.direction = RIGHT
        self.grow_amount = 0
        self.alive = True

    def head(self):
        return self.body[0]

    def occupied_set(self):
        return {(int(p.x), int(p.y)) for p in self.body}

    def set_direction(self, new_dir: Vector2):
        # Prevent reversing directly
        if new_dir + self.direction == Vector2(0, 0):
            return
        self.direction = new_dir

    def update(self):
        if not self.alive:
            return
        new_head = self.head() + self.direction
        # Check walls
        if not (0 <= new_head.x < GRID_WIDTH) or not (0 <= new_head.y < GRID_HEIGHT):
            self.alive = False
            return
        # Check self collision
        for segment in self.body:
            if int(segment.x) == int(new_head.x) and int(segment.y) == int(new_head.y):
                self.alive = False
                return
        # Move
        self.body.insert(0, new_head)
        if self.grow_amount > 0:
            self.grow_amount -= 1
        else:
            self.body.pop()

    def grow(self, amount=1):
        self.grow_amount += amount

    def draw(self, surf: pygame.Surface):
        # Draw body (excluding head) with darker border
        for seg in self.body[1:]:
            px, py = grid_to_pixel(seg)
            rect = pygame.Rect(px + 2, py + 2, CELL_SIZE - 4, CELL_SIZE - 4)
            pygame.draw.rect(surf, SNAKE_BORDER, rect, border_radius=4)
            inner = pygame.Rect(px + 4, py + 4, CELL_SIZE - 8, CELL_SIZE - 8)
            pygame.draw.rect(surf, SNAKE_BODY_COLOR, inner, border_radius=3)

        # Draw head as a stylised deer head
        self._draw_deer_head(surf, self.head(), self.direction)

    def _draw_deer_head(self, surf: pygame.Surface, pos: Vector2, direction: Vector2):
        px, py = grid_to_pixel(pos)
        center = (px + CELL_SIZE // 2, py + CELL_SIZE // 2)
        head_radius = CELL_SIZE // 2 - 2

        # Base head (ellipse)
        head_rect = pygame.Rect(0, 0, head_radius * 2, head_radius * 2)
        head_rect.center = center
        pygame.draw.ellipse(surf, SNAKE_BODY_COLOR, head_rect)
        pygame.draw.ellipse(surf, SNAKE_BORDER, head_rect, width=2)

        # Ears
        ear_offset = head_radius - 4
        left_ear = (center[0] - ear_offset, center[1] - ear_offset)
        right_ear = (center[0] + ear_offset, center[1] - ear_offset)
        pygame.draw.polygon(surf, SNAKE_BODY_COLOR, [(left_ear[0], left_ear[1]), (left_ear[0]-4, left_ear[1]-10), (left_ear[0]+6, left_ear[1]-8)])
        pygame.draw.polygon(surf, SNAKE_BODY_COLOR, [(right_ear[0], right_ear[1]), (right_ear[0]+4, right_ear[1]-10), (right_ear[0]-6, right_ear[1]-8)])

        # Antlers (simple branching)
        antler_color = (200, 150, 60)
        base_y = center[1] - head_radius
        left_base = (center[0] - 6, base_y)
        right_base = (center[0] + 6, base_y)

        def draw_antler(base_x, steps):
            x = base_x
            y = base_y
            for i in range(steps):
                nx = x + (-1 if base_x < center[0] else 1) * (4 + i)
                ny = y - (6 + i * 4)
                pygame.draw.line(surf, antler_color, (x, y), (nx, ny), 3)
                # small branch
                bx = nx + (2 if base_x < center[0] else -2)
                by = ny + 6
                pygame.draw.line(surf, antler_color, (nx, ny), (bx, by), 2)

        draw_antler(left_base[0], 2)
        draw_antler(right_base[0], 2)

        # Eye and nose
        eye_pos = (center[0] + int(direction.x) * 6 + 6, center[1] - 2)
        pygame.draw.circle(surf, (40, 40, 40), eye_pos, 3)
        nose_pos = (center[0] + int(direction.x) * 10, center[1] + 6)
        pygame.draw.circle(surf, (180, 80, 120), nose_pos, 3)


# -------- Main loop --------

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake - Pink Deer Head")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 28)
    big_font = pygame.font.SysFont(None, 48)

    snake = Snake()
    food = Food(snake.occupied_set())
    score = 0
    speed = FPS

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if snake.alive:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        snake.set_direction(UP)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        snake.set_direction(DOWN)
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        snake.set_direction(LEFT)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        snake.set_direction(RIGHT)
                else:
                    # dead: allow restart
                    if event.key == pygame.K_r:
                        snake.reset()
                        food.respawn(snake.occupied_set())
                        score = 0
                        speed = FPS

        # regarde si le joueur a atteint son objectif
        if score == 5:
            running = False


        # Update at fixed tick speed
        if snake.alive:
            snake.update()

            # Check food collision
            if snake.head().x == food.position.x and snake.head().y == food.position.y:
                snake.grow(1)
                score += 1
                # increase speed modestly
                speed = min(25, FPS + score // 3)
                food.respawn(snake.occupied_set())

        # Draw
        screen.fill(BG_COLOR)

        # grid optional subtle
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

        food.draw(screen)
        snake.draw(screen)

        # Score
        score_surf = font.render(f"Score: {score}", True, TEXT_COLOR)
        screen.blit(score_surf, (10, 10))

        if not snake.alive:
            # Game over overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))
            go_text = big_font.render("Game Over", True, (240, 240, 240))
            go_rect = go_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
            screen.blit(go_text, go_rect)
            info_text = font.render("Press R to restart or Esc to quit", True, (220, 220, 220))
            info_rect = info_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            screen.blit(info_text, info_rect)

        pygame.display.flip()
        clock.tick(speed)

    pygame.quit()
    sys.exit()
