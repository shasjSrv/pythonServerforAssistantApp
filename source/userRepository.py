from DBInterface import DB
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context


class User(UserMixin):
    def __init__(self , username , password , id , active=True):
        self.id = id
        self.username = username
        self.password_hash = pwd_context.encrypt(password)
        self.active = active

    def get_id(self):
        return self.id

    def is_active(self):
        return self.active

    def get_auth_token(self):
        return make_secure_token(self.username, key='secret_key')

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)




class UsersRepository:

    def __init__(self):
        self.users = dict()
        self.users_id_dict = dict()
        self.identifier = 0
        self.query_registered_user()
        
    
    def query_registered_user(self):
        query_db = DB()
        ret = query_db.query_web_user_name_pwd()
        max_id = -1
        for i in range(0, len(ret)):
            new_user = User(ret[i][1] , ret[i][2] , ret[i][0])
            max_id = max(max_id, ret[i][0])
            self.save_user(new_user)
        self.identifier = max_id

    def insert_registered_user(self, user):
        insert_db = DB()
        ret = insert_db.insert_web_user_login_info(user.id, user.username, user.password_hash)
        if ret is None:
            return
        self.users_id_dict.setdefault(user.id, user)
        self.users.setdefault(user.username, user)


    def save_user(self, user):
        self.users_id_dict.setdefault(user.id, user)
        self.users.setdefault(user.username, user)

    def get_user(self, username):
        return self.users.get(username)

    def get_user_by_id(self, userid):
        return self.users.get(userid)

    def next_index(self):
        self.identifier += 1
        return self.identifier

