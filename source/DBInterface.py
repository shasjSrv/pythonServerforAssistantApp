"""This module implements an interface of mysql DB."""
from datetime import date
import MySQLdb



SETTINGS = {}

SETTINGS['MYSQL_HOST'] = 'localhost'
SETTINGS['MYSQL_DBNAME'] = 'MedicalUserInfo'
SETTINGS['MYSQL_USER'] = 'SCUT'
SETTINGS['MYSQL_PASSWD'] = 'SCUT1234'


PATIENT = 0
NURSE = 1

###########
# the limit days of medicine that would be sent
###########
DURATION = 4


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
        # try:
        cursor = self.conn.cursor()
        cursor.execute("SELECT rfid FROM userInfo WHERE userID = \
        (SELECT userID FROM roomUserInfo WHERE room_no = %s and berth_no = %s)"
                        , (room_no, berth_no))
        onedata = cursor.fetchone()
        cursor.close()
        self.conn.close()
        return onedata
       
    
    def queryUserName(self, user_id):
        # try:
        cursor = self.conn.cursor()
        cursor.execute("select userName,type from userInfo where userID = %s", (user_id,))
        onedata = cursor.fetchone()
        cursor.close()
        self.conn.close()
        return onedata
        

    def queryUserMedicineInfo(self, user_id):
        # try:
        cursor = self.conn.cursor()
        cursor.execute("SELECT mui.userID,mi.medicineName,mi.medicineDosage,mi.unit,\
        mui.number,mui.isSend,mi.medicineID from medicalUserInfo as mui left join medicineInfo as mi on \
        mi.medicineID = mui.medicineID  left join userInfo as u on\
        mui.userID = u.userID where mui.userID = %s", (user_id,))
        alldata = cursor.fetchall()
        cursor.close()
        self.conn.close()
        return alldata
        
    def queryPatient(self):
        # try:
        cursor = self.conn.cursor()
        cursor.execute("select userName,userID,rfid from userInfo where type = %s", (PATIENT,))
        alldata = cursor.fetchall()
        cursor.close()
        self.conn.close()
        return alldata
        #

    def queryRoomRfid(self, room_no):
        # try:
        cursor = self.conn.cursor()
        cursor.execute("select rfid from roomInfo where room_no = %s", (room_no,))
        onedata = cursor.fetchone()
        cursor.close()
        self.conn.close()
        return onedata
        
    def updateMedicineInfo(self, user_id, medicine_id, date_yyyy, date_mm, date_dd):
        # try:
        cursor = self.conn.cursor()
        cursor.execute("update medicalUserInfo set isSend = 1 where \
        userID = %s and medicineID = %s and dateTime BETWEEN %s AND %s "\
        , (user_id, medicine_id, date(int(date_yyyy), int(date_mm), int(date_dd) - DURATION)\
        , date(int(date_yyyy), int(date_mm), int(date_dd))))
        
        self.conn.commit()
        cursor.close()
        self.conn.close()
        return True
