# -*- c o d i n g: u t f - 8 -*-
# Mazemaker ported from thenerdshow.com's aMaze (both javascript and C, with my modifications).
# It also didn't draw boxes the way I needed so I fixed that. This is a spanning tree, so
# there is always one solution.

#print sys.stdout.encoding

#import struct
#print u'\xe9'
#print struct.pack('B', 218)

space = " "
wall= '*'  

# safechars = ["+", 231, 232, 233, 234, 235-?-245, 246, 247, 248, -249, 250

import math
from random import randint

def mazeInit(rows, cols, wall):
  a = [[wall for y in range(2*cols+1)] for x in range(2*rows+1)]
  return a

def mazeStep(a, rows, cols, r, c):
  vector=[[0 for i in range(2)] for j in range(3)]
  
  def R(val):
    if(val==None): return vector[i][0]
    vector[i][0]=val
    
  def C(val):
    if(val==None): return vector[i][1]
    vector[i][1]=val
    
  while True:
    i=0; 
    if(r > 1          and a[r-2][c  ] != " "): R(r-2); C(c); i+=1
    if(r < rows*2 - 1 and a[r+2][c  ] != " "): R(r+2); C(c); i+=1
    if(c > 1          and a[r  ][c-2] != " "): C(c-2); R(r); i+=1
    if(c < cols*2 - 1 and a[r  ][c+2] != " "): C(c+2); R(r); i+=1
    
    # i is never > 3 because path behind is cleared
    if(i==0): break;  # check for deadend;
    
    i=int(i * randint(0,32767)/32767) # Emulate the c++ thing (even though I just need an int 0..i-1

    a[int( (R(None)+r)/2 )][int( (C(None)+c)/2 )]=" "  # Knock out wall
    a[             R(None)       ][             C(None)       ]=" "  # Clear to it

    mazeStep(a, rows, cols, R(None), C(None))

def mazeWalk(maze, rows, cols):
  i=r=c=0
  
  c=cols|1;
  maze[0][c]=" ";
  maze[2*rows][c]=" "
  
  i=randint(0,1) # I think they're doing a 50/50 thing in C++
  c=1 if i else 2*cols-1
  r=rows | 1
  maze[r][c]=" "                    # Make a hole
  mazeStep(maze, rows, cols, r, c)

"""
def mazeXlate(a, rows,cols,x,y):
  # public wall
  # bitmask : UDLR
  bitmask = 0
  U=8; D=4; L=2; R=1
  pieces={
      0       : space, # " ",
      D+R     : u"\u250c", #str(218).decode('utf=8'),    # top left
      L+R     : "-", # u"\u2500", # chr(196),    # horizontal
      D+L+R   : u"\u252c", # chr(194),  # T
      D+L     : u"\u2510", # chr(191),    # top right
      U+D+L   : u"\u2524", # chr(180),  # -|
      U+D     : ":", # u"\u2502", # e29482", # chr(179),    # vertical
      U+L     : u"\u2518", # chr(217),    # bottom right
      U+L+R   : u"\u2534", # chr(193),  # _|_
      U+R     : u"\u2514", # chr(192),    # bottom left
      U+D+R   : u"\u251c", # chr(195),  # |-
      U+D+R+L : u"\u253c", # chr(197),  # +

      U: "|", # u"\u2502", # chr(179),   # perpendiculars from edges (no other side)
      D: "|", #u"\u2502", # chr(179),
      L: "-", #u"\u2500", # chr(196),
      R: "-", #u"\u2500", # chr(196),
  }

  def cr():
    return (R if a[x][y+1] == wall else 0) if y<cols else 0
  def cl():
    return (L if a[x][y-1] == wall else 0) if y>0 else 0
  def cu():
    return (U if a[x-1][y] == wall else 0) if x>0 else 0
  def cd():
    return (D if a[x+1][y] == wall else 0) if x<rows else 0

  return(pieces[cr()+cl()+cu()+cd()]) 
"""

def mazePrint(a, rows, cols, color):
  target = open('mazeout.txt', 'a')

  for i in range(0,2*rows+1):
    # print(''.join(q) for q in a[i][(j for j in range(0,2*cols+1) )])
    l=[]; r=[]
    binout=0
    max = 2*cols+1
    for j in range(0,max):
      if (a[i][j]==wall):
        # l.append( mazeXlate( a,rows,cols,i,j ) )
        r.append(wall)
        binout += 2**(max-j)
      else: 
	    #l.append(" "); 
		r.append(" ")
    target.write(str(binout) + ",")

    ll = [int(x) for x in bin(binout)[2:]]
    l = [wall if c==1 else " " for c in ll]
    print ''.join(r) + " | " + ''.join(l)
  target.write("0\n")
  target.close()

square=19
rows=square
cols=square

color=0

a=mazeInit(rows, cols, wall)
mazeWalk(a, rows, cols)
mazePrint(a, rows, cols, 0)
