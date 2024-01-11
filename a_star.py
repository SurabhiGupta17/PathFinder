import math
from Pose import Pose

def a_star(current_pose: Pose, goal_pose: Pose) -> Pose:
    # updated_current_pose = Pose()
    #For each block, [g_cost, h_cost, f_cost]
    top_left = [0, 0, 0] 
    top = [0, 0, 0] 
    top_right = [0, 0, 0] 
    right = [0, 0, 0] 
    bottom_right = [0, 0, 0]
    bottom = [0, 0, 0]
    bottom_left = [0, 0, 0] 
    left =[0, 0, 0]
        
    #Initialise g_cost
    top_left[0] = 1.4
    top[0] = 1.0
    top_right[0] = 1.4
    right[0] = 1.0
    bottom_right[0] = 1.4
    bottom[0] = 1.0
    bottom_left[0] = 1.4
    left[0] = 1.0

    #Update h_cost
    top_left[1] = math.sqrt(((current_pose.x-1)-goal_pose.x)**2 + ((current_pose.y-1)-goal_pose.y)**2)
    top[1] = math.sqrt((current_pose.x-goal_pose.x)**2 + ((current_pose.y-1)-goal_pose.y)**2)
    top_right[1] = math.sqrt(((current_pose.x+1)-goal_pose.x)**2 + ((current_pose.y-1)-goal_pose.y)**2)
    right[1] = math.sqrt(((current_pose.x+1)-goal_pose.x)**2 + (current_pose.y-goal_pose.y)**2)
    bottom_right[1] = math.sqrt(((current_pose.x+1)-goal_pose.x)**2 + ((current_pose.y+1)-goal_pose.y)**2)
    bottom[1] = math.sqrt((current_pose.x-goal_pose.x)**2 + ((current_pose.y+1)-goal_pose.y)**2)
    bottom_left[1] = math.sqrt(((current_pose.x-1)-goal_pose.x)**2 + ((current_pose.y+1)-goal_pose.y)**2)
    left[1] = math.sqrt(((current_pose.x-1)-goal_pose.x)**2 + (current_pose.y-goal_pose.y)**2)

    #Update f_cost
    top_left[2] = top_left[0] + top_left[1]
    top[2] = top[0] + top[1]
    top_right[2] = top_right[0] + top_right[1]
    right[2] = right[0] + right[1]
    bottom_right[2] = bottom_right[0] + bottom_right[1]
    bottom[2] = bottom[0] + bottom[1]
    bottom_left[2] = bottom_left[0] + bottom_left[1]
    left[2] = left[0] + left[1]

    block = [
        top_left, 
        top, 
        top_right, 
        right, 
        bottom_right,
        bottom,
        bottom_left, 
        left
    ]

    lowest_f = 1000
    for i in range(8):
        # print(f"f_cost : {i} : {self.block[i][2]}")
        # print(f"g_cost : {i} : {self.block[i][0]}")
        # print(f"h_cost : {i} : {self.block[i][1]}")
        if lowest_f>block[i][2]:
            lowest_f=block[i][2] 
            best_move = i
        
    if best_move == 0:
        current_pose.x -= 1
        current_pose.y -= 1
    elif best_move == 1:
        current_pose.y -= 1
    elif best_move == 2:
        current_pose.x += 1
        current_pose.y -= 1
    elif best_move == 3:
        current_pose.x += 1
    elif best_move == 4:
        current_pose.x += 1
        current_pose.y += 1
    elif best_move == 5:
        current_pose.y += 1
    elif best_move == 6:
        current_pose.x -= 1
        current_pose.y += 1
    elif best_move == 7:
        current_pose.x -= 1
    #Add condition where lowest f_cost is same for multiple blocks.
    return current_pose
