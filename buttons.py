import pygame
import pygame_gui

def create_start_button(manager):
    button_rect = pygame.Rect(900, 30, 100, 50)
    return pygame_gui.elements.UIButton(
    relative_rect=button_rect, 
    text='Start', 
    manager=manager
    )

def create_dropdown_menu(manager):
    select_mode_rect=pygame.Rect(850, 115, 200, 50)
    return pygame_gui.elements.UIDropDownMenu(
        options_list=['Set Goal Pose', 'Set Start Pose', 'Add obstacles'],
        starting_option='Set Goal Pose',
        relative_rect=select_mode_rect,
        expand_on_option_click=True
    )

def create_generate_map_button(manager):
    map_button_rect = pygame.Rect(800, 200, 300, 50)
    return pygame_gui.elements.UIButton(
        relative_rect=map_button_rect, 
        text='Generate Random Map', 
        manager=manager
    )

def create_reset_map_button(manager):
    reset_map_button_rect = pygame.Rect(900, 285, 100, 50)
    return pygame_gui.elements.UIButton(
        relative_rect=reset_map_button_rect, 
        text='Reset Map', 
        manager=manager
    )

def create_reset_pos_button(manager):
    reset_pos_button_rect = pygame.Rect(875, 370, 150, 50)
    return pygame_gui.elements.UIButton(
        relative_rect=reset_pos_button_rect, 
        text='Reset Pose', 
        manager=manager
    )