from DBInterface import DB

def respose_query_user_info():
    respose = {
        'userID' : [],
        'userName' : [],
        'age': [],
        'gender': [],
        'rfid': [],
        'roomNo': [],
        'berthNo': []
    }
    query_patient_info_db = DB()
    ret = query_patient_info_db.query_patient_info()
    
    if ret is None:
        return respose

    for i in range(0, len(ret)):
        #7 columns: 0 userID,1 userName,2 age
        #           3 gender, 4 rfid, 5 roomNo, 6 berthNo
        respose['userID'].append(ret[i][0]) 
        respose['userName'].append(ret[i][1])
        respose['age'].append(ret[i][2])
        respose['gender'].append(ret[i][3])
        respose['rfid'].append(ret[i][4])
        respose['roomNo'].append(ret[i][5])
        respose['berthNo'].append(ret[i][6])

    return respose
