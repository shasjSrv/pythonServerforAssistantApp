from DBInterface import DB


def respose_query_id_info(request_json):
    """
    return the respose of user's id info to robot
    """
    respose = {
        'isSuccess' : 0,
        'userName' : "",
        'type' : -1,
        'patientNameArray': [],
        'patientIDArray':[],
        'patientRfIDArray':[],
        'medicineNameArray':[],
        'medicineCountArray':[],
        'medicineDosageArray':[],
        'medicineIDArray':[]
    }

    user_id = request_json['user_id']
    query_user_name_db = DB()
    ret = query_user_name_db.query_user_name(user_id)
    if ret is None:
        return respose

    user_name = ret[0]
    user_type = ret[1]

    respose['isSuccess'] = 1
    respose['userName'] = user_name
    respose['type'] = user_type
    query_patient_db = DB()
    ret = query_patient_db.query_patient()
    #3 columns: 0   patientName, 1  patientID, 2    patientRfID

    if ret is None:
        return respose
    

    for i in range(0, len(ret)):
        # medicine_send_info_list = []
        medicine_name_list = []
        medicine_measure_list = []
        medicine_dosage_list = []
        medicine_id_list = []
        # cursor = MYDB.queryUserMedicineInfo(ret[i][1])
        # ret_medicine = cursor.fetchall()
        query_medecine_info_db = DB()
        ret_medicine = query_medecine_info_db.query_user_medicine_info(ret[i][1])
        
        for j in range(0, len(ret_medicine)):
            #8 columns: 0 userID,1 medicineName,2 medicineDosage
            #           3 uNit, 4 number, 5 isSend, 6 medicineID,8 dateTime
            is_send = ret_medicine[j][5]
            #if the medicine is sent,jump to next one
            if is_send == 1:    
                continue
            measure = str(ret_medicine[j][4]) + ret_medicine[j][3]
            medicine_name_list.append(ret_medicine[j][1])
            medicine_measure_list.append(measure)
            medicine_dosage_list.append(ret_medicine[j][2])
            medicine_id_list.append(ret_medicine[j][6])

        print len(medicine_name_list)
        if len(medicine_name_list) != 0:
            respose['patientNameArray'].append(ret[i][0])
            respose['patientIDArray'].append(ret[i][1])
            respose['patientRfIDArray'].append(ret[i][2])
            respose['medicineNameArray'].append(medicine_name_list)
            respose['medicineCountArray'].append(medicine_measure_list)
            respose['medicineDosageArray'].append(medicine_dosage_list)
            respose['medicineIDArray'].append(medicine_id_list)

    return respose


def respose_update_medicine_state(request_json):
    """
    return the state of update medicine state to robot
    """
    respose = {
        'updateSuccess' : 0
    }

    user_id = request_json['user_id']
    medicine_id_arraylist = list(request_json['medicine_id_arraylist'])
    date_yyyy = request_json['date_yyyy']
    date_mm = request_json['date_mm']
    date_dd = request_json['date_dd']

    respose['updateSuccess'] = 1
    for i in range(0, len(medicine_id_arraylist)):
        update_medicine_db = DB()
        update_success = update_medicine_db.update_medicine_info(user_id, medicine_id_arraylist[i] \
        , date_yyyy, date_mm, date_dd)
        if update_success is False:
            respose['updateSuccess'] = 0
    return respose


def respose_query_user_info(request_json):
    """
    return the whole user info which want to query
    """
    respose = {
        'isSuccess': 0,
        'userID' : -1,
        'userName' : "",
        'age': -1,
        'gender': "",
        'rfid': "",
        'roomNo': -1,
        'berthNo': -1
    }
    user_id = request_json['user_id']
    query_patient_info_db = DB()
    ret = query_patient_info_db.query_patient_info_by_userid(user_id)
    
    if ret is None:
        return respose

    respose['isSuccess'] = 1
    #7 columns: 0 userID,1 userName,2 age
    #           3 gender, 4 rfid, 5 roomNo, 6 berthNo
    respose['userID'] = ret[0[0]]
    respose['userName'] = ret[0][1]
    respose['age'] = ret[0][2]
    respose['gender'] = ret[0][3]
    respose['rfid'] = ret[0][4]
    respose['roomNo'] = ret[0][5]
    respose['berthNo'] = ret[0][6]

    return respose