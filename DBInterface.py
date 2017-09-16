"""This module is interface to mysql."""
import MySQLdb


SETTINGS = {}

SETTINGS['MYSQL_HOST'] = 'localhost'
SETTINGS['MYSQL_DBNAME'] = 'MedicalUserInfo'
SETTINGS['MYSQL_USER'] = 'SCUT'
SETTINGS['MYSQL_PASSWD'] = 'SCUT1234'
PATIENT = 0


class DB:
  conn = None

  def __init__(self):
    self.connect()

  def connect(self):
    self.conn = MySQLdb.connect(host=SETTINGS['MYSQL_HOST'],
        port=3306,
        user=SETTINGS['MYSQL_USER'],
        passwd=SETTINGS['MYSQL_PASSWD'],
        db=SETTINGS['MYSQL_DBNAME'],
        charset='utf8')

  def queryUserRfid(self, room_no,berth_no):
    try:
      cursor = self.conn.cursor()
      cursor.execute("select rfid from user where id = (SELECT id FROM roomUserInfo WHERE room_no = ? and berth_no = ?)",(room_no,berth_no))
    except (AttributeError, MySQLdb.OperationalError):
      self.connect()
      cursor = self.conn.cursor()
      cursor.execute("select rfid from user where id = (SELECT id FROM roomUserInfo WHERE room_no = ? and berth_no = ?)",(room_no,berth_no))
    return cursor
  
  def queryUserName(self, user_id):
    try:
      cursor = self.conn.cursor()
      cursor.execute("select userName,type from user where id = %s",(user_id,))
    except (AttributeError, MySQLdb.OperationalError):
      self.connect()
      cursor = self.conn.cursor()
      cursor.execute("select userName,type from user where id = %s",(user_id,))
    return cursor

  def queryPatient(self):
    try:
      cursor = self.conn.cursor()
      cursor.execute("select userName from user where type = %s",(PATIENT,))
    except (AttributeError, MySQLdb.OperationalError):
      self.connect()
      cursor = self.conn.cursor()
      cursor.execute("select userName from user where type = %s",(PATIENT,))
    return cursor

  def queryRoomRfid(self, room_no):
    try:
      cursor = self.conn.cursor()
      cursor.execute("select rfid from roomInfo where room_no = %s",(room_no,))
    except (AttributeError, MySQLdb.OperationalError):
      self.connect()
      cursor = self.conn.cursor()
      cursor.execute("select rfid from roomInfo where room_no = %s",(room_no,))
    return cursor

