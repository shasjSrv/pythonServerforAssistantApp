"""This module is interface to mysql."""
import sys
import json
from DBInterface import DB
import dealRobotAccess
import dealWebAccess

from flask import Flask, jsonify, redirect, url_for, Response
from flask import request
from flask import make_response
from flask import abort


from flask_login import LoginManager , login_required , UserMixin , login_user
# from PIL import Image, ImageFile

APP = Flask(__name__)
MYDB = DB()



@APP.route('/QueryPatientInfo', methods=['POST','GET'])
def query_patient_info():
    # if not request.json:
    #     abort(400)   
    respose = dealWebAccess.respose_query_user_info()
    resp = Response(json.dumps(respose))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp

@APP.route('/QueryUserMedicine', methods=['POST'])
def query_user_medicine():
    """
    This function is about Query user medicine.
    """
    if not request.json or not 'user_id' in request.json:
        abort(400)
    
    respose = dealWebAccess.respose_query_user_medicine(request.json)
    resp = Response(json.dumps(respose))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp


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

@APP.route('/CheckUpdateCondition', methods=['POST'])
def check_update_condition():
    if not request.json or not 'user_id':
        abort(400)
    respose = dealRobotAccess.respose_query_user_info(request.json)

    return jsonify({'result' : respose}), 201



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