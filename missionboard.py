import re
import requests
import json
import uuid
import time
from post import postimage

Teamlist = []
NumberOfTeamsMax=20
MissionResultArray=[]

i=0
while i <=NumberOfTeamsMax:
    i=i+1
    a=[]
    MissionResultArray.append(a)

def generatebarvaluestring():
    barvaluestring='1,1,1,0,1,1|1,0,1,1,1,0|1,0,1,1,1,0'

    return barvaluestring

def generateteamlabels():
    labels=''
    for i in Teamlist:
        if int(i) == 1:
            labels=labels+'|Team '+i+'|'
        else:
            labels=labels+'Team '+i+'|'
    return (labels)

def renderboard():

    labels=generateteamlabels()
    barvalues=generatebarvaluestring()
    testurl="https://chart.googleapis.com/chart?cht=bhs&chs=500x300&chxt=x,y&chd=t:"+barvalues+"&chtt=Missionsstatus&chxl=1:"+labels+"&chds=a&chco=4D89F9,C6D9FD,D6D9FD"    
    r = requests.get(url=testurl, allow_redirects=True)
    open('graph.png', 'wb').write(r.content)
    postimage('graph.png')
    return 'to be done'

    

def checkandaddteam(jsondata,data,team,mission,result,entryid):


    print (jsondata)
    global Teamlist
    global MissionResultArray
    t = time.localtime()
    str(uuid.uuid1())
    if entryid==0:
        entryid=str(uuid.uuid1()) 
    teamobject= eval('{"id": "'+entryid+'","Mission": "'+str(mission)+'","Team": "'+str(team)+'","Time": "'+str(time.strftime("%H:%M:%S", t))+'","Result": "'+str(result)+'"}')

    team=int(jsondata['Team'])
    if str(team) in Teamlist:
        if team in MissionResultArray[team]:
            print ('Missionstatus bereits gespeichert')
        else:
            MissionResultArray[team].append(jsondata['Mission'])
                
    else:
        print ('Team noch nicht gelistet')
        Teamlist.append(jsondata['Team'])
        if teamobject['id'] != entryid:
            data['Missions'].append(teamobject) #Hier ist der Fehler
        MissionResultArray[team].append(jsondata['Mission'])
        
    return jsondata

def load():
    count=0
    with open("stats.json") as fobj_in:
        data = json.load(fobj_in)

    for Mission in data['Missions']:
        numberofmission=int(Mission['Mission'])
        numberofteam=int(Mission['Team'])
        entryid=(Mission['id'])
        result=Mission['Result']
        checkandaddteam(Mission,data,numberofteam,numberofmission,result,entryid)
    
    return (data)

def save(teamsstatlist):
    teamsstatlist=json.dumps(teamsstatlist,indent=4)
    with open('stats.json', 'w') as fobj_out:
        for line in teamsstatlist:
            fobj_out.write("%s" % line)
    print ('Teamstatistiken angepasst')



if __name__ == "__main__":

    print ('Lade Teamergebnisse')
    teamlist=load()
    #print (json.dumps(teamlist,indent=4))
    #print ('*****************')        
    print (MissionResultArray)
    renderboard() 
    #save(teamlist)
    generateteamlabels()



