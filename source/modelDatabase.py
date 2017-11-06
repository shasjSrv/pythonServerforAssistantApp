"""This module implements an interface of mysql DB by using pw."""
import peewee as pw

SENT = 1
NOTSEND = 0


SETTINGS = {}

SETTINGS['MYSQL_HOST'] = 'localhost'
SETTINGS['MYSQL_DBNAME'] = 'MedicalUserInfo'
SETTINGS['MYSQL_USER'] = 'SCUT'
SETTINGS['MYSQL_PASSWD'] = 'SCUT1234'

MYSQLDB = pw.MySQLDatabase(SETTINGS['MYSQL_DBNAME'],
                        host=SETTINGS['MYSQL_HOST'],
                        port=3306,
                        user=SETTINGS['MYSQL_USER'],
                        passwd=SETTINGS['MYSQL_PASSWD'])


class MySQLModel(pw.Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = MYSQLDB


class UserInfo(MySQLModel):
    """userInfo table"""
    userID = pw.IntegerField()
    userName = pw.CharField()
    type = pw.IntegerField()
    rfid = pw.CharField()
    age = pw.IntegerField()
    gender = pw.CharField()
    diseaseType = pw.IntegerField()
    class Meta:
        db_table = 'userInfo'


class DiseaseInfo(MySQLModel):
    """diseaseInfo table"""
    diseaseType = pw.IntegerField(primary_key=True)
    diseaseDec = pw.CharField()
    class Meta:
        db_table = 'diseaseInfo'


class MedicalUserInfo(MySQLModel):
    """medicalUserInfo table"""
    id = pw.IntegerField(primary_key=True)
    userID = pw.IntegerField()
    medicineID = pw.IntegerField()
    number = pw.IntegerField()
    dateTime = pw.DateField()
    is_send = pw.IntegerField(db_column='isSend')
    class Meta:
        db_table = 'medicalUserInfo'


class MedicineInfo(MySQLModel):
    """medicineInfo table"""
    medicineID = pw.IntegerField(primary_key=True)
    medicineName = pw.CharField()
    medicineDosage = pw.CharField()
    unit = pw.CharField()
    class Meta:
        db_table = 'medicineInfo'



class MoomInfo(MySQLModel):
    """roomInfo table"""
    room_no = pw.IntegerField(primary_key=True)
    room_rfid = pw.CharField()
    class Meta:
        db_table = 'roomInfo'


class RoomUserInfo(MySQLModel):
    """roomUserInfo table"""
    userID = pw.IntegerField(primary_key=True)
    roomNo = pw.IntegerField()
    berthNo = pw.IntegerField()
    class Meta:
        db_table = 'roomUserInfo'


class WebUserLoginInfo(MySQLModel):
    """webUserLoginInfo table"""
    userID = pw.IntegerField(primary_key=True)
    userName = pw.CharField()
    passwd = pw.CharField()
    class Meta:
        db_table = 'webUserLoginInfo'



# MYDB.connect()
