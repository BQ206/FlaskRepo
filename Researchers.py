

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

import threading                                                                
import functools    
import time   

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
def getconn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    return conn
def createTable():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    print("fsa")
    c.execute('''CREATE TABLE IF NOT EXISTS ResearcherAccounts
           (ID INT PRIMARY KEY     NOT NULL,
            FullName           TEXT    NOT NULL,
            Email     TEXT     NOT NULL,
            Password    TEXT       NOT NULL);''')
    conn.commit()          
def dropTables():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    c.execute('DROP TABLE ResearcherAccounts')
    c.execute('DROP TABLE AcceptedProposals')
    c.execute('DROP TABLE RejectedProposals')
    c.execute('DROP TABLE IdleProposals')
    c.execute('DROP TABLE ResearchAccount')
    c.execute('DROP TABLE AddResearchers')
    c.execute('DROP TABLE Transactions')
    c.execute('DROP TABLE UniversityNotifications')
@synchronized
def CreateAccount(Name, Email, Password):
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    c.execute(' SELECT ID FROM ResearcherAccounts ')
    infoID = c.fetchall()
    if(len(infoID) > 0):
        IDtmp = infoID[len(infoID) - 1][0]
    else:
        IDtmp = 0
    sql = "INSERT INTO ResearcherAccounts (ID, FullName, Email,Password) VALUES (%s, %s,%s,%s)"
    val = (IDtmp + 1, Name, Email,Password)
    c.execute(sql, val)
    conn.commit()

def LoginAccount(NameEmail,Password):
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    c.execute('SELECT FullName,Email,Password,ID FROM ResearcherAccounts')
    information = c.fetchall()
    print(information)
    i = 0
    while(i < len(information)):
        if((information[i][0] == NameEmail or information[i][1] == NameEmail) and information[i][2] == Password):
            print("SUCCESS")
            ytupl = (True,information[i][3])
            return ytupl
        i += 1
    return (False,0)


def ListResearchers():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    c.execute('SELECT FullName,ID FROM ResearcherAccounts')
    information = c.fetchall()
    return information

def ListResearchersRemove(AccountHolderID):
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    sql = 'SELECT ResearcherName,ResearcherAddedID FROM AddResearchers WHERE ResearchAccountID = %s'
    val = (AccountHolderID)
    c.execute(sql, val)
    information = c.fetchall()
    return information

def RemoveResearchers(ResearcherAddedID,HolderAccountID):
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    sql = "DELETE FROM AddResearchers WHERE ResearcherAddedID = %s AND ResearchAccountID = %s"
    val = (ResearcherAddedID,HolderAccountID)
    c.execute(sql, val)
    conn.commit()
    c.close()

def SearchResearchers(SearchString):
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    SearchString = SearchString.upper()
    sql = 'SELECT FullName,ID FROM ResearcherAccounts WHERE UPPER(FullName) LIKE "% %s %"'
    val = (SearchString)
    c.execute(sql, val)
    information = c.fetchall()
    return information

def AddResearcher(ID,Name,ResearcherAddedID,AccountID,ResearcherID):
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
        IDtmp = 0
    else:
        IDtmp = infoID[len(infoID) - 1][0]
    sql = ' SELECT count(*) FROM AddResearchers WHERE ResearcherAddedID = %s AND  ResearchAccountID = %s '
    val = (ResearcherAddedID,AccountID)
    c.execute(sql, val)
    researcherAlready = c.fetchall()
    if(researcherAlready[0][0] == 0):
        sql = "insert into AddResearchers (ID, ResearcherID,  ResearcherAddedID,ResearchAccountID, ResearcherName, OriginialResearchID) values (%s, %s, %s,%s,%s,%s  )"
        val = (IDtmp + 1,ResearcherID, ResearcherAddedID, AccountID,Name,ID)
        c.execute(sql, val)
        conn.commit()
        c.close()

def getAddedAcounts(ResearcherID):
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    sql = "SELECT ResearchAccountID,ResearcherID FROM AddResearchers WHERE ResearcherAddedID = %s"
    val = (ResearcherID)
    c.execute(sql, val)
    information = c.fetchall()
    print('fs')
    print(information)
    return information

def getResearchAccountTitles(AccountID):
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    c = conn.cursor()
    sql = "SELECT Title FROM ResearchAccount WHERE ID = %s"
    val = (str(AccountID))
    c.execute(sql, val)
    information = c.fetchall()
    return information
