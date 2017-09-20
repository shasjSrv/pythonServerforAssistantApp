"""This module implements an interface of mysql DB."""
import MySQLdb


SETTINGS = {}

SETTINGS['MYSQL_HOST'] = 'localhost'
SETTINGS['MYSQL_DBNAME'] = 'MedicalUserInfo'
SETTINGS['MYSQL_USER'] = 'SCUT'
SETTINGS['MYSQL_PASSWD'] = 'SCUT1234'
PATIENT = 0
NURSE = 1


class DB(object):
    """
    This class is an interface to mysql.
    """
    conn = None

    def __init__(self):
        self.connect()

    def connect(self):
        """
        read the configuration to connect mysql.
        """
        self.conn = MySQLdb.connect(host=SETTINGS['MYSQL_HOST'],
                                    port=3306,
                                    user=SETTINGS['MYSQL_USER'],
                                    passwd=SETTINGS['MYSQL_PASSWD'],
                                    db=SETTINGS['MYSQL_DBNAME'],
                                    charset='utf8')

    def queryUserRfid(self, room_no,berth_no):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT rfid FROM userInfo WHERE userID = \
            (SELECT userID FROM roomUserInfo WHERE room_no = %s and berth_no = %s)"
                           , (room_no, berth_no))
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute("SELECT rfid FROM userInfo WHERE userID = \
            (SELECT userID FROM roomUserInfo WHERE room_no = %s and berth_no = %s)"
                           , (room_no, berth_no))
        return cursor
    
    def queryUserName(self, user_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("select userName,type from userInfo where userID = %s", (user_id,))
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute("select userName,type from userInfo where userID = %s", (user_id,))
        return cursor

    def queryUserMedicineInfo(self, user_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT mui.userID,mi.medicineName,mi.medicineDosage,mi.unit,mui.number,mui.isSend \
            from medicalUserInfo as mui left join medicineInfo as mi on \
            mi.medicineID = mui.medicineID left join  userInfo as u on\
            mui.userID = u.userID where mui.userID = %s", (user_id,))
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute("SELECT mui.userID,mi.medicineName,mi.medicineDosage,mi.unit,mui.number,mui.isSend \
            from medicalUserInfo as mui left join medicineInfo as mi on \
            mi.medicineID = mui.medicineID  left join userInfo as u on\
            mui.userID = u.userID where mui.userID = %s", (user_id,))
        return cursor


    def queryPatient(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("select userName,userID from userInfo where type = %s", (PATIENT,))
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute("select userName,userID from userInfo where type = %s", (PATIENT,))
        return cursor

    def queryRoomRfid(self, room_no):
        try:
            cursor = self.conn.cursor()
            cursor.execute("select rfid from roomInfo where room_no = %s", (room_no,))
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute("select rfid from roomInfo where room_no = %s", (room_no,))
        return cursor

