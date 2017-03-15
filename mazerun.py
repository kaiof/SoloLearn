# Just hit Run with NO INPUT.
# You're new! You'll get instructions.

import socket, ssl, json, urllib.parse as urlp, string
from random import randint, choice
# import multiprocessing # memory seems ok

###### Identify your saved state #####
myID=""    # Provided to new players #
myPass=""  # Up to you:theft control #
onSoloLearn=True                     #
######################################

# Solo:  ....V....X....V....X....V...
def printInstructions():
  print("Instructions   [{}]".format(myID))
  print("Copy the ID above into myID")
#  print("You may set the password   ")
#  print("NOW (not later). When you  ")
#  print("want to start a new maze,  ")
  print("Start over?")
  print("just reset the ID to empty.")
  print("\n ** From now on: ")
  print("Enter as many movements as ")
  print("You want. You will STOP")
  print("for events, walls, monsters")
  print("treasure, etc.")
  printValidInputs()

def printValidInputs():
  print("---------  INPUTS ---------")
  print("          Normal    Attack ")
  print("            u         U    ")
  print("Movement: l . r     L * R  ")
  print("            d         D    ")
  print("        >Treasure  >Offense")
  print("Ex: uu*RRDdldru          ")
  print("        * fight in place   ")
  print("\nNo input = review state. ")

# Variables
############################################################
wall, playerChar = [chr(246), chr(232)] if onSoloLearn else ["*", "@"]

progInfo = {
  "name" : "pyMazeRun",
  "version" : "0.1",
  "verXtra" : "(alpha)",
}

gameStuff = {
  "maze" : { "ints":(), "text":[] },  # TODO: Convert to hexadecimal
  "lastX" : 0,
  "lastY" : 0,
  "nowX" : 1,  #TODO: Default start, v1 mazes
  "nowY" : 19,
  "events" : (),
  "treasures" : ()
}

cr = chr(13) + chr(10); dcr = cr+cr
workarounds = {
  "getState" : {
    "server" : "docs.google.com",
    "port" : 443,
    "qry" : urlp.urlencode({"tq": "select * where B='{}' and C='{}' order by A desc limit 1".format(progInfo["name"], myID) }),
    "lines" : [  # Bug workaround
      "GET ",
      '/spreadsheets/d',
      '/165j5AGZZOotBpztjkt0JsEcPLeNBYO8S7fSlsdTgkug/gviz',
    ]
  },
  "postMsg" : {
    "server" : "script.google.com",
    "port" : 443,
    "lines" : [
      'POST ',
      '/macros/s',
      '/AKfycbxmW9vaqyRPaVSpg1igeq',
      'Y6aQHaDwLewR2njuRjvj8k3oXQ2dg',
    ]
  },
}

def openSocket(server, port):
  """ TODO: Handle Exceptions: OSError et al
  """
  ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # IPv4, data stream
  s = ssl.wrap_socket(ss, ssl_version=ssl.PROTOCOL_TLSv1, ciphers="ALL")
  s.connect((server,port))
  return s

def RestoreSavedState():
  global gameStuff
  gsm = gameStuff["maze"]

  global cr, dcr, workarounds
  wka=workarounds["getState"]
  
  # TODO: Alpha test; add loader
  # ------------------------------------------------
  gsm["ints"] = (
    1099510579198,586263037986,733365644202,
    732426183306,734102798074,696458446850,
    818992050158,561040728098,1078014753722,
    695828777130,754752352170,586833600554,
    802084863978,561038532642,1029428981678,
    586407749794,1076890630842,560629711498,
    820069973690,697941265058,1078014503598,
    560537936522,801995668202,696366170658,
    755640303546,698069058082,802067234542,
    689351172642,824629258938,558382090914,
    802066971566,723737682466,755842920186,
    584688085154,1025137175470,698612197930,
    801745119978,552442298882,1099510579198,0
  )
    
  # TODO: maze, events, treasures
  # TODO: Locate player at correct spot in maze
  
  qry, lines, server, port = wka["qry"], wka["lines"], wka["server"], wka["port"]
  lines.append('/tq?{} HTTP/1.1'.format(qry) + cr)
  lines.append('Host: {}'.format(server) + dcr)

  s = openSocket(server, port)
  [s.send(q.encode()) for q in lines]

  res = getResponse(s, 1)
  # s.shutdown(SHUT_RDWR) # supposed to do this, but constants not defined
  s.close()

  paren=res.find("(")+1
  oData = json.loads(res[paren:-4])

  try:
    rows=oData["table"]["rows"]
    if(len(rows) == 0):
      raise Exception("Something's wrong. No results to query.")

    row=rows[0]["c"]                       # TODO: Reusing these for now
    
    data = eval(row[4]["v"])
    gameStuff["nowX"] = int(data["nowX"])
    gameStuff["nowY"] = int(data["nowY"])
  except Exception as e:
    print("Exception while loading data" + "*"*35)
    print(e)
  #finally:    # debugging
  #  print("*"*35)
  #  import pprint
  #  pp=pprint.PrettyPrinter(width=38)
  #  pp.pprint(oData) 

def loadMaze():
  global wall, gameStuff
  gsm = gameStuff["maze"]
  i=0; nowX,nowY = gameStuff["nowX"], gameStuff["nowY"]
  
  for rowInt in gsm["ints"]:
    if(rowInt == 0): break; # TODO: Optimize generator
    
    mazeExpand = [int(x) for x in bin(rowInt)[2:]]
    outLine = [wall if c==1 else " " for c in mazeExpand]
    if(i==nowX): outLine[nowY] = playerChar;
    o=''.join(outLine)
    gsm["text"].append(o)
    i += 1

def printMaze():
  for o in gameStuff["maze"]["text"]:
    print(o[:-1])

def tryToMove(moves):
  # TODO: Convert to class for self variables
  global gameStuff
  maze=gameStuff["maze"]["text"]
  
  hitwall=False
  stop=False  # TODO: Confusion
  
  def up(x,y):
    stop=illegal=hitWall=False
    if x==0:
      illegal=True
      stop=True
    else:
      if maze[x-1][y] == wall:
        hitWall=True
        stop=True
      else:
        gameStuff["nowX"] -= 1
    return([stop, illegal, hitWall])
        
  #def HW():
  #  hitWall=True
  #  stop=True
  #def ILL():
  #  illegal=True
  #  stop=True
        
  def down(x,y):
    stop=illegal=hitWall=False
    if x==len(maze):
      illegal=True
      stop==True
    else:
      if maze[x+1][y] == wall:
        hitWall=True
        stop=True
      else:
        gameStuff["nowX"] += 1
    return([stop, illegal, hitWall])
        
  def left(x,y):
    stop=illegal=hitWall=False
    if y==0:
      illegal=True
      stop=True
    else:
      if maze[x][y-1] == wall:
        hitWall=True
        stop=True
      else:
        gameStuff["nowY"] -=1
    return([stop, illegal, hitWall])
        
  def right(x,y):
    stop=illegal=hitWall=False
    if y==len(maze[0]):
      illegal=True
      stop=True
    else:
      if maze[x][y+1] == wall:
        hitWall=True
        stop=True
      else:
        gameStuff["nowY"] += 1
    return([stop, illegal, hitWall])
  
  def passIt():  # use later
    pass
    
  options={
    'l' : left,    'L' : left,
    'u' : up,      'U' : up,
    'r' : right,   'R' : right,
    'd' : down,    'D' : down,
    '.' : passIt,  '*' : passIt,
  }
  
  for c in moves:
    flags = options[c](gameStuff["nowX"], gameStuff["nowY"])
    if flags[0]:
      if flags[1]:
        print("Illegal move!")
      if flags[2]:
        print("You hit a wall!")
      break

def printStats():
  print("Stats: Gold, health, messages...TODO")  #TODO
  pass

def retrieveNewID():
  global myID
  myID = ''.join(choice(string.ascii_letters + string.digits) for _ in range(8))

# TODO: client during alpha; "server" later. 
# TODO: Update instead of appending (though append provides history)
def writeState():
  global cr, dcr, workarounds, myID
  wka=workarounds["postMsg"]
  
  lines, server, port = wka["lines"], wka["server"], wka["port"]
  lines.append('/exec HTTP/1.1' +cr)
  lines.append('Host: {}'.format(server)+cr)    # Todo: Password

  s = openSocket(server, port)
  [s.send(q.encode()) for q in lines]

  pi = progInfo
  gs = gameStuff
  
  data={'app': pi["name"],
        'unique': myID,            # TODO: insecure during alpha
        'sequence': pi["version"], # TODO: if !timestamp works
        'data': { 
          'myID' : myID,
          'nowX' : gs["nowX"],
          'nowY' : gs["nowY"],
          'api'  : pi["version"],
        }
  }
  safedata=urlp.urlencode(data)
  
  s.send(("Content-Length: "+str(len(safedata)) + cr).encode())
  s.send(("Content-Type: application/x-www-form-urlencoded"+dcr).encode())
  s.send((safedata).encode())

  res=getResponse(s, 0)

  # s.shutdown()
  s.close()
  
  return(myID)

def SaveState():
  # TODO:
  pass

def getVisibleMaze():
  # TODO:
  pass

# fix this - packet 1 for 1 type, packet 2 for the other
def getResponse(sock, thisOne):
  chunks=[]
  bytes_recd=0
  while True:
    chunk = sock.recv(8192) # min(expected, 2048)
    if chunk == b'':
      raise RuntimeError("Socket connection broken")
    chunks.append(chunk)
    bytes_recd=bytes_recd + len(chunk)
    if chunk == b'0\r\n\r\n':
      # no more data
      break
    if chunk[:30] == b'HTTP/1.1 302 Moved Temporarily':  # ignore server redirect for now
      break
  return chunks[thisOne].decode()   # b''.join(chunks)
  
def game():
  if(playerChar == wall):
    print("WARNING: Player character same as walls!")
  if(myID==""):
    retrieveNewID()
    printInstructions()
    writeState()
    quit()

  # restore state. If input is blank, always print map and stats, then quit
  #   If not on sololearn:                         print map+stats, take input (blank:printquit), try to move, update, print map and stats, quit() - should restart
  #   If on sololearn, take input. If it's blank,  printquit
  #                                if it's moves,                              try to move, update, print map and stats, quit

  RestoreSavedState()
  loadMaze()
  if not onSoloLearn:
    printMaze()
    printStats()

  sInput = input("Your command: ")
  if (sInput.strip() == ""):
    if onSoloLearn:
      printMaze()      # don't duplicate off SoloLearn
      printStats()
    quit()

  if not onSoloLearn:
    tryToMove(sInput)
    writeState()
    loadMaze()
    printMaze()
    
  if onSoloLearn:
      #printMaze()   # oops. Loads text maze too
      tryToMove(sInput)
      writeState()
      loadMaze()
      printMaze()
      printStats()

game()