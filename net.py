import socket
import json
from threading import *
BUF_SIZE = 30

def connect(sock, ip, port): #self explanatory
  try:
    sock.connect((ip, port))
    print("Connected to ", ip, "|", port)
  except OSError as e:
    print("Error connecting to ", ip ,"|" , port)
    print("OS error: {0}".format(e))

def send(s,t, d): #socket, type, data eg: net.send(soc, "msg", "hello world!")
  try:
    datatable = json.dumps([t, d])
    etable = datatable.encode()
    elen = str(len(etable)) + ";"
    s.send(elen.encode()) #send length of packet
    s.send(etable) #send packet
    #print("Sent data, type: ", t, " | Length: ", elen, " | Data: ", datatable, "| ", etable)
  except OSError as e:
    print("Error sending data to ", ip ,"|" , port)
    print("OS error: {0}".format(e))

def receive(s): #returns a list like [type, content] eg: ["msg", "hello world!"]
  fd = s.recv(BUF_SIZE).decode() #Decode inital packet
  fdd = fd.split(";",1) #Read length
  if not int(fdd[0]):
    print("ERROR NO LENGTH OF PACKET")
    return
  L = int(fdd[0])
  datatable = fdd[1]
  try:
    attempts = 0
    while (not len(datatable) == L ) and attempts <= (10 + L): #peice together packet
      datatable = datatable + s.recv(BUF_SIZE).decode()
      #print(datatable)
      attempts = attempts + 1
    try:
      datatable = json.loads(datatable)
    except OSError:
      print("Error decoding data :(")
    #print(datatable)
    return datatable
  except OSError:
    print("failed to retrieve and decode data.")
    return []
