import pygame   
import pygame_gui
import sys
import time
import random

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

grid_cell_color_obstacle = (0, 0, 0)

# Initialise a 2D array to represent the grid
grid = [[False for _ in range(boxesPerRow)] for _ in range(boxesPerCol)]

# List to store the cells that are part of the path
global path_cells
path_cells = []
global obstacle_grid
obstacle_grid = []
global grid_map
grid_map = []

# Initialise values
global goal_pose
goal_pose=None
global start_pose
start_pose=None
current_pose=None

manager=pygame_gui.UIManager((pygame_screen_length, pygame_screen_width))

def update_obstacle_grid(new_value):
    global obstacle_grid
    obstacle_grid = new_value

#Create start button
button_rect = pygame.Rect(900, 30, 100, 50)
start_button = pygame_gui.elements.UIButton(
    relative_rect=button_rect, 
    text='Start', 
    manager=manager
    )

#Create dropdown for selecting mode
select_mode_rect=pygame.Rect(850, 115, 200, 50)
select_mode = pygame_gui.elements.UIDropDownMenu(
    options_list=['Set Goal Pose', 'Set Start Pose', 'Add obstacles'],
    starting_option='Set Goal Pose',
    relative_rect=select_mode_rect,
    expand_on_option_click=True
)

#Create generate map button
map_button_rect = pygame.Rect(800, 200, 300, 50)
map_button = pygame_gui.elements.UIButton(
    relative_rect=map_button_rect, 
    text='Generate Random Map', 
    manager=manager
    )

#Create reset button
reset_map_button_rect = pygame.Rect(900, 285, 100, 50)
reset_map_button = pygame_gui.elements.UIButton(
    relative_rect=reset_map_button_rect, 
    text='Reset Map', 
    manager=manager
    )

#Create reset button
reset_pos_button_rect = pygame.Rect(875, 370, 150, 50)
reset_pos_button = pygame_gui.elements.UIButton(
    relative_rect=reset_pos_button_rect, 
    text='Reset Pose', 
    manager=manager
    )

def reset_map():
    global goal_pose
    global start_pose
    global obstacle_grid
    global grid_map
    global path_cells
    global start

    goal_pose=None
    start_pose=None
    obstacle_grid = []
    grid_map = []
    path_cells = []
    start=False
    draw_grid()

def reset_pos():
    global goal_pose
    global start_pose
    global path_cells
    global start

    goal_pose=None
    start_pose=None
    path_cells = []
    start=False
    draw_grid()

def generate_random_map(boxesPerRow, boxesPerCol, min_cluster_size=20, max_clusters=20):
    global obstacle_grid
    global grid_map
    grid_map = []

    for _ in range(random.randint(10, max_clusters)):
        # Randomly select a starting point for the cluster
        start_row = random.randint(0, boxesPerCol - 1)
        start_col = random.randint(0, boxesPerRow - 1)
        current_pos = (start_row, start_col)

        # Perform a random walk to create a continuous path of obstacles within the cluster
        for _ in range(min_cluster_size + random.randint(0, min_cluster_size)):
            grid_map.append(current_pos)
            obstacle_grid.append((current_pos))

            # Randomly choose one of the neighboring cells
            neighbors = [(current_pos[0] + 1, current_pos[1]),
                         (current_pos[0] - 1, current_pos[1]),
                         (current_pos[0], current_pos[1] + 1),
                         (current_pos[0], current_pos[1] - 1)]

            valid_neighbors = [(r, c) for r, c in neighbors if 0 <= r < boxesPerCol and 0 <= c < boxesPerRow]

            if valid_neighbors:
                current_pos = random.choice(valid_neighbors)

    return grid_map

def draw_grid():
    global goal_pose
    global start_pose
    global obstacle_grid
    global grid_map
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
            if (goal_pose):
                pygame.draw.rect(pygame_screen, (200, 0, 0), (grid_area_start_x + goal_pose.x * box_size, grid_area_start_y + goal_pose.y * box_size, box_size, box_size))
            
            #Draw start pose
            if (start_pose):
                pygame.draw.rect(pygame_screen, (0, 150, 0), (grid_area_start_x + start_pose.x * box_size, grid_area_start_y + start_pose.y * box_size, box_size, box_size))

            #Draw current pose
            if (current_pose and 
                goal_pose and
                start_pose and
                not(current_pose.x==start_pose.x and current_pose.y==start_pose.y) and
                not(current_pose.x==goal_pose.x and current_pose.y==goal_pose.y)):
                pygame.draw.rect(pygame_screen, (100, 100, 100), (grid_area_start_x + current_pose.x * box_size, grid_area_start_y + current_pose.y * box_size, box_size, box_size))

            #Draw path cell
            if ((row, col) in path_cells):
                pygame.draw.rect(pygame_screen, (0, 0, 200), (x, y, box_size, box_size))

            #Draw obstacle
            if ((row, col) in obstacle_grid):
                pygame.draw.rect(pygame_screen, (0, 0, 0), (x, y, box_size, box_size))

            #Draw map
            if ((row, col) in grid_map):
                pygame.draw.rect(pygame_screen, (0, 0, 0), (x, y, box_size, box_size))

            # Draw top border
            pygame.draw.line(pygame_screen, (128, 128, 128), (x, y), (x + box_size, y), 1)

            # Draw left border
            pygame.draw.line(pygame_screen, (128, 128, 128), (x, y), (x, y + box_size), 1)

            # Draw right border
            pygame.draw.line(pygame_screen, (128, 128, 128), (x + box_size, y), (x + box_size, y + box_size), 1)

            # Draw bottom border
            pygame.draw.line(pygame_screen, (128, 128, 128), (x, y + box_size), (x + box_size, y + box_size), 1)
 


# Pygame main loop
clock = pygame.time.Clock()
running = True
global start
start=False
selected_option='Set Goal Pose'

while running:
    time_delta = clock.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    start=True
                    print("Start button clicked!")

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == reset_map_button:
                    print("Reset map button clicked!")
                    reset_map()

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == reset_pos_button:
                    print("Reset pos button clicked!")
                    reset_pos()
            
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == map_button:
                    grid_map = generate_random_map(boxesPerRow, boxesPerCol)
                    print("Generating map")

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == select_mode:
                    selected_option = event.text

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if (selected_option=='Set Goal Pose'):
                if (grid_area_start_x <= x <= grid_area_start_x + grid_area_length and
                    grid_area_start_y <= y <= grid_area_start_y + grid_area_width):
                    x, y = event.pos
                    grid_x, grid_y = int((x - grid_area_start_x) // box_size), int((y - grid_area_start_y) // box_size)
                    goal_pose = Pose(grid_x, grid_y)

            elif (selected_option=='Set Start Pose'):
                if (grid_area_start_x <= x <= grid_area_start_x + grid_area_length and
                    grid_area_start_y <= y <= grid_area_start_y + grid_area_width):
                    x, y = event.pos
                    grid_x, grid_y = int((x - grid_area_start_x) // box_size), int((y - grid_area_start_y) // box_size)
                    start_pose = Pose(grid_x, grid_y)
                    current_pose = Pose(start_pose.x, start_pose.y)

            elif (selected_option=='Add obstacles'):
                if (grid_area_start_x <= x <= grid_area_start_x + grid_area_length and
                    grid_area_start_y <= y <= grid_area_start_y + grid_area_width):
                    x, y = event.pos
                    grid_x, grid_y = int((x - grid_area_start_x) // box_size), int((y - grid_area_start_y) // box_size)
                    if (grid_y, grid_x) in obstacle_grid:
                        obstacle_grid.remove((grid_y, grid_x))
                    else:
                        obstacle_grid.append((grid_y, grid_x))

        manager.process_events(event)
    manager.update(time_delta)
    update_obstacle_grid(obstacle_grid)

    # Update the Pygame window
    pygame_screen.fill((255, 255, 255))

    #If start button is pressed, start the algorithm
    if (start and current_pose and goal_pose):
        if (current_pose.x==goal_pose.x and current_pose.y==goal_pose.y):
            pass
        else:
            current_pose=a_star(current_pose, goal_pose, obstacle_grid, path_cells)

        path_cells.append((current_pose.y, current_pose.x))

    # Draw the grid
    draw_grid()
    manager.update(0.01)
    manager.draw_ui(pygame_screen)
    pygame.display.update()
    pygame.display.flip()
    time.sleep(0.25)

pygame.quit()
sys.exit()