from DBInterface import DB

def respose_query_user_info():
    """
    This function is about querying whole info of a user.
    """
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



def respose_query_user_medicine(request_json):
    """
    This function is about querying medicine info of a user.
    """
    respose = {
        'isSuccess' : 0,
        'medicineName':[],
        'medicineCount':[],
        'medicineDosage':[],
        'medicineID': []
    }
    user_id = request_json['user_id']
    query_medecine_info_db = DB()
    ret_medicine = query_medecine_info_db.query_user_medicine_info(user_id)

    if ret_medicine is None:
        return respose

    for j in range(0, len(ret_medicine)):
        #7 columns: 0 userID,1 medicineName,2 medicineDosage
        #           3 uNit, 4 number, 5 isSend, 6 medicineID
        is_send = ret_medicine[j][5]
        measure = str(ret_medicine[j][4]) + ret_medicine[j][3]
        respose['medicineName'].append(ret_medicine[j][1])
        respose['medicineCount'].append(measure)
        respose['medicineDosage'].append(ret_medicine[j][2])
        respose['medicineID'].append(ret_medicine[j][6])

    return respose
