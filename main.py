import pygame   
import pygame_gui
import sys
import time
import random

from Pose import Pose
from a_star import a_star
import settings
import buttons

#Initialise pygame window
pygame.init()
pygame_screen = pygame.display.set_mode((settings.SCREEN_LENGTH, settings.SCREEN_WIDTH))
pygame.display.set_caption("Interactive Path Planner")

grid_cell_color_obstacle = (0, 0, 0)

# Initialise a 2D array to represent the grid
grid = [[False for _ in range(settings.BOXES_PER_ROW)] for _ in range(settings.BOXES_PER_COL)]

# List to store the cells that are part of the path
global path_cells
path_cells = []
global obstacle_grid
obstacle_grid = []
global grid_map
grid_map = []
global visited_cells
visited_cells = []
global not_visited_cells
not_visited_cells = []

# Initialise values
global goal_pose
goal_pose=None
global start_pose
start_pose=None
current_pose=None

manager=pygame_gui.UIManager((settings.SCREEN_LENGTH, settings.SCREEN_WIDTH))

def update_obstacle_grid(new_value):
    global obstacle_grid
    obstacle_grid = new_value

#Create buttons
start_button = buttons.create_start_button(manager)
select_mode = buttons.create_dropdown_menu(manager)
map_button = buttons.create_generate_map_button(manager)
reset_map_button = buttons.create_reset_map_button(manager)
reset_pos_button = buttons.create_reset_pos_button(manager)

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

def generate_random_map(boxesPerRow, boxesPerCol, min_cluster_size=2, max_clusters=5):
    global obstacle_grid
    global grid_map
    grid_map = []

    for _ in range(random.randint(1, max_clusters)):
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
        (settings.GRID_AREA_START_X - 1, 
         settings.GRID_AREA_START_Y - 1, 
         settings.GRID_AREA_LENGTH + 3, 
         settings.GRID_AREA_WIDTH + 3), 
         2)

    for row in range(settings.BOXES_PER_COL):
        for col in range(settings.BOXES_PER_ROW):
            x = settings.GRID_AREA_START_X + col * settings.BOX_SIZE
            y = settings.GRID_AREA_START_Y + row * settings.BOX_SIZE

            #Draw goal pose
            if (goal_pose):
                pygame.draw.rect(pygame_screen, (200, 0, 0), (settings.GRID_AREA_START_X + goal_pose.x * settings.BOX_SIZE, settings.GRID_AREA_START_Y + goal_pose.y * settings.BOX_SIZE, settings.BOX_SIZE, settings.BOX_SIZE))
            
            #Draw start pose
            if (start_pose):
                pygame.draw.rect(pygame_screen, (0, 150, 0), (settings.GRID_AREA_START_X + start_pose.x * settings.BOX_SIZE, settings.GRID_AREA_START_Y + start_pose.y * settings.BOX_SIZE, settings.BOX_SIZE, settings.BOX_SIZE))

            #Draw current pose
            if (current_pose and 
                goal_pose and
                start_pose and
                not(current_pose.x==start_pose.x and current_pose.y==start_pose.y) and
                not(current_pose.x==goal_pose.x and current_pose.y==goal_pose.y)):
                pygame.draw.rect(pygame_screen, (100, 100, 100), (settings.GRID_AREA_START_X + current_pose.x * settings.BOX_SIZE, settings.GRID_AREA_START_Y + current_pose.y * settings.BOX_SIZE, settings.BOX_SIZE, settings.BOX_SIZE))
    
            #Draw path cell
            if ((row, col) in path_cells):
                pygame.draw.rect(pygame_screen, (0, 0, 200), (x, y, settings.BOX_SIZE, settings.BOX_SIZE))

            #Draw obstacle
            if ((row, col) in obstacle_grid):
                pygame.draw.rect(pygame_screen, (0, 0, 0), (x, y, settings.BOX_SIZE, settings.BOX_SIZE))

            #Draw map
            if ((row, col) in grid_map):
                pygame.draw.rect(pygame_screen, (0, 0, 0), (x, y, settings.BOX_SIZE, settings.BOX_SIZE))

            # Draw top border
            pygame.draw.line(pygame_screen, (128, 128, 128), (x, y), (x + settings.BOX_SIZE, y), 1)

            # Draw left border
            pygame.draw.line(pygame_screen, (128, 128, 128), (x, y), (x, y + settings.BOX_SIZE), 1)

            # Draw right border
            pygame.draw.line(pygame_screen, (128, 128, 128), (x + settings.BOX_SIZE, y), (x + settings.BOX_SIZE, y + settings.BOX_SIZE), 1)

            # Draw bottom border
            pygame.draw.line(pygame_screen, (128, 128, 128), (x, y + settings.BOX_SIZE), (x + settings.BOX_SIZE, y + settings.BOX_SIZE), 1)
 


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
                    grid_map = generate_random_map(settings.BOXES_PER_ROW, settings.BOXES_PER_COL)
                    print("Generating map")

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == select_mode:
                    selected_option = event.text

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if (selected_option=='Set Goal Pose'):
                if (settings.GRID_AREA_START_X <= x <= settings.GRID_AREA_START_X + settings.GRID_AREA_LENGTH and
                    settings.GRID_AREA_START_Y <= y <= settings.GRID_AREA_START_Y + settings.GRID_AREA_WIDTH):
                    x, y = event.pos
                    grid_x, grid_y = int((x - settings.GRID_AREA_START_X) // settings.BOX_SIZE), int((y - settings.GRID_AREA_START_Y) // settings.BOX_SIZE)
                    goal_pose = Pose(grid_x, grid_y)

            elif (selected_option=='Set Start Pose'):
                if (settings.GRID_AREA_START_X <= x <= settings.GRID_AREA_START_X + settings.GRID_AREA_LENGTH and
                    settings.GRID_AREA_START_Y <= y <= settings.GRID_AREA_START_Y + settings.GRID_AREA_WIDTH):
                    x, y = event.pos
                    grid_x, grid_y = int((x - settings.GRID_AREA_START_X) // settings.BOX_SIZE), int((y - settings.GRID_AREA_START_Y) // settings.BOX_SIZE)
                    start_pose = Pose(grid_x, grid_y)
                    current_pose = Pose(start_pose.x, start_pose.y)

            elif (selected_option=='Add obstacles'):
                if (settings.GRID_AREA_START_X <= x <= settings.GRID_AREA_START_X + settings.GRID_AREA_LENGTH and
                    settings.GRID_AREA_START_Y <= y <= settings.GRID_AREA_START_Y + settings.GRID_AREA_WIDTH):
                    x, y = event.pos
                    grid_x, grid_y = int((x - settings.GRID_AREA_START_X) // settings.BOX_SIZE), int((y - settings.GRID_AREA_START_Y) // settings.BOX_SIZE)
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
            if [current_pose.x, current_pose.y] not in visited_cells:
                visited_cells.append([current_pose.x, current_pose.y]) 

            if [current_pose.x, current_pose.y-1] not in not_visited_cells and [current_pose.x, current_pose.y-1] not in visited_cells and 0 < current_pose.y:
                not_visited_cells.append([current_pose.x, current_pose.y-1])  

            if [current_pose.x+1, current_pose.y] not in not_visited_cells and [current_pose.x+1, current_pose.y] not in visited_cells and current_pose.x < 5:
                not_visited_cells.append([current_pose.x+1, current_pose.y])  

            if [current_pose.x, current_pose.y+1] not in not_visited_cells and [current_pose.x, current_pose.y+1] not in visited_cells and current_pose.y < 5:
                not_visited_cells.append([current_pose.x, current_pose.y+1])  

            if [current_pose.x-1, current_pose.y] not in not_visited_cells and [current_pose.x-1, current_pose.y] not in visited_cells and 0 < current_pose.x:
                not_visited_cells.append([current_pose.x-1, current_pose.y])   

            current_pose.x, current_pose.y = not_visited_cells.pop()
        
            # current_pose=a_star(current_pose, goal_pose, obstacle_grid, path_cells)

        path_cells.append((current_pose.y, current_pose.x))
        print(not_visited_cells)
        print(visited_cells)

    # Draw the grid
    draw_grid()
    manager.update(0.01)
    manager.draw_ui(pygame_screen)
    pygame.display.update()
    pygame.display.flip()
    time.sleep(0.5)

pygame.quit()
sys.exit()