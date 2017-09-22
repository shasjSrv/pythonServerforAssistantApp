"""This module is interface to mysql."""
import sys
from DBInterface import DB
import dealRobotAccess

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
        ret = query_user_rfid_db.queryUserRfid(room_no, berth_no)

        if ret is None:
            return jsonify({'result' : respose}), 202
        user_rfid = ret[0]
        # cursor = MYDB.queryRoomRfid(room_no)
        # ret = cursor.fetchone()
        query_room_rfid_db = DB()
        ret = query_room_rfid_db.queryRoomRfid(room_no)

        if ret is None:
            return jsonify({'result' : respose}), 202

        room_rfid = ret[0]
        respose['isSuccess'] = 1
        respose['userRfid'] = user_rfid
        respose['roomRfid'] = room_rfid


        return jsonify({'result' : respose}), 201


@APP.route('/QueryID', methods=['POST'])
def query_id_info():
    """
    This function is about Query user describ and user type.
    """
    if not request.json or not 'user_id' in request.json:
        abort(400)
    respose = dealRobotAccess.respose_query_id_info(request.json)
  
    return jsonify({'result' : respose}), 201


@APP.route('/UpdateUIDMID', methods=['POST'])
def update_medicine_state():
    """
    This function is about Query user describ and user type.
    """
    if not request.json or not 'user_id' \
    or not 'medicine_id_arraylist' \
    or not 'date_yyyy'\
    or not 'date_mm'\
    or not 'date_dd' in request.json:
        abort(400)
    
    respose = dealRobotAccess.respose_update_medicine_state(request.json)

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