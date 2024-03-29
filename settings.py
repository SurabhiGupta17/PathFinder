SCREEN_WIDTH = 650
SCREEN_LENGTH = 1200

GRID_AREA_WIDTH = 600
GRID_AREA_LENGTH = 600

#To ensure that the grid is always in the center in the x axis
GRID_AREA_START_Y = (SCREEN_WIDTH-GRID_AREA_WIDTH)//2
GRID_AREA_START_X = GRID_AREA_START_Y

BOX_SIZE = 100
BOXES_PER_ROW = int(GRID_AREA_LENGTH//BOX_SIZE)
BOXES_PER_COL = int(GRID_AREA_WIDTH//BOX_SIZE)