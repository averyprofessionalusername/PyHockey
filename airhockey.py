#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 17:13:06 2020

@author: dominicbolton
"""
import pygame
import numpy as np

pygame.init()

window_width = 600
window_height = 400
goal_size = 150

L_paddle_x = window_width//5
L_paddle_y = window_height//2 
R_paddle_x = window_width - window_width//5
R_paddle_y = window_height//2
paddle_vel = 10
paddle_r = 20

puck_velx = 0
puck_vely = 0
puck_x = 300
puck_y = 200
puck_vel = 20
puck_r = 10

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)

left_score = 0
right_score = 0

window = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("pyhockey")

run = True

def move_paddle(paddle,posx,posy,rad):
    """
    interprets key press and moves paddle
    """
    keys = pygame.key.get_pressed()
    
    if paddle == 'left':#if left, use arrow keys
        up, down, left, right = pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT
    if paddle == 'right':# if right use wasd
        up, down, left, right = pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d
    
    if keys[left] and posx >= rad and paddle == 'left':
        posx -= paddle_vel
        
    if keys[left] and posx >= window_width//2 + rad and paddle =='right':
        posx -= paddle_vel
    
    if keys[right] and posx <= window_width//2 - rad and paddle == 'left':
        posx += paddle_vel
        
    if keys[right] and posx <= window_width - rad and paddle == 'right':
        posx += paddle_vel
    
    if keys[up] and posy >= rad:
        posy -= paddle_vel
        
    if keys[down] and posy <= window_height - rad:
        posy += paddle_vel
    
    return posx,posy

def touch_puck(paddlex, paddley, puckx, pucky):
    """
    checks if paddle touches puck
    """
    global puck_velx, puck_vely
    distance = np.sqrt((paddlex - puckx)**2 + (paddley - pucky)**2)
    touch = distance <= 30
    if touch:
        return move_puck(paddlex, paddley, puckx, pucky)
    else:
        return puck_velx, puck_vely

    
def move_puck(paddlex, paddley, puckx, pucky):
    """
    returns new x and y velocities of the puck after a touch
    """    
    vectx = puckx - paddlex
    vecty = pucky - paddley   
    if vectx == 0:
        vectx = 0.01        
    angle = np.arctan(vecty/vectx)
    if vectx < 0:
        angle += np.pi        
    return (puck_vel*np.cos(angle), puck_vel*np.sin(angle))

def puck_border_check(x,y,rad, velx, vely):
    """
    checks whether the puck has hit one of the borders, different condition 
    for each wall and net
    """
    if x < rad:
        if y <= window_height//2 - goal_size//2 or y >= window_height//2 + goal_size//2:
            velx = abs(0.95*velx)
            return velx, vely
        else:
            return 0,0
    if x > 590:
        if y <= window_height//2 - goal_size//2 or y >= window_height//2 + goal_size//2: 
            velx = -abs(0.95*velx)
            return velx, vely
        else:
            return 0,0
    if y < rad:
        vely = abs(0.95*vely)
        return velx,vely
    if y >= 390:
        vely = -abs(0.95*vely)
        return velx,vely
    else:
        return velx, vely

def check_goal(x,y,rad):
    """
    checks whether a goal has been scored
    """
    if y >= window_height//2 - goal_size//2 and y <= window_height//2 + goal_size//2 and x < rad:
        return 'leftgoal'
    if y >= window_height//2 - goal_size//2 and y <= window_height//2 + goal_size//2 and x > 590:
        return 'rightgoal'
    else:
        return None
        
    
def goal(bodcheck, left_score, right_score):
    """
    does goal score stuff
    """
    global puck_x
    global puck_y

    L_paddle_x = window_width//5
    L_paddle_y = window_height//2 

    R_paddle_x = window_width - window_width//5
    R_paddle_y = window_height//2
     
    if bodcheck == 'leftgoal':
        puck_x = window_width//2 - 50
        puck_y = window_height//2
        right_score += 1
        
    if bodcheck == 'rightgoal':
        puck_x = window_width//2 + 50
        puck_y = window_height//2
        print ('goal: rightgoal')
        left_score += 1
        
    print ('done checking')  
    return puck_x, puck_y, L_paddle_x, L_paddle_y, R_paddle_x, R_paddle_y, left_score, right_score
        
def paint_ice(win):
    """
    makes the background of win look like a hockey rink
    """
    window.fill((WHITE))
    
    pygame.draw.ellipse(window, (90,90,250), [-75, 125, 150, 150])    
    pygame.draw.ellipse(window, RED, [-75, 125, 150, 150], 2)
    
    pygame.draw.ellipse(window, (90,90,250), [window_width-75, window_height//2 - 75, 150, 150])    
    pygame.draw.ellipse(window, RED, [window_width-75, window_height//2 - 75, 150, 150], 2)
    
    pygame.draw.line(window, RED, (window_width//2, 0), (window_width//2, window_height),width=5)
        
    return None

def draw_paddle(posx,posy,rad,side):
    """
    draws a paddle at posx, posy of radius rad for the side indicated by... side
    """
    if side == 'left':
        pygame.draw.circle(window, BLACK, (posx,posy),rad)
        pygame.draw.circle(window, RED, (posx,posy),rad-2)
        pygame.draw.circle(window, (150,0,0), (posx,posy),rad-10)
    if side == 'right':
        pygame.draw.circle(window, BLACK, (posx,posy),rad)
        pygame.draw.circle(window, BLUE, (posx,posy),rad-2)
        pygame.draw.circle(window, (0,0,150), (posx,posy),rad-10)
    return None


def draw_score(l,r):
    """
    draws the score down l is left(red), r is right (blue)
    """
    font = pygame.font.SysFont('comicsansmsbold', 30)
    text = font.render('{} - {}'.format(l,r), True, BLACK)
    window.blit(text,[window_width//2 - 40,5])   
    return None

### main loop
count = 0
while run:
    count += 1
    pygame.time.delay(30)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()    

    #### draw background
    paint_ice(window)
    
    #### update paddle movement from key press
    L_paddle_x, L_paddle_y = move_paddle('left',L_paddle_x,L_paddle_y,paddle_r)
    R_paddle_x, R_paddle_y = move_paddle('right',R_paddle_x,R_paddle_y,paddle_r)
      
    #### update puck movement if touched by paddle
    puck_velx, puck_vely = touch_puck(L_paddle_x, L_paddle_y, puck_x, puck_y)
    puck_velx, puck_vely = touch_puck(R_paddle_x, R_paddle_y, puck_x, puck_y)
    
    #### check if puck hits border
    puck_velx, puck_vely = puck_border_check(puck_x, puck_y, puck_r, puck_velx,puck_vely)

    #### check if it went in goal
    if check_goal(puck_x, puck_y, puck_r) == 'leftgoal' or check_goal(puck_x, puck_y, puck_r) == 'rightgoal':
        puck_x, puck_y, L_paddle_x, L_paddle_y, R_paddle_x, R_paddle_y, \
        left_score, right_score = goal(check_goal(puck_x, puck_y, puck_r), left_score, right_score)
        
    puck_x += puck_velx
    puck_y += puck_vely
    
    #draw puck
    pygame.draw.circle(window, BLACK, (puck_x,puck_y), 10)
    
    #draw paddles
    draw_paddle(L_paddle_x,L_paddle_y,paddle_r,'left')    
    draw_paddle(R_paddle_x,R_paddle_y,paddle_r,'right') 
    
    #draw score
    draw_score(left_score, right_score)
        
pygame.quit()
            
