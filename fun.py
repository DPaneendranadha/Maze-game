import pygame
import sys
from numpy import random

def rect(x,y,w,h,color,surface):
     """
     To draw the rect with dimensions and position on a surface
     """
     rectangle = pygame.Surface((w, h))
     rectangle.fill(color)
     surface.blit(rectangle, (x,y))
def path(s,e,vertices,level,dim,axis):
        '''
            To find out points on the maze which are then used to draw a path
            from a start point to end point using draw function
            Parameters
            ----------
            s : int
                start point(here it is (0,0,))
            e : int
                end point ( end point will be random )
            level will basically decide the no.of vertices in the path and this
            path will have xcoordinates in increasing order
            
        '''
        if e-s>level:
           xaxis=[a for a in range(s,e) if a%dim==0]
           x=random.choice(xaxis) 
           y=random.choice(axis)
           vertices.append([x,y])
           path(s,x,vertices,level,dim,axis)
           path(x,e,vertices,level,dim,axis)
def draw(x,y,x1,y1,dim,trail):
      '''
         Now from the vertices in path we will draw the way 
         between two consecutive points given in draw() 
         first via x-axis and then via y-axis
      '''
      while x<x1:
       x+=dim
       trail.append([x,y])
       
      if y<y1:
      
       while y<y1:
        y+=dim
        trail.append([x,y])
       
      elif y>y1:
       while y>y1:
        y-=dim
        trail.append([x,y])  

# Define a function for BFS
def bfs(grid, start, end, d):
    visited = set()
    queue = [(start, [])]

    while queue:
        current_point, path = queue.pop(0)

        if current_point == end:
            return path + [current_point]

        visited.add(current_point)

        x, y = current_point
        neighbors = [(x + d, y), (x - d, y), (x, y + d), (x, y - d)]
        for neighbor in neighbors:
            if neighbor not in visited and neighbor in grid:
                queue.append((neighbor, path + [current_point]))

    return None  # No path found
def trail_convert(p):
    '''
    To write solution.txt
    '''
    i=0
    solution=[]
    while i<len(p)-1:
     if p[i+1][0] - p[i][0]==50:
        solution.append("R")
     elif p[i+1][1] - p[i][1]==50:
        solution.append("D")
     elif p[i+1][1] - p[i][1]==-50:
        solution.append("U")
     i+=1
    return solution

   
   