# SoloLearn-imports compatible. Home-simpler!-version here: https://code.sololearn.com/c37XERvwb2Cz/?ref=app
import socket, ssl, json, urllib.parse as urlp
from random import randint

# Program prints last msg (from Google sheets) + adds yours.
YourApp="pyPersist"
YourUnique="pyp-"+str(randint(0,1000000))
YourSequence = str(randint(0,1000000))
YourQuery="select * order by A desc limit 1"

YourMessage="Anonymous was here."
# YourMessage=input("What's your message? ")

# See all data: https://sites.google.com/site/sllkspersist

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