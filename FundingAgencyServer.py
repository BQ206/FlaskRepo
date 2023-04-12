from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO,join_room
import subprocess
import FundingAgency
import Researchers
import University
import uuid

from multiprocessing import Process

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on("onconnect")
def oncconnect():
    UniqueID = str(uuid.uuid4())
    print("fsa")
    print(UniqueID)
    join_room(UniqueID)
    data = {
        "UniqueID" : UniqueID
    }
    socketio.emit('connected',data,room=UniqueID)

@app.route('/')
def Funding():
    print("fsas")
    FundingAgency.createTable()
    return render_template('FundingAgencyHTML.html')


@socketio.on("getProposals")
def getProposals(data):
    i = 0
    UniqueID = data['UniqueID']
    Tble = data['proposal']
    getProposalsList = FundingAgency.getProposals(Tble)
    print("inforOnlns")
    print(data['InfoOnly'])
    while(i < len(getProposalsList)):
        ProposalTitle = getProposalsList[i][0]
        print(ProposalTitle)
        data = {
            "Title" : ProposalTitle,
            "ID" : getProposalsList[i][1],
            "Table" : Tble,
            "InfoOnly" : data['InfoOnly']
        }
        socketio.emit('ProposalTitles', data,room=UniqueID)
        i += 1

@socketio.on("ProposalInformation")
def getInformation(data):  
    UniqueID = data['UniqueID']
    proposalInformationList = FundingAgency.getProposalInformation(data['proposal'],data['ID'])
    print(proposalInformationList)
    i = 0
    Name = FundingAgency.getResearcher(proposalInformationList[i][3])
    data = {
        "Title" : proposalInformationList[i][0],
        "ProjectDescription" : proposalInformationList[i][1],
        "FundAmount" : proposalInformationList[i][2],
        "ID" : data['ID'],
        "Name" : Name
    }
    socketio.emit('ProposalInformation', data,room=UniqueID)
    print(proposalInformationList[i][2])
    i += 1


@socketio.on("SetProposalAccepted")
def setStatus(data):
    print(data['ID'])
    FundingAgency.ProposalAccepted(data['ID'],data['Budget'] , data['endDate'])

@socketio.on("SetProposalRejected")
def setStatus(data):
    print(data['ID'])
    FundingAgency.ProposalRejected(data['ID'])

if __name__ == "__main__":
    socketio.run(app, debug = True,port=5001)
