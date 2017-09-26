"""This module is interface to mysql."""
import sys
import json
import hashlib
from DBInterface import DB
import dealRobotAccess
import dealWebAccess
from userRepository import UsersRepository, User

from flask import Flask, jsonify, redirect, url_for, Response
from flask import request
from flask import make_response
from flask import abort


# from passlib.apps import custom_app_context as pwd_context
from flask_login import LoginManager, login_required, UserMixin, login_user
# from PIL import Image, ImageFile

APP = Flask(__name__)
APP.config['SECRET_KEY'] = 'secret_key'
LOGIN_MANAGER = LoginManager()
LOGIN_MANAGER.init_app(APP)
MYDB = DB()
USERS_RESPOITORY = UsersRepository()



# @APP.route("/settings")
# @login_required
# def settings():
#     pass


@APP.route('/login' , methods=['GET' , 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        registeredUser = USERS_RESPOITORY.get_user(username)
        print('Users '+ str(USERS_RESPOITORY.users))
        print('Register user %s , password %s' % (registeredUser.username, registeredUser.password_hash))
        # print('hash passwd %s' % pwd_context.encrypt(password))
        md5 = hashlib.md5()
        md5.update(password)
        password = md5.hexdigest()
        # print password
        if registeredUser != None and registeredUser.password_hash == password:
            print('Logged in..')
            login_user(registeredUser)
            return redirect(url_for('query_patient_info'))
        else:
            return abort(401)
    else:
        return Response('''
            <form action="" method="post">
                <p><input type=text name=username>
                <p><input type=password name=password>
                <p><input type=submit value=Login>
            </form>
        ''')

@APP.route('/register' , methods = ['GET' , 'POST'])
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

@APP.route('/QueryPatientInfo', methods=['POST','GET'])
@login_required
def query_patient_info():
    # if not request.json:
    #     abort(400)   
    respose = dealWebAccess.respose_query_user_info()
    resp = Response(json.dumps(respose))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp

@APP.route('/QueryUserMedicine', methods=['POST'])
@login_required
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


@LOGIN_MANAGER.user_loader
def load_user(userid):
    print userid
    print USERS_RESPOITORY.get_user_by_id(userid)
    return USERS_RESPOITORY.get_user_by_id(userid)


if __name__ == '__main__':
    reload(sys) 
    sys.setdefaultencoding('utf-8')
    APP.run(host='0.0.0.0',port = 5000)