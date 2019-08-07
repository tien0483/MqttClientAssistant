#coding: utf-8
import sys
from PyQt5.QtWidgets import QApplication,QMainWindow
from mqttclientassistant import MqttClientAssistant


def main():
    app=QApplication(sys.argv)
    win=MqttClientAssistant()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
