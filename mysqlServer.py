"""This module is interface to mysql."""
import sys
from DBInterface import DB


from flask import Flask, jsonify
from flask import request
from flask import make_response
from flask import abort
# from PIL import Image, ImageFile

APP = Flask(__name__)
MYDB = DB()


@APP.route('/QueryIDInfo', methods=['POST'])
def create_task():
    """
    This function is about Query room RFID and user RFID.
    """
    if not request.json or not 'room_no' or not 'berth_no' in request.json:
        abort(400)
        respose = {
            'isSuccess' : 0,
            'userRfid' : -1,
            'roomRfid' : -1
        }

        room_no = request.json['room_no']
        berth_no = request.json['berth_no']
        # cursor = MYDB.queryUserRfid(room_no,berth_no)
        # ret = cursor.fetchone()
        # ret = MYDB.queryUserRfid(room_no,berth_no)
        query_user_rfid_db = DB()
        ret = query_user_rfid_db.queryUserRfid(room_no,berth_no)

        if ret is None:
            return jsonify({'result' : respose}),202
        
        user_rfid = ret[0]
        # cursor = MYDB.queryRoomRfid(room_no)
        # ret = cursor.fetchone()
        query_room_rfid_db = DB()
        ret = query_room_rfid_db.queryRoomRfid(room_no)
       

        if ret is None:
            return jsonify({'result' : respose}),202

        room_rfid = ret[0]
        respose['isSuccess'] = 1
        respose['userRfid'] = user_rfid
        respose['roomRfid'] = room_rfid


        return jsonify({'result' : respose}),201


@APP.route('/QueryID', methods=['POST'])
def query_id_info():
    """
    This function is about Query user describ and user type.
    """
    if not request.json or not 'user_id' in request.json:
        abort(400)
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

    user_id = request.json['user_id']
    query_user_name_db = DB()
    ret = query_user_name_db.queryUserName(user_id)
    if ret is None:
        return jsonify({'result' : respose}),202

    user_name = ret[0]
    user_type = ret[1]

    respose['isSuccess'] = 1
    respose['userName'] = user_name
    respose['type'] = user_type
    query_patient_db = DB()
    ret = query_patient_db.queryPatient()
    #3 columns: 0   patientName, 1  patientID, 2    patientRfID

    if ret is None:
        return jsonify({'result' : respose}), 202
    

    for i in range(0, len(ret)):
        # medicine_send_info_list = []
        medicine_name_list = []
        medicine_measure_list = []
        medicine_dosage_list = []
        medicine_id_list = []
        # cursor = MYDB.queryUserMedicineInfo(ret[i][1])
        # ret_medicine = cursor.fetchall()
        query_medecine_info_db = DB()
        ret_medicine = query_medecine_info_db.queryUserMedicineInfo(ret[i][1])
        
        for j in range(0, len(ret_medicine)):
            #7 columns: 0 userID,1 medicineName,2 medicineDosage
            #           3 uNit, 4 number, 5 isSend, 6 medicineID
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
    return jsonify({'result' : respose}), 201


@APP.route('/UpdateUIDMID', methods=['POST'])
def update_medicine_id_info():
    """
    This function is about Query user describ and user type.
    """
    if not request.json or not 'user_id' \
    or not 'medicine_id_arraylist' \
    or not 'date_yyyy'\
    or not 'date_mm'\
    or not 'date_dd' in request.json:
        abort(400)
    respose = {
        'updateSuccess' : 0
    }

    user_id = request.json['user_id']
    medicine_id_arraylist = list(request.json['medicine_id_arraylist'])
    date_yyyy = request.json['date_yyyy']
    date_mm = request.json['date_mm']
    date_dd = request.json['date_dd']

    print user_id
    respose['updateSuccess'] = 1
    print medicine_id_arraylist[0]
    for i in range(0, len(medicine_id_arraylist)):
        update_medicine_db = DB()
        update_success = update_medicine_db.updateMedicineInfo(user_id, medicine_id_arraylist[i] \
        , date_yyyy, date_mm, date_dd)
        if update_success is False:
            respose['updateSuccess'] = 0

    return jsonify({'result' : respose}), 201

# @app.route('/sendIDStatuse', methods=['POST'])
# def create_task():
#     if not request.json or not 'photo' in request.json:
#         abort(400)  
#     task = {
#         'id': tasks[-1]['id'] + 1,
#         'title': request.json['photo'],
#         'description': request.json.get('description', ""),
#         'done': False
#     }
#     #print base64.b64decode(task['title'])
#     #ImageFile.MAXBLOCK = 2**20
#     #print base64.b64decode(strs)  
#     fh = open("imageToSave.jpeg", "wb")
#     fh.write(task['title'].decode('base64'))
#     fh.close()
#     print type(task['title'].decode('base64'))
#     #file = cStringIO.StringIO(request.json.get('description', ""))
#     #img = Image.open(file)
#     #img.show()
#     tasks.append(task)
#     return jsonify({'task': task}), 201


@APP.errorhandler(404)
def not_found(error):
    """
    This function is about error.
    """
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    reload(sys) 
    sys.setdefaultencoding('utf-8')
    APP.run(host='0.0.0.0',port = 5000)