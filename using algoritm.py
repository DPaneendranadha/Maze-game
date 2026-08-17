import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set constants for the maze
WIDTH, HEIGHT = 1000, 800
CELL_SIZE = 40
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
WALL_COLOR = (0, 0, 0)
PATH_COLOR = (255, 255, 255)
SOLUTION_COLOR = (0, 255, 0)
START_COLOR = (255, 0, 0)
END_COLOR = (0, 0, 255)

# Function to generate maze using depth-first search
def generate_maze():
    maze = [[0] * COLS for _ in range(ROWS)]
    stack = [(0, 0)]
    while stack:
        cell = stack[-1]
        maze[cell[0]][cell[1]] = 1
        neighbors = [(cell[0] + 2, cell[1]), (cell[0] - 2, cell[1]),
                     (cell[0], cell[1] + 2), (cell[0], cell[1] - 2)]
        unvisited_neighbors = [n for n in neighbors if 0 <= n[0] < ROWS and 0 <= n[1] < COLS and maze[n[0]][n[1]] == 0]
        if unvisited_neighbors:
            next_cell = random.choice(unvisited_neighbors)
            maze[(cell[0] + next_cell[0]) // 2][(cell[1] + next_cell[1]) // 2] = 1
            stack.append(next_cell)
        else:
            stack.pop()
    return maze

# Function to find solution using backtracking
def find_solution(maze, start, end):
    def backtrack(current):
        if current == end:
            return True
        row, col = current
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < ROWS and 0 <= new_col < COLS and maze[new_row][new_col] == 1 and (new_row, new_col) not in visited:
                visited.add((new_row, new_col))
                solution_path.append((new_row, new_col))
                if backtrack((new_row, new_col)):
                    return True
                solution_path.pop()
        return False

    visited = {start}
    solution_path = [start]
    if backtrack(start):
        return solution_path
    return []

# Draw the maze and solution
def draw_maze_and_solution(screen, maze, solution_path):
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[row][col] == 0:
                pygame.draw.rect(screen, WALL_COLOR, rect)
            elif (row, col) in solution_path:
                pygame.draw.rect(screen, SOLUTION_COLOR, rect)
            else:
                pygame.draw.rect(screen, PATH_COLOR, rect)

# Generate maze and find solution
maze = generate_maze()
solution_path = find_solution(maze, (0, 0), (ROWS - 1, COLS - 1))

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze with Solution")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    draw_maze_and_solution(screen, maze, solution_path)
    
    # Highlight start and end points
    pygame.draw.rect(screen, START_COLOR, pygame.Rect(0, 0, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, END_COLOR, pygame.Rect((COLS - 1) * CELL_SIZE, (ROWS - 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
