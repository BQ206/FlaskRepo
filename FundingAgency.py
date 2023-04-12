import os 

from google.cloud.sql.connector import connector
import json
import sqlalchemy

INSTANCE_CONNECTION_NAME = f"lively-wave-340915:europe-west1:ca4006database" # i.e demo-project:us-central1:demo-instance
DB_USER = "admin"
DB_PASS = "food"
DB_NAME = "CA4006DB"

tst = {
  "type": "service_account",
  "project_id": "lively-wave-340915",
  "private_key_id": "dd9ed0f5626a32f292c74fa49d441ecd77f3d53f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCrjUk7ptQmBi+Z\nFlzd9fwLARze9rJa9WFMSld508X/xUMpgvy+TtoWcV0mxoU56+Am0kuqSEqLQ0Z8\nLUN+vk+EO09r+zl12sHfAG6Omy2jOwDbL2/Lp3pL/s3YBfftDcuAK+EU1KEEsVsG\nnoBEK+xwqq+lqDTUJYEfghZVkAPbDuMhf/aTyqoJyRkG8+WAOkI6CT9t18ByRJtr\nDAvZEVIF5zTN+exELIjmRNTrwuRdNCMNpE4XE/Z/EfR6dHUUmlrnwp0sJqiqxLIu\noCvmjTduRy7IUOxvwmAMInEA/urqSrmzPIoolFd4yYsIGtYHQk1aW84GADnROVrB\nSYJregbvAgMBAAECggEAAjpLylDfPojR4xmXbZ69ved4LkthGzpyQK5osBSVm5HU\nXR1k7FYw+At/MRpprxUrTT2G+kUmT5Phiv7ltOzhT+RgiQJAM3+Mx0RLPYax3FKC\nU92krMtAERGg11VRbCe1JbxbrbarmrsnRG/66OmMIqDBXrwfqY5zowvO8VMvn1iT\nbfgV2KN/qXqeZ5qTIbnMPQYHvxZRTXkPe5bDPWwX3eIioy3XMAwk+nRPamm6RZZO\nZ7J76PD+vx8Ks+aHlLYP2Op47CLemJrcSUv1xBh8u4SEGvdE9peR6Kfz2rYTd6ot\nibLcJjgJhWIvIzsoX1kn32V1/8fqQbRpL5TKw8DWoQKBgQDV6IeL4zJI/T9QSTwd\nvV/qeO47iFH23j0jHID3jIc6nvdjF5cZ/Hj/LqExrd7Tu+rxhav9S7d8AiknVfcT\n0EMr57lp7dIwRCIAb7y0EGH9KKHEP3Ao3FAay/LSRjFoSv58kmLu0bQb5mgMcWXs\nxte270CDAukgsraWkMMIxQw4oQKBgQDNTxV2KACUHZhxUu7i2dEtz6B0La4Qdb2J\nRlFMZCbDiixydsJMkPJlCDdQI42LX0hPgxHyUOaqF5wKfGW/Enz6PJHVIqzgYWs4\nL2BnltHrBDS49NC2rKB5aVgC0+tuB8ws+TIXBChugVG3m838CZMx0A5a+OxHEoJ/\nm5tClINFjwKBgGY1xMbX2cg8kgs34yzGt1UfUZ5KpfeS+52SWiFvGZKuMME9nWrC\nU8KDMmy9itKbYUjkuWi/zD3J/oYYMoZaJi6Ne/Acviln9ONGgOF9ToUb7CgMs/gi\nRXh4aV+GQMd3xiAaBoHc2/XU43TGnpBD9wEnUykGtAR2wH4zT64aEZvhAoGAMT10\nYkA500w90YAYdyPSfXA8hWCnTJ9Qc+n/eZjTizZKbrF47DAfUofj7D56piCWESvY\nVAt/JvA+pm0rYeYnP0TjnQCSAcabloAWWQHdGsaJdoqQvB8u5a+UQildX6hTGb4y\nez6uC8LMPIMLphUNznad2se0s18HGV/SnudLjJUCgYAFmuld61KDzwq07v9tH/lk\nkiAV/EQ0rZV4H1z2Ho9paw6nslp5lHuT/NV1sqogLDP3gvYEHBC0hJNZusC8xzDj\nGhkWAN81+5uGGwX19j9wtieA65ZdH6fYTu48MNAgac3eS8lOiL6cagFGvV1Un+Nq\n9xqkWrIXBwMgiuqH1NZy3A==\n-----END PRIVATE KEY-----\n",
  "client_email": "lively-wave-340915@appspot.gserviceaccount.com",
  "client_id": "107196161448967607355",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/lively-wave-340915%40appspot.gserviceaccount.com"
}

json_object = json.dumps(tst, indent=4)

# Writing to sample.json
with open("sample.json", "w") as outfile:
    outfile.write(json_object)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./sample.json"

import subprocess
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import threading                                                                
import functools                                                                
import time   
    
def createTable():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS AcceptedProposals
            (ID INT PRIMARY KEY     NOT NULL,
            ResearcherID    Int       NOT NULL,
            Title           TEXT    NOT NULL,
            ProjectDescription     TEXT     NOT NULL,
            FundingAmount    Int       NOT NULL);''')
    c.execute('''CREATE TABLE IF NOT EXISTS RejectedProposals
            (ID INT PRIMARY KEY     NOT NULL,
            ResearcherID    Int       NOT NULL,
            Title           TEXT    NOT NULL,
            ProjectDescription     TEXT     NOT NULL,
            FundingAmount    Int       NOT NULL);''')
    c.execute('''CREATE TABLE IF NOT EXISTS IdleProposals
            (ID INT PRIMARY KEY     NOT NULL,
            ResearcherID    Int       NOT NULL,
            Title           TEXT    NOT NULL,
            ProjectDescription     TEXT     NOT NULL,
            FundingAmount    Int       NOT NULL);''')
    c.execute('''CREATE TABLE IF NOT EXISTS ResearchAccount
            (ID INT PRIMARY KEY     NOT NULL,
            HolderID        Int     NOT NULL,
            ResearcherID    Int       NOT NULL,
            Title           Text        NOT NULL,
            Budget           TEXT    NOT NULL,
            EndDate     TEXT     NOT NULL);''')
    c.execute('''CREATE TABLE IF NOT EXISTS AddResearchers
            (ID INT PRIMARY KEY     NOT NULL,
            ResearcherID        Int     NOT NULL,
            ResearcherAddedID   Int     NOT NULL,
            ResearchAccountID   Int     NOT NULL,
            ResearcherName           TEXT    NOT NULL,
            OriginialResearchID     Int    NOT NULL );''')
    c.execute('''CREATE TABLE IF NOT EXISTS Transactions
            (ID INT PRIMARY KEY     NOT NULL,
            ResearcherID    Int       NOT NULL,
            AccountID       Int         NOT NULL,
            date           TEXT    NOT NULL,
            amount     Int     NOT NULL,
            Reason     Text     NOT NULL,
            FundingAmount    Int       NOT NULL);''')
    c.execute('''CREATE TABLE IF NOT EXISTS UniversityNotifications
            (ID INT PRIMARY KEY     NOT NULL,
            AccountID       Int         NOT NULL,
            date           TEXT    NOT NULL,
            Budget     Int     NOT NULL,
            Researcher     Text     NOT NULL);''')
    print("connected")
    conn.close()

def synchronized(wrapped):                                                      
    lock = threading.Lock()                                                     
    print (lock, id(lock)   )                                                     
    @functools.wraps(wrapped)                                                   
    def _wrap(*args, **kwargs):                                                 
        with lock:                                                              
            print ("Calling '%s' with Lock %s from thread %s [%s]"              
                   % (wrapped.__name__, id(lock),                               
                   threading.current_thread().name, time.time()))               
            result = wrapped(*args, **kwargs)                                   
            print ("Done '%s' with Lock %s from thread %s [%s]"                 
                   % (wrapped.__name__, id(lock),                               
                   threading.current_thread().name, time.time()))               
            return result                                                       
    return _wrap 

@synchronized
def ProposalSubmited(Title, ProjectDescription,FundAmount, ResearchID):
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    c.execute(' SELECT ID FROM AddResearchers ')
    infoID = c.fetchall()
    if(len(infoID) == 0):
        ID = 0
    else:
        ID = infoID[len(infoID) - 1][0]
    sql = "SELECT count(*) FROM AcceptedProposals WHERE ResearcherID = %s"
    val = (ResearchID)
    c.execute(sql, val)
    HolderID = c.fetchone()[0]
    if(int(FundAmount) >= 200 and int(FundAmount) <= 500):
        sql = "insert into AcceptedProposals (ID, ResearcherID, Title, ProjectDescription,FundingAmount) values (%s, %s, %s,%s,%s )"
        val = (ID + 1,ResearchID, Title, ProjectDescription,FundAmount)
        c.execute(sql, val)
        # default to 3 months for automatic acception 
        currentTimeDate = date.today() + relativedelta(months=3)
        currentTime = currentTimeDate.strftime('%Y-%m-%d')
        sql = "insert into ResearchAccount (ID, HolderID, ResearcherID, Title, Budget, EndDate) values (%s, %s, %s,%s,%s,%s )"
        val = (ID + 1,HolderID + 1,ResearchID,Title,FundAmount,currentTime)
        c.execute(sql, val)
    elif(int(FundAmount) >= 1000):
        c.execute(' SELECT ID FROM RejectedProposals ')
        infoID = c.fetchall()
        print(infoID)
        if(len(infoID) == 0):
            IDRej = 0
        else:
            IDRej = infoID[len(infoID) - 1][0]
        sql = "insert into RejectedProposals (ID, ResearcherID, Title, ProjectDescription,FundingAmount) values (%s, %s, %s,%s,%s)"
        val = (IDRej + 1,ResearchID, Title, ProjectDescription,FundAmount)
        c.execute(sql,val)
    else:
        c.execute(' SELECT ID FROM IdleProposals ')
        infoID = c.fetchall()
        if(len(infoID) == 0):
            IDIdle = 0
        else:
            IDIdle = infoID[len(infoID) - 1][0]
        sql = "insert into IdleProposals (ID, ResearcherID, Title, ProjectDescription,FundingAmount) values (%s, %s, %s,%s,%s)"
        val = (IDIdle + 1,ResearchID, Title, ProjectDescription,FundAmount)
        c.execute(sql,val)
    print("inserted")
    conn.commit()
    conn.close()


def WithdrawFunds(ResearcherID, HolderID, WithdrawAmount,Reason):
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    sql = 'SELECT Budget,EndDate FROM ResearchAccount WHERE HolderID= %s AND ResearcherID= %s' 
    vals = (HolderID,ResearcherID)
    c.execute(sql, vals)
    information = c.fetchall()
    WithdrawNew = int(information[0][0]) - int(WithdrawAmount)
    EndDate = information[0][1]
    today = date.today()
    date_format = '%Y-%m-%d'
    date_obj = datetime.strptime(EndDate, date_format).date()
    if(WithdrawNew >= 0 and today <= date_obj):
        currentTimeDate = date.today()
        c.execute(' SELECT ID FROM Transactions ')
        infoID = c.fetchall()
        if(len(infoID) == 0):
            ID = 0
        else:
            ID = infoID[len(infoID) - 1][0]
        sql = 'UPDATE ResearchAccount SET Budget = %s WHERE HolderID = %s AND ResearcherID = %s'
        val = (WithdrawNew, HolderID,ResearcherID)
        c.execute(sql, val)
        sql = "insert into Transactions (date, amount, Reason, FundingAmount,ID,ResearcherID,AccountID) values (%s, %s, %s,%s,%s,%s,%s)"
        vals = (currentTimeDate,WithdrawAmount,Reason,WithdrawNew,ID + 1 ,ResearcherID,HolderID)
        c.execute(sql, vals)
        conn.commit()
        conn.close()

def Transactions(ResearcherID, HolderID):
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    sql = 'SELECT date,amount,Reason,FundingAmount FROM Transactions WHERE AccountID=%s AND ResearcherID= %s'
    val = (HolderID,ResearcherID)
    c.execute(sql, val)
    information = c.fetchall()
    return information


def ProposalAccepted(ID,Budget,EndDate):
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    c.execute(' SELECT ID FROM AcceptedProposals ')
    infoID = c.fetchall()
    if(len(infoID) == 0):
        IDtmp = 0
    else:
        IDtmp = infoID[len(infoID) - 1][0]
    sql = 'SELECT Title,ResearcherID,ProjectDescription,FundingAmount FROM IdleProposals WHERE ID= %s'
    val = (ID)
    c.execute(sql, val)
    information = c.fetchall()
    print(information)
    sql = ' SELECT count(*) FROM ResearchAccount WHERE ResearcherID=%s'
    val = (str(information[0][1]))
    c.execute(sql, val)
    HolderID = c.fetchone()[0]
    sql = "insert into AcceptedProposals (ID,Title, ResearcherID, ProjectDescription,FundingAmount) values (%s, %s, %s,%s,%s)"
    val = (IDtmp + 1, information[0][0], information[0][1], information[0][2],information[0][3])
    c.execute(sql, val)
    c.execute(' SELECT ID FROM ResearchAccount ')
    infoID = c.fetchall()
    if(len(infoID) == 0):
        AccountIDtmp = 0
    else:
        AccountIDtmp = infoID[len(infoID) - 1][0]
    sql = "insert into ResearchAccount (ID, HolderID, Title, ResearcherID, Budget, EndDate) values (%s, %s, %s , %s, %s,%s)"
    val = (AccountIDtmp + 1,HolderID + 1, information[0][0], information[0][1], Budget,EndDate)
    c.execute(sql, val)
    sql = "DELETE FROM IdleProposals WHERE ID = %s"
    val = (ID)
    c.execute(sql, val)
    c.execute(' SELECT ID FROM UniversityNotifications ')
    infoID = c.fetchall()
    if(len(infoID) == 0):
        IDtmp3 = 0
    else:
        IDtmp3 = infoID[len(infoID) - 1][0]
    print(getResearcher(information[0][1]))
    ResearcherName = getResearcher(information[0][1])[0][0]
    sql = "insert into UniversityNotifications (ID,AccountID,date,Budget,Researcher) values(%s,%s,%s,%s,%s)"
    val = (IDtmp3 + 1,AccountIDtmp + 1,EndDate,Budget,ResearcherName)
    c.execute(sql, val)
    conn.commit()
    conn.close()


def ProposalRejected(ID):
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    c.execute(' SELECT ID FROM RejectedProposals ')
    infoID = c.fetchall()
    if(len(infoID) == 0):
        IDtmp = 0
    else:
        IDtmp = infoID[len(infoID) - 1][0]
    sql = 'SELECT Title,ResearcherID,ProjectDescription,FundingAmount FROM IdleProposals WHERE ID=%s'
    val = (ID)
    c.execute(sql, val)
    information = c.fetchall()
    sql = "insert into RejectedProposals (ID, Title, ResearcherID,  ProjectDescription,FundingAmount) values (%s, %s, %s,%s,%s)"
    val = (IDtmp + 1, information[0][0],information[0][1], information[0][2],information[0][3])
    c.execute(sql, val)
    sql = "DELETE FROM IdleProposals WHERE ID = %s"
    val = (ID)
    c.execute(sql, val)
    conn.commit()
    conn.close()  
def getProposals(TableToGet):
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    sql = 'SELECT Title,ID FROM ' + TableToGet
    c.execute(sql)
    titles = c.fetchall()
    conn.close()
    return titles


def getProposalsResearchers(TableToGet,ResearcherID):
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    c.execute('SELECT * FROM ' + TableToGet)
    tlkf = c.fetchall()
    print(tlkf)
    sql = 'SELECT Title FROM ' + TableToGet + ' WHERE ResearcherID= %s'
    val = (int(ResearcherID))
    c.execute(sql, val)
    titles = c.fetchall()
    print('fs')
    print(titles)
    return titles

def researchAccountInformation(ResearcherID,HolderID):
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    print(ResearcherID)
    sql = 'SELECT Title,Budget,EndDate,HolderID,ResearcherID FROM ResearchAccount WHERE HolderID= %s AND ResearcherID= %s'
    val = (HolderID,ResearcherID)
    c.execute(sql, val)
    information = c.fetchall()
    print(information)
    return information

def getProposalInformation(TableToGet,ID):
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    sql = 'SELECT Title,ProjectDescription,FundingAmount,ResearcherID FROM ' + TableToGet + ' WHERE ID=%s'
    val = (ID)
    c.execute(sql, val)
    information = c.fetchall()
    conn.close()
    return information

def getResearcher(ID):
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    sql = 'SELECT FullName FROM ResearcherAccounts WHERE ID=%s '
    c.execute('SELECT * FROM ResearcherAccounts')
    print(c.fetchall())
    val = (ID)
    c.execute(sql, val)
    information = c.fetchall()
    return information