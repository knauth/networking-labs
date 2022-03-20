#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 22:24:34 2022

@author: june
"""

from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
        QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QFileDialog, QFormLayout, QBoxLayout,
        QMessageBox, QTableWidgetItem, QAbstractItemView, QWidgetItem)
import os
import socket as sk
import sys

class ChatGui(QDialog):
    def __init__(self, title, con, parent=None):
        super(ChatGui, self).__init__(parent)
        self.setWindowTitle(title)
        
        self.con = con
        
        self.mainLayout = QVBoxLayout()
        
        self.cliServLabel = QLabel(con.cliOrServ)
        self.mainLayout.addWidget(self.cliServLabel)
        
        self.infoLabel = QLabel("Recieve blocks until you get a message, "+ 
                                "but you can send as much as you'd like")
        self.infoLabel.setWordWrap(True)
        self.mainLayout.addWidget(self.infoLabel)
        
        self.recvText = QLabel("Nothing received yet...")
        self.recvText.setWordWrap(True)
        self.mainLayout.addWidget(self.recvText)
        
        self.sendBox = QLineEdit()
        self.sendBox.setText("Type your message here.")
        self.mainLayout.addWidget(self.sendBox)
        
        sendButton = QPushButton("Send")
        sendButton.clicked.connect(self.send)
        self.mainLayout.addWidget(sendButton)
        
        recvButton = QPushButton("receive")
        recvButton.clicked.connect(self.receive)
        self.mainLayout.addWidget(recvButton)
        
        self.setLayout(self.mainLayout)
        
    def send(self):
        self.con.send(self.sendBox.text())
    
    def receive(self):
        self.recvText.setText('Received: "{}"'.format(self.con.receive()))
    
class ConnectionHandler():
    def __init__(self, cliOrServ='server'):
        self.sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self.server_address = (sk.gethostbyname(sk.gethostname()), 10000)
        self.cliOrServ = cliOrServ
            
        if cliOrServ == 'client':
            self.setupClient()
        elif cliOrServ == 'server':
            self.setupServer()
        
        else:
            print("Bad args!")
            self.sock.close()
            raise AssertionError
            
    def setupClient(self):
        print("*** Client is connecting to {} at port {}".format(
            self.server_address[0], 
            self.server_address[1]))
        self.sock.connect(self.server_address)
        print("Connected")
        
    def setupServer(self):
        print('*** Server is starting up on {} port {}***'.format(
            self.server_address[0], 
            self.server_address[1]))
        self.sock.bind(self.server_address)
        self.sock.listen(1)
        
        print('*** Waiting for a connection ***')
        self.connection, self.client_address = self.sock.accept()
        print("Connected")
        
    def send(self, text):
        if self.cliOrServ == 'client':
            self.sock.sendall(text.encode())
        else:
            self.connection.sendall(text.encode())
        
    def receive(self):
        # output= ""
        # while True:
        #     # decode() function returns string object
        #     data = self.sock.recv(1024).decode()
        #     if data:
        #         print('received "%s"' % data)
        #         output += data
        if self.cliOrServ == 'client':
            return self.sock.recv(1024).decode()
        
        return self.connection.recv(1024).decode()

if __name__ == '__main__':
    con = ConnectionHandler(sys.argv[1])
    
    app = QApplication([])
    app.setStyle('Fusion')
    app.setPalette(app.style().standardPalette())
    
    form = ChatGui(con.cliOrServ, con)
    form.show()
    app.exec_()