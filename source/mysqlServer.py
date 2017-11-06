"""This module is interface to mysql."""
import sys
import json
import hashlib
from datetime import timedelta
from DBInterface import DB
from modelDatabase import MYSQLDB
import dealRobotAccess
import dealWebAccess
from const import *

from userRepository import UsersRepository, User

from flask import Flask, jsonify, redirect, url_for, Response
from flask import request
from flask import make_response, render_template, send_from_directory
from flask import abort
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_socketio import send, emit, join_room, leave_room

# from passlib.apps import custom_app_context as pwd_context
from flask_login import LoginManager, login_required, UserMixin, login_user
# from PIL import Image, ImageFile

APP = Flask(__name__)
CORS(APP, resources={
     r"*": {"origins": "http://localhost:4200"}}, supports_credentials=True)
APP.config['SECRET_KEY'] = 'secret_key'
LOGIN_MANAGER = LoginManager()
LOGIN_MANAGER.init_app(APP)
LOGIN_MANAGER.login_view = "login"
LOGIN_MANAGER.login_message = unicode("Bonvolu ensaluti por uzi tiun paon.")
LOGIN_MANAGER.login_message_category = "info"
SOCKETIO = SocketIO(APP)

MYDB = DB()
USERS_RESPOITORY = UsersRepository()


@APP.route('/', methods=['get'])
def default():
    return redirect(url_for('login'))


@APP.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        registeredUser = USERS_RESPOITORY.get_user(username)
        # print('Users '+ str(USERS_RESPOITORY.users))
        # print('Register user %s , password %s' % (registeredUser.username, registeredUser.password_hash))
        # print('hash passwd %s' % pwd_context.encrypt(password))
        md5 = hashlib.md5()
        md5.update(password)
        password = md5.hexdigest()
        # print password
        if registeredUser != None and registeredUser.password_hash == password:
            print('Logged in..')
            login_user(registeredUser)
            resp = Response('success!')
            resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4200'
            resp.headers['Access-Control-Allow-Credentials'] = 'true'
            return resp
            # return redirect(url_for('query_patient_info'))
        else:
            resp = Response('false')
            return resp
    else:
        # return Response('''
        #     <form action="" method="post">
        #         <p><input type=text name=username>
        #         <p><input type=password name=password>
        #         <p><input type=submit value=Login>
        #     </form>
        # ''')
        return render_template('index.html')


@APP.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password, USERS_RESPOITORY.next_index())
        new_user.hash_password()
        USERS_RESPOITORY.insert_registered_user(new_user)
        return Response("Registered Successfully")
    else:
        return Response('''
            <form action="" method="post">
            <p><input type=text name=username placeholder="Enter username">
            <p><input type=password name=password placeholder="Enter password">
            <p><input type=submit value=Login>
            </form>
        ''')


@APP.route('/QueryPatientInfo', methods=['POST', 'GET'])
# @login_required
def query_patient_info():
    # if not request.json:
    #     abort(400)
    respose = dealWebAccess.respose_query_user_info()
    resp = Response(json.dumps(respose))
    # resp.headers['Access-Control-Allow-Origin'] = 'https://developer.mozilla.org'
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4200'
    resp.headers['Access-Control-Allow-Methods'] = 'POST'
    resp.headers['Access-Control-Allow-Headers'] = 'Referer,Accept,Origin,User-Agent'
    resp.headers['Content-Type'] = 'application/json'
    return resp


@APP.route('/QueryUserMedicine', methods=['POST'])
# @login_required
def query_user_medicine():
    """
    This function is about Query user medicine.
    """
    print request.json
    if not request.json or not 'user_id' in request.json:
        abort(400)

    respose = dealWebAccess.respose_query_user_medicine(request.json)
    resp = Response(json.dumps(respose))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp


@APP.route('/QueryMedicineInfo', methods=['GET'])
# @login_required
def query_medicine_info():
    """
    This function is about Query whole medicine info in DB.
    """
    respose = dealWebAccess.respose_query_medicine()
    resp = Response(json.dumps(respose, ensure_ascii=False))
    return resp


@APP.route('/QueryUserMedicine/AddUserMedcine', methods=['POST'])
# @login_required
def insert_medicine_to_user():
    """
    This function is about inserting medicine to user by userID.
    """
    print request.json
    if not request.json\
    or not 'user_id'\
    or not 'medicine_id'\
    or not 'number' in request.json:
        abort(400)
    respose = dealWebAccess.insert_medicine_to_user(request.json)
    resp = Response(json.dumps(respose, ensure_ascii=False))
    return resp


@APP.route('/QueryUserMedicine/DeleteUserMedcine', methods=['POST'])
# @login_required
def delete_medicine_to_user():
    """
    This function is about deleting medicine to user by userID.
    """
    print request.json
    if not request.json\
    or not 'user_id'\
    or not 'medicine_id'\
    or not 'number' in request.json:
        abort(400)
    respose = dealWebAccess.delete_medicine_to_user(request.json)
    resp = Response(json.dumps(respose, ensure_ascii=False))
    return resp


@APP.route('/QueryID', methods=['POST'])
def query_id_info():
    """
    This function is about Query user describ and user type.
    """
    if not request.json or not 'user_id' in request.json:
        abort(400)
    respose = dealRobotAccess.respose_query_id_info(request.json)

    return jsonify({'result': respose}), 201


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

    return jsonify({'result': respose}), 201


@APP.route('/CheckUpdateCondition', methods=['POST'])
def check_update_condition():
    """
    This function make sure the user is in DB
    """
    if not request.json or not 'user_id':
        abort(400)
    respose = dealRobotAccess.respose_query_user_info(request.json)

    return jsonify({'result': respose}), 201

@APP.route('/managePatient',methods=['POST'])
def manage_patient():
    if not request.json or not 'options' in request.json:
        abort(400)
    if request.json['options'] == ADDPATIENT :
        respose = dealWebAccess.add_patient_info(request.json)
    elif request.json['options'] == DELETEPATIENT:
        respose = dealWebAccess.delete_patient_info(request.json)
    elif request.json['options'] == QUERYDISEASEINFO:
        respose = dealWebAccess.query_disease_info()
    return jsonify({'result': respose}), 201


@APP.errorhandler(404)
def not_found(error):
    """
    This function is about error.
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


@LOGIN_MANAGER.user_loader
def load_user(userid):
    """
    This callback is used to reload the user object
    from the user ID stored in the session.
    It should take the unicode ID of a user,
    and return the corresponding user object.
    """
    # print userid
    # print USERS_RESPOITORY.get_user_by_id(userid)
    return USERS_RESPOITORY.get_user_by_id(userid)


# @APP.route('/')
# def simulate():
#     return render_template('index.html')

@APP.route('/<path:path>')
def send_static(path):
    if ('.js' in path)\
    or ('.ico' in path)\
    or ('.png' in path) \
    or ('.jpg' in path) \
    or ('.map' in path):
        return send_from_directory('templates', path)


@APP.before_request
def before_request():
    MYSQLDB.connect()


@APP.after_request
def after_request(response):
    MYSQLDB.close()
    return response


@SOCKETIO.on('statsUpdate')
def handle_my_custom_event(json):
    print json
    emit('statsUpdate', json)


@SOCKETIO.on('join')
def on_join(data):
    json_data = json.loads(data)
    if not json_data or not 'room' \
    or not 'client_type' in json_data:
        print data
        abort(400)
    respose = {
        'type': 0,
        'room': -1
    }
    room = json_data['room']
    client_type = json_data['client_type']
    respose['type'] = client_type
    respose['room'] = room
    print "join %s"%room
    response = json.dumps({'body':respose})
    emit('joinRep',response, broadcast=True)

@SOCKETIO.on('leave')
def on_leave(data):
    json_data = json.loads(data)
    if not json_data or not 'room' \
    or not 'client_type' in json_data:
        abort(400)
    respose = {
        'type': 0,
        'room': -1
    }
    room = json_data['room']
    client_type = json_data['client_type']
    respose['type'] = client_type
    respose['room'] = room
    print "leave %s"%room
    response = json.dumps({'body':respose})
    emit('leaveRep',response, broadcast=True)

if __name__ == '__main__':
    reload(sys) 
    sys.setdefaultencoding('utf-8')
    SOCKETIO.run(APP,host='0.0.0.0',port = 5000)

