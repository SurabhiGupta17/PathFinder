import pygame   
import sys
import time
from Pose import Pose
from a_star import a_star

#Initialise pygame window
pygame.init()
pygame_screen_width = 650
pygame_screen_length = 1200
pygame_screen = pygame.display.set_mode((pygame_screen_length, pygame_screen_width))
pygame.display.set_caption("Interactive Path Planner")

#Dimensions for the grid area
grid_area_width = grid_area_length = 600

#to ensure that the grid is always in the center in the x axis
grid_area_start_y = (pygame_screen_width-grid_area_width)//2
grid_area_start_x = grid_area_start_y

box_size = 20

boxesPerRow = int(grid_area_length//box_size)
boxesPerCol = int(grid_area_width//box_size)

obstacle_grid = []
grid_cell_color_obstacle = (0, 0, 0)

# Initialize a 2D array to represent the grid
grid = [[False for _ in range(boxesPerRow)] for _ in range(boxesPerCol)]

# List to store the cells that are part of the path
path_cells = []

#Initialise end point and start point
goal_pose = Pose(0, 0)
start_pose = Pose(23, 23)
current_pose = Pose(start_pose.x, start_pose.y)

# Function to draw the grid
def draw_grid():
    # Draw border around the grid area
    pygame.draw.rect(
        pygame_screen, 
        (0, 0, 0), 
        (grid_area_start_x - 1, 
         grid_area_start_y - 1, 
         grid_area_length + 3, 
         grid_area_width + 3), 
         2)

    for row in range(boxesPerCol):
        for col in range(boxesPerRow):
            x = grid_area_start_x + col * box_size
            y = grid_area_start_y + row * box_size

            #Draw goal pose
            pygame.draw.rect(pygame_screen, (200, 0, 0), (grid_area_start_x + goal_pose.x * box_size, grid_area_start_y + goal_pose.y * box_size, box_size, box_size))
            
            #Draw start pose
            pygame.draw.rect(pygame_screen, (0, 0, 0), (grid_area_start_x + start_pose.x * box_size, grid_area_start_y + start_pose.y * box_size, box_size, box_size))

             #Draw current pose
            pygame.draw.rect(pygame_screen, (0, 0, 0), (grid_area_start_x + current_pose.x * box_size, grid_area_start_y + current_pose.y * box_size, box_size, box_size))

            #Draw cell
            if (row, col) in path_cells:
                pygame.draw.rect(pygame_screen, (0, 0, 0), (x, y, box_size, box_size))

            else:
                color = grid_cell_color_obstacle if grid[row][col] else (255, 255, 255)
                pygame.draw.rect(pygame_screen, color, (x, y, box_size, box_size))

            # Draw top border
            pygame.draw.line(pygame_screen, (128, 128, 128), (x, y), (x + box_size, y), 1)

            # Draw left border
            pygame.draw.line(pygame_screen, (128, 128, 128), (x, y), (x, y + box_size), 1)

            # Draw right border
            pygame.draw.line(pygame_screen, (128, 128, 128), (x + box_size, y), (x + box_size, y + box_size), 1)

            # Draw bottom border
            pygame.draw.line(pygame_screen, (128, 128, 128), (x, y + box_size), (x + box_size, y + box_size), 1)
 


# Pygame main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle mouse clicks in the Pygame window
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if (grid_area_start_x <= x <= grid_area_start_x + grid_area_length and
                grid_area_start_y <= y <= grid_area_start_y + grid_area_width):
                # Toggle obstacle status for the clicked grid cell
                x, y = event.pos
                # Convert pixel coordinates to grid indices
                grid_x, grid_y = int((x - grid_area_start_x) // box_size), int((y - grid_area_start_y) // box_size)
                # Toggle the square color
                grid[grid_y][grid_x] = not grid[grid_y][grid_x]

    # Update the Pygame window
    pygame_screen.fill((255, 255, 255))

    if (current_pose.x==goal_pose.x and current_pose.y==goal_pose.y):
        pass
    else:
        current_pose=a_star(current_pose, goal_pose)

    # Add the current cell to the path
    path_cells.append((current_pose.y, current_pose.x))

    # Draw the grid
    draw_grid()
    pygame.display.flip()
    time.sleep(0.25)

pygame.quit()
sys.exit()