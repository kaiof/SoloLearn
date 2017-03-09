# HOME (simpler!) version. An import is missing for SoloLearn. SoloLearn version here: https://code.sololearn.com/cJTcw0o5WgaZ/?ref=app
import requests, json
from random import randint

# Program prints last msg (from Google sheets) + adds yours.

YourApp="HomeVersion"
YourUnique="ha-" + str(randint(0,1024**2))
YourSequence=str(randint(0,1024**2))
YourMessage=input("What's your message? ")

# See all data: https://sites.google.com/site/sllkspersist

def getLastMsg():
  qry={"tq":"select * order by A desc limit 1"}
  url = "https://docs.google.com/spreadsheets/d/165j5AGZZOotBpztjkt0JsEcPLeNBYO8S7fSlsdTgkug/gviz/tq"
  r = requests.get(url, params=qry)
 
  injson=r.text   # json
  paren=injson.find("(")+1
  oData = json.loads(injson[paren:-2])
  
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
  postdata={'app':YourApp,        # change it!
        'unique':YourUnique,      # demo data
        'sequence': YourSequence, # demo data
        'data':m}                 # demo message
  
  url="https://script.google.com/macros/s/AKfycbxmW9vaqyRPaVSpg1igeqY6aQHaDwLewR2njuRjvj8k3oXQ2dg/exec"
  r = requests.post(url, data=postdata)
  
getLastMsg()
print("Sending message...")
postNewMsg(YourMessage)