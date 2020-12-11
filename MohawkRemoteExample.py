# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 20:05:19 2020

@author: kterry
"""
import socket
import xml.etree.ElementTree as ET
import threading
import time

"""
  Command Server client example. Sends valid xml commands and returns 
  valid xml responses. 
"""
class CommandServerClient:
    
  def __init__(self):
    self.__readBuffer = ""
    self.__socket = None
    self.__fileSocket = None
    self.__connected = False

  def connect(self):
    """Create a socket and connects it to Mohawk Server.  Ensure the firewall
    allows port  8555  to connect to the localhost"""
    if self.__connected:
      raise Exception('Mohawk already connected')
      
    self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.__socket.connect(("localhost", 8555))
    self.__fileSocket = self.__socket.makefile()
    
    info = self.__fileSocket.readline()
    
    if 'Too many connections' in info:
      raise Exception('Server reach maximum connections')
    
    self.__connected = True

  def disconnect(self):
    """Closes the socket and sets socket objects to None"""
    if not self.__connected:
        raise Exception('Mohawk client not connected')
        
    self.__connected = False
    self.__fileSocket.close()
    self.__socket.close()
    
    self.__fileSocket = None
    self.__socket = None
    
  def sendCommand(self, command):
    if not self.__connected:
      raise Exception('Mohawk client not connected')
      
    self.__socket.sendall(bytes(command+'\n', 'UTF-8'))
    response = self._readSocketResponse()
    #print (response)
    
    return response
    
  def _readSocketResponse(self):
    response = ''
    validXML = False
    line = self.__fileSocket.readline()
    
    while (not validXML) and (line):
      response += line + "\n"
      validXML = self._checkValidXML(response)
      
      if not validXML : 
        line = self.__fileSocket.readline()
    
    return response
  
  def _checkValidXML(self, text):
    try:
      ET.fromstring(text)
      return True
    except:
      return False
    
"""
  Notification Server client example. Prints any server notification
"""
class NotificationServerClient:
    
  def __init__(self):
    self.__readBuffer = ""
    self.__socket = None
    self.__fileSocket = None
    self.__connected = False

  def connect(self):
    """Create a socket and connects it to Mohawk Notification server.  Ensure the firewall
    allows port  8282  to connect to the localhost"""
    if self.__connected:
      raise Exception('Mohawk already connected')
      
    self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.__socket.connect(("localhost", 8282))
    self.__fileSocket = self.__socket.makefile()
    
    info = self.__fileSocket.readline()
    
    if 'Too many connections' in info:
      raise Exception('Server reach maximum connections')
    
    self.__connected = True
    
    # read server notifications continously
    x = threading.Thread(target=self.startReadNotificationsFromServer)
    x.start()

  def disconnect(self):
    """Closes the socket and sets socket objects to None"""
    if not self.__connected:
        raise Exception('Mohawk client not connected')
    
    self.__connected = False
    self.__fileSocket.close()
    self.__socket.close()
    self.__fileSocket = None
    self.__socket = None
    
    
  def startReadNotificationsFromServer(self):
    
    while self.__connected :
      notification = self._readValidXmlNotificationFromSocket()
      
      print('** notification received -> ' + notification)
      time.sleep(1)
      
  def _readValidXmlNotificationFromSocket(self):
    response = ''
    validXML = False
    line = self.__fileSocket.readline()
    
    while (not validXML) and (line):
      response += line + "\n"
      validXML = self._checkValidXML(response)
      
      if not validXML : 
        line = self.__fileSocket.readline()
    
    return response
  
  def _checkValidXML(self, text):
    try:
      ET.fromstring(text)
      return True
    except:
      return False
     

class Pin:
    
    def __init__(self, row: int, column: int, status: bool = None):
       self.row = row
       self.column = column
       self.up = status
       
    def getXmlElement(self):
      return '<pin row="{}" column="{}"/>'.format(self.row, self.column)
    
    def __str__(self):
      status = ''
      if self.up != None :
        status ="UP" if self.up else "DOWN"
        
      return '{}(row={}, col={})'.format(status, self.row, self.column)
    
    def __repr__(self):
      return self.__str__()

def generateForceFirePinsCommand(pins):
  command = '<forcePins>'
  for pin in pins:
    command += pin.getXmlElement();
  
  command+='</forcePins>'
  return command

def processPinStatus(text):
  pins = []
  root = ET.fromstring(text)
  
  for child in root[0]:
    pin = Pin(int(child.attrib['row']), int(child.attrib['column']), True if child.attrib['pinUp']=="true" else False)
    pins.append(pin)
  
  return pins

def main():
  
  print('Create command server client')
  mohawkClient = CommandServerClient()
  mohawkClient.connect()
  
  print('Create mohawk notification client')
  mohawkNotificationClient = NotificationServerClient()
  mohawkNotificationClient.connect()
  
  print('Get version')
  response = mohawkClient.sendCommand('<getVersion/>')
  print(response)
  
  print('Get temperature')
  response = mohawkClient.sendCommand('<temperature/>')
  print(response)
  
  print('Read rack barcode')
  response = mohawkClient.sendCommand('<readRackBarcode/>')
  print(response)
   
  
  print('Force pins')
  #Force to fire pins
  pins = []
  pins.append(Pin(1,1))
  pins.append(Pin(2,2))
  pins.append(Pin(3,3))
  response = mohawkClient.sendCommand(generateForceFirePinsCommand(pins))
  print(response)
  
  
  print('Check pin status')
  response = mohawkClient.sendCommand('<pinStatus/>')
  print(processPinStatus(response))
  
  
  print('Reset pins')
  response = mohawkClient.sendCommand('<resetPins/>')
  print(response)
  
  
  print('Load a worklist')
  # Worklist start
  filepath = 'C:/Temp/DemoWorklist_1.csv'
  loadWorklistCommand = '<loadWorklist path="{}" type="{}"/>'.format(filepath, 'csv')
  response = mohawkClient.sendCommand(loadWorklistCommand)
 
  print('End a worklist')
  response = mohawkClient.sendCommand('<finishWorklist/>')
  print(response)
    
  print('Close connection')
  response = mohawkClient.sendCommand('<close/>')
  print(response)
  
  mohawkClient.disconnect();
  
   # Play with the mohawk, for example with the lid to receive notifications
  print("Open and close lid to see notifications. Process will be killed after 10 seconds")
  time.sleep(10)
  
  mohawkNotificationClient.disconnect()
  

if __name__ == '__main__':
  main()
