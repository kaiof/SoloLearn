from __future__ import print_function   # Home conflict; strip at SoloLearn

# Just hit Run with NO INPUT.
# You're new! You'll get instructions.

import socket, ssl, json #, urllib.parse as urlp
from random import randint

###### Identify your saved state #####
myID=""    # Provided to new players #
myPass=""  # Up to you:theft control #
######################################
# 
# Done the 'hard' way due to missing imports
# and a SoloLearn bug. TODO: Move queries
# off program and switch sheets.
######################################

# Solo:  ....V....X....V....X....V...
def printInstructions(id):
  print("Instructions   [          ]")
  print("Copy the ID above into myID")
  print("You may set the password   ")
  print("NOW (not later). When you  ")
  print("want to start a new maze,  ")
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
  print("Movement: l   r     L   R  ")
  print("            d         D    ")
  print("        >Treasure  >Offense")
  print("\n--- No input: View state.")
  print("Version " + progInfo["version"] + progInfo["verXtra"])

# Program vars
wall = "*" # chr(233)
playerChar = "@"

progInfo = {
  "name" : "pyMazeRun",
  "version" : "0.1",
  "verXtra" : "(alpha)",
}

gameStuff = {
  "maze" : (),  # TODO: Convert to hexadecimal
  "meX" : 1,  #TODO: Default start, v1 mazes
  "meY" : 19,
  "events" : (),
  "treasures" : ()
}

def RestoreSavedState():
  global gameStuff
  
  # TODO: Delete test data
  # ------------------------------------------------
  gameStuff["maze"] = (
    1099510579198,586263037986,733365644202,732426183306,734102798074,
    696458446850,818992050158,561040728098,1078014753722,695828777130,
    754752352170,586833600554,802084863978,561038532642,1029428981678,
    586407749794,1076890630842,560629711498,820069973690,697941265058,
    1078014503598,560537936522,801995668202,696366170658,755640303546,
    698069058082,802067234542,689351172642,824629258938,558382090914,
    802066971566,723737682466,755842920186,584688085154,1025137175470,
    698612197930,801745119978,552442298882,1099510579198,0
  )
    
  # TODO: maze, events, treasures
  # TODO: Locate player at correct spot in maze

def printMaze():
  global wall
  i=0; meX,meY = gameStuff["meX"], gameStuff["meY"]
  
  for rowInt in gameStuff["maze"]:
    if(rowInt == 0): break; # TODO: Optimize generator
    
    mazeExpand = [int(x) for x in bin(rowInt)[2:]]
    outLine = [wall if c==1 else " " for c in mazeExpand]
    if(i==meX): outLine[meY] = playerChar;
    print(''.join(outLine))
    i += 1

def printStats():
  print("Stats: TODO")  #TODO
  pass

def retrieveNewID():
  return("TODO:")

def SaveState():
  # TODO:
  pass

def getVisibleMaze():
  # TODO:
  pass
  
def game():
  if(playerChar == wall):
    print("WARNING: Player character same as walls!")
  if(myID==""):
    printInstructions(retrieveNewID())
    quit()

  sInput = raw_input("Your command: ")

  RestoreSavedState()
  printMaze()
  printStats()

  if (sInput.strip() == ""):
    # SoloLearn effect: No input = print maze. Home effect: might continue.
    quit()

  if (not validInput(sInput) ):
    print("Invalid input detected.")
    printValidInputs()
    quit()

game()

"""

def getLastMsg():
  cr=chr(13)+chr(10); dcr=cr+cr
  qry=urlp.urlencode({"tq":YourQuery})
  server="docs.google.com"
  wkaround=["GET ",
    '/spreadsheets/d',
    '/165j5AGZZOotBpztjkt0JsEcPLeNBYO8S7fSlsdTgkug/gviz',
    '/tq?{} HTTP/1.1'.format(qry) + cr,
    'Host: {}'.format(server) + dcr,
  ]

  ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  s = ssl.wrap_socket(ss, ssl_version=ssl.PROTOCOL_TLSv1, ciphers="ALL")
  s.connect((server,443))
  [s.send(q.encode()) for q in wkaround]
  
  c=0
  while True:
    resp = s.recv(4096).decode() # hardcoded/known reads
    # print("[{}]".format(c), resp,)  
    if(c==1): injson = resp
    if(c==2): break    # last read has len 0
    c+=1

  s.close()
  
  paren=injson.find("(")+1
  oData = json.loads(injson[paren:-4])
  
  try:
    row=oData["table"]["rows"][0]["c"]
    print("Last: {}".format(row[0]["f"]) )
    print(" App: {}".format(row[1]["v"]) )
    print("Uniq: {}".format(row[2]["v"]) )
    print(" Seq: {}".format(row[3]["v"]) )
    print(" Msg: {}".format(row[4]["v"]) )
  except Exception as e:
    print(e)
  else:
    print("*"*35)
    import pprint
    pp=pprint.PrettyPrinter(width=38)
    pp.pprint(oData) 
  
def postNewMsg(m):
  cr=chr(13)+chr(10); dcr=cr+cr
  server="script.google.com"
  wkAround=['POST ',
    '/macros/s',
    '/AKfycbxmW9vaqyRPaVSpg1igeq',
    'Y6aQHaDwLewR2njuRjvj8k3oXQ2dg',
    '/exec HTTP/1.1' +cr, 'Host: {}'.format(server)+cr,
  ]
  
  ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  s = ssl.wrap_socket(ss, ssl_version=ssl.PROTOCOL_TLSv1, ciphers="ALL")
  s.connect((server,443))
  [s.send(q.encode()) for q in wkAround]
  
  data={'app':YourApp,            # change it!
        'unique':YourUnique,      # demo data
        'sequence': YourSequence, # demo data
        'data':m}                 # demo message
  safedata=urlp.urlencode(data)
  
  s.send(("Content-Length: "+str(len(safedata)) + cr).encode())
  s.send(("Content-Type: application/x-www-form-urlencoded"+dcr).encode())
  s.send((safedata).encode())

  c=0
  while True:
    resp = s.recv(4096).decode() # fragile but fixable
    # print("[{}]".format(c), resp,) # ignore 302 redir atm
    break
    c+=1

  s.close()
  
getLastMsg()
print("sending message...")
postNewMsg(YourMessage)
"""