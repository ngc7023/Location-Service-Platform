# encoding:utf-8
import serial
import pynmea2
from datetime import datetime
from gsmmodem import modem
from subprocess import PIPE, STDOUT, Popen
ser = serial.Serial("/dev/USB0", 9600)
info = {}
while True:
    line = ser.readline()
    if line.startswith('$GNGGA'):
        rmc = pynmea2.parse(line)
        # Latitude & Latitude Direction
        info['Latitude'] = str(float(rmc.lat)/100)+" "+str(rmc.lat_dir)
        # Longitude & Longitude Direction
        info['Longitude'] = str(float(rmc.lon)/100)+" "+str(rmc.lon_dir)
        # altitude
        info['altitude'] = str(rmc.altitude) + str(rmc.altitude_units).lower()
        # UTCTime
        info['UTCTime'] = rmc.timestamp
        # LocalTime
        info['LocalTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Number of Satellites in use
        info['num_sats'] = rmc.num_sats
        # GPS Quality Indicator/质量指标，1为好
        info['gps_qual'] = rmc.gps_qual
        # Horizontal Dilution of Precision 水平分量精度因子：为纬度和经度等误差平方和的开根号值
        info['horizontal_dil'] = rmc.horizontal_dil
        # Geoidal Separation 大地水准面（与平均海水面重合并延伸到大陆内部的水准面）
        info['geo_sep'] = str(rmc.geo_sep) + str(rmc.geo_sep_units).lower()
        CSQ = commond('echo "AT+CSQ" > /dev/ttyAMA0')
        CREG = int(commond('echo "AT+CREG" > /dev/ttyAMA0'))
        CGATT = commond('echo "AT+CGATT" > /dev/ttyAMA0')
        CSTT = commond('echo "AT+CSTT" > /dev/ttyAMA0')
        CIICR = commond('echo "AT+CIICR" > /dev/ttyAMA0')
        CIPSTART = commond('echo "AT+CIPSTART = 'TCP', '服务器ip', 端口" > /dev/ttyAMA0')
        CIPSEND = commond('echo "AT+CIPSEND" > /dev/ttyAMA0')
        if CSQ == CGATT == CSTT == CIICR == CIPSTART == CIPSEND == 'ok' and (CREG == 1 or CREG == 5):
            commond('echo '+info+' > /dev/ttyAMA0')
    break


def commond(cmd):
    p = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
    return p.stdout.readline()
