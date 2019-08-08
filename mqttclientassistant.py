#coding: utf-8
from PyQt5.QtWidgets import *
from PyQt5 import  uic
from PyQt5 import QtWidgets
import paho.mqtt.client as mqtt
from datetime import datetime
import os
import sys
import ssl
import time
import msgpack
import ast
import json
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib as mpl
import matplotlib.pyplot as plt
import logging
import seaborn as sns

if getattr(sys, 'frozen', False):
    APP_DIR = sys._MEIPASS
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
uifile = os.path.join(APP_DIR, "mqttclientassistant.ui")
ui_mainwindow, qtbaseclass = uic.loadUiType(uifile)


# class MeasureDuration:
#     def __init__(self):
#         self.start = None
#         self.end = None
#
#     def __enter__(self):
#         self.start = time.time()
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.end = time.time()
#         print("Total time taken: %s" % self.duration())
#
#     def duration(self):
#         return str((self.end - self.start) * 1000) + ' milliseconds'


class MqttClientAssistant(ui_mainwindow, qtbaseclass):
    client = None
    is_connected = False
    topics = dict()

    def __init__(self, parent=None):


        if not parent:
            parent = self
        ui_mainwindow.__init__(parent)
        qtbaseclass.__init__(parent)
        self.setupUi(parent)
        self.setWindowTitle("MqttClientAssistant ")
        self.lineEdit_pwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.client = mqtt.Client()
        # self.client.tls_set(ca_certs="C:/Users/Admin/Downloads/ca.crt",cert_reqs=ssl.CERT_REQUIRED,  tls_version=ssl.PROTOCOL_TLSv1_2)
        self.client.on_connect = self.mqtt_on_connected
        self.client.on_message = self.mqtt_on_message
        # self.client.on_subscribe = self.mqtt_on_subcribe
        # self.client.on_publish = self.mqtt_on_publish

        self.pushButton_sub.setEnabled(False)
        self.pushButton_pub.setEnabled(False)
        self.stock=[]
        self.Browser_text=[]
    def slot_connect_pressed(self):

        if self.is_connected:
            return
        if self.lineEdit_server_port.text():
            port = int(self.lineEdit_server_port.text())
        else:
            port = 8883

        # if self.lineEdit_cert.text():
        #     if self.checkBox_protocol.checkState():
        #         self.client.tls_set(ca_certs=self.lineEdit_cert.text(), cert_reqs=ssl.CERT_REQUIRED,tls_version=ssl.PROTOCOL_TLSv1_2)


        if self.lineEdit_user.text() and self.lineEdit_pwd.text():
            self.client.username_pw_set(self.lineEdit_user.text(),
                                        self.lineEdit_pwd.text())
        self.client.connect(self.lineEdit_server_ip.text(), port)
        self.client.loop_start()

    def mqtt_on_connected(self, client, userdata, flags, rc):
        if rc == 0:
            print("Server Connected!")
            self.is_connected = True
            self.pushButton_sub.setEnabled(True)
            self.pushButton_pub.setEnabled(True)
            self.statusbar.showMessage("Kết nối thành công！")
        else:
            self.statusbar.showMessage("Kết nối không thành công！")
            print("Server Connect Failed, with result code " + str(rc))

    def mqtt_on_message(self,client, userdata, msg):

        # if self.client.on_subscribe :
        #     loop_flag=1
        #     counter=1
        # elif self.client.on_publish :
        #     loop_flag=1
        #     counter=0
        # while loop_flag ==1:
        #     time.sleep(0.001)
        #     counter+=1
        #     if  self.client.on_message:
        #         loop_flag =0
        # timeclock=start_time-time.time()
        # print("Time (miliseconds) " + timeclock)
        # MeasureDuration.__enter__(self)



        message=msg.payload.decode("utf-8","ignore")
        message_jdecode=json.loads(message)
        # for x in message_jdecode:
        #     if x==["name2"]:
        #         message_select=message_jdecode.x
        mykeys=["parent_id","client_id"]
        newList = [message_jdecode[k] for k in mykeys if k in message_jdecode]
        for x in newList :
            if x == self.parent_id:
                self.end_time = datetime.now().microsecond
                # print(self.end_time)
                # print(self.start_time)
                self.time_measured = abs((self.end_time - self.start_time) / 1000)
                self.stock.append(self.time_measured)
                text_time = ("Time measured : " + str(self.time_measured) + "ms" + " \n ")
                # self.textBrowser.append(text_time)
                text_address= ("Message from  "+self.parent_id + " to " + self.client_id + "\n" )
            break
        text = '[%s] %r:%s ' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f'), msg.topic,msg.payload)

        print(text)
        self.Browser_text=text_time+text_address+text
        a=[]
        a.append(self.Browser_text)
        self.displayLog=a
        self.textBrowser.append(self.Browser_text)
    def slot_sub_pressed(self):

        if not self.is_connected:
            QMessageBox.critical(self, "Error, try again!")
            return

        if self.topics:
            topics = [(topic, qos) for topic, qos in self.topics.items()]
            topics = []
            text = ""
            topics= [self.lineEdit_topic.text(),int(self.lineEdit_qos.text())]
            for topic, qos in self.topics.items():
                text += "%r" % topic + "," + str(qos) + "\n"
                topics.append((topic, qos))
        if self.lineEdit_topic.text() or self.lineEdit_qos.text():
            self.client.subscribe(topic=self.lineEdit_topic.text(),qos=int(self.lineEdit_qos.text()))
            # self.lineEdit_topic.setToolTip("\n" + text)

    def slot_topic_change(self):
    
        if self.lineEdit_topic.text() and self.lineEdit_qos.text():
            self.topics[self.lineEdit_topic.text()] = int(
                self.lineEdit_qos.text())
            #self.topics[self.lineEdit_topic.text()]=self.lineEdit_topic.text()
    def slot_pub_pressed(self):
        # MeasureDuration.__enter__(self)

        self.start_time=datetime.now().microsecond

        if not self.is_connected:
            QMessageBox.critical(self,"Error, try again!")
            return

        topic=self.lineEdit_topic_2.text()
        msg =self.lineEdit_msg_pub.text()
        qos = self.lineEdit_qos_2.text()

        message_jdecode = json.loads(msg)
        # for x in message_jdecode:
        #     if x==["name2"]:
        #         message_select=message_jdecode.x
        mykeys = ["parent_id", "client_id"]
        newList = [message_jdecode[k] for k in mykeys if k in message_jdecode]
        self.parent_id=newList[0]
        self.client_id=newList[1]
        if topic and msg and qos:
            qos = int(qos)
            self.client.publish(topic, msg, qos)
    def slot_log_file(self):
        logging.basicConfig(filename="Log_Test_File.txt",
                            level=logging.DEBUG,
                            format='%(levelname)s: %(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S')
        logging.debug(self.Browser_text)

    def slot_time_delay(self):
        obj=pd.Series(self.stock)
        thisDict={"Number":[],"TimeDelay":[]}

        thisDict["Number"].extend(range(0,len(self.stock)))
        thisDict["TimeDelay"].extend(self.stock)
        dframe=pd.DataFrame(thisDict,columns=["Number","TimeDelay"])
        g=sns.lmplot("Number","TimeDelay",dframe)
        plt.show()
# {"parent_id":"010203","client_id":"1513456"}