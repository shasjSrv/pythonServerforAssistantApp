from modelDatabase import MYSQLDB
from modelDatabase import *
import sys
import datetime


reload(sys)
sys.setdefaultencoding('utf-8')


MYSQLDB.connect()

for medicine in MedicineInfo.select():
    medicine_info = {}
    medicine_info['medicineID'] = medicine.medicineID
    medicine_info['medicineName'] = medicine.medicineName
    medicine_info['medicineDosage'] = medicine.medicineDosage
    medicine_info['unit'] = medicine.unit
    print medicine.medicineName
print "\n"

for medicineUserInfo in MedicalUserInfo.select():
    medicine_info = {}
    medicine_info['userID'] = medicineUserInfo.userID
    medicine_info['medicineID'] = medicineUserInfo.medicineID
    medicine_info['number'] = medicineUserInfo.number
    medicine_info['dateTime'] = medicineUserInfo.dateTime
    medicine_info['is_send'] = medicineUserInfo.is_send
    medicine_info['id'] = medicineUserInfo.id
    print medicine_info

# insert = MedicalUserInfo.insert(userID=10,
#                                 medicineID=0,
#                                 number=1,
#                                 dateTime=datetime.datetime.now().strftime("%Y-%m-%d"),
#                                 is_send=NOTSEND).execute()

UserInfo.delete().where(UserInfo.userID == 6).execute()

MYSQLDB.close()
