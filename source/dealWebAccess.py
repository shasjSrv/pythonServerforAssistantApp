from DBInterface import DB
from modelDatabase import *
import datetime


def respose_query_user_info():
    """
    This function is about querying whole info of a user.
    """
    response = {
        'userID': [],
        'userName': [],
        'age': [],
        'gender': [],
        'rfid': [],
        'roomNo': [],
        'berthNo': []
    }
    query_patient_info_db = DB()
    ret = query_patient_info_db.query_patient_info()

    if ret is None:
        return response

    for i in range(0, len(ret)):
        # 7 columns: 0 userID,1 userName,2 age
        #           3 gender, 4 rfid, 5 roomNo, 6 berthNo
        response['userID'].append(ret[i][0])
        response['userName'].append(ret[i][1])
        response['age'].append(ret[i][2])
        response['gender'].append(ret[i][3])
        response['rfid'].append(ret[i][4])
        response['roomNo'].append(ret[i][5])
        response['berthNo'].append(ret[i][6])

    return response


def respose_query_user_medicine(request_json):
    """
    This function is about querying medicine info of a user.
    """
    response = {
        'isSuccess': 0,
        'medicineName': [],
        'medicineCount': [],
        'medicineDosage': [],
        'medicineID': [],
        'isSent': [],
        'dateTime': []
    }
    user_id = request_json['user_id']
    query_medecine_info_db = DB()
    ret_medicine = query_medecine_info_db.query_user_medicine_info(user_id)

    if ret_medicine is None:
        return response
    response['isSuccess'] = 1

    for j in range(0, len(ret_medicine)):
        # 7 columns: 0 userID,1 medicineName,2 medicineDosage
        #           3 uNit, 4 number, 5 isSend, 6 medicineID,8 dateTime
        is_send = ret_medicine[j][5]
        measure = str(ret_medicine[j][4]) + ret_medicine[j][3]
        response['medicineName'].append(ret_medicine[j][1])
        response['medicineCount'].append(measure)
        response['medicineDosage'].append(ret_medicine[j][2])
        response['medicineID'].append(ret_medicine[j][6])
        response['isSent'].append(is_send)
        response['dateTime'].append(ret_medicine[j][7].strftime('%m/%d/%Y'))

    return response


def respose_query_medicine():
    """
    This function is about querying whole medicine info
    """
    response = {
        "MedicineInfo": []
    }
    for medicine in MedicineInfo.select():
        medicine_info = {}
        medicine_info['medicineID'] = medicine.medicineID
        medicine_info['medicineName'] = medicine.medicineName
        medicine_info['medicineDosage'] = medicine.medicineDosage
        medicine_info['unit'] = medicine.unit
        response['MedicineInfo'].append(medicine_info)
    return response


def insert_medicine_to_user(request_json):
    response = {
        'isSuccess': "false"
    }
    user_id = request_json['user_id']
    medicine_id = request_json['medicine_id']
    number = request_json['number']
    insert = MedicalUserInfo.insert(userID=user_id,
                                    medicineID=medicine_id,
                                    number=number,
                                    dateTime=datetime.datetime.now().strftime("%Y-%m-%d"),
                                    is_send=NOTSEND).execute()
    response['isSuccess'] = 'true'
    return response


def delete_medicine_to_user(request_json):
    response = {
        'isSuccess': "false"
    }
    user_id = request_json['user_id']
    medicine_id_array = request_json['medicine_id']
    number_array = request_json['number']
    # medicine_id = request_json['medicine_id']
    # number = request_json['number']
    for i, medicine_id in enumerate(medicine_id_array):
        delete = MedicalUserInfo.delete().where(MedicalUserInfo.userID == user_id,
                                                MedicalUserInfo.medicineID == medicine_id,
                                                MedicalUserInfo.number == number_array[i]).execute()
    response['isSuccess'] = 'true'
    return response
