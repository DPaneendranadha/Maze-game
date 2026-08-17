import sys
from numpy import random
height=800
yaxis=[x for x in range(0,height) if x%40==0]
def path(s,e,vertices):
 # print("path called with s =", s, "and e =", e)
  if e-s>200:
   
   xaxis=[a for a in range(s,e) if a%40==0]
  # print(xaxis)
   x=random.choice(xaxis) 
   y=random.choice(yaxis)
   #print(x,y)
   vertices.append([x,y])
   path(s,x,vertices)
   path(x,e,vertices)
def draw(x,y,x1,y1):
              #40 is the dimension of the block
     while x<x1:
       x+=40
       trail.append([x,y])
       
     if y<y1:
      
      while y<y1:
       y+=40
       trail.append([x,y])
       
     elif y>y1:
      
      while y>y1:
       y-=40
       trail.append([x,y])  

def final_path():

 points=[] 
 trail=[]
 path(0,1000,points)
 a,b=0,0
 for x in points:
  draw(a,b,x[0],x[1])
  a,b=x[0],x[1]
#vertices also gets included in the trail
 trail.sort()
 


