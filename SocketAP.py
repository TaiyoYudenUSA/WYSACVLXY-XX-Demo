#This code was tested on Python 2.7.12 on a Windows 7 machine
#pyserial must be installed for script to work

#Tested with TYSA-W version 2.00.00 
#API document: TY_WLAN_WYSACVLXY-XX_AppAPI_V2.00_20160315
#To get a copy of the API document visit http://www.ty-top.com/ and contact your local sales office.

import serial
import sys
from SocketClient import readResponse

def main():
    #Set serial port to N,8,1  @ 115200     
    ser = serial.Serial(sys.argv[1], 115200, timeout=2)

    print "Performing Soft Reset..."
    ser.write("WRST\r\n")
    print readResponse(ser) #Should get ACK back
    print readResponse(ser) #After reset module sends version number. Read version number.

    print "Setting SSID..."
    ser.write("WSTU101MW300AP\r\n")
    print readResponse(ser) #Should get ACK back

    print "Setting IP..."
    ser.write("WSTU105192.168.001.254\r\n")
    print readResponse(ser) #Should get ACK back

    print "Starting uAP...."
    ser.write("WUSA1\r\n")
    print readResponse(ser) #Should get ACK back

    print "Starting DHCP..."
    ser.write("WUDC1\r\n")
    print readResponse(ser) #Should get ACK back

    print "Enabling WPA2 with PSK..."
    ser.write("WSTU1024\r\n")
    print readResponse(ser) #Should get ACK back

    print "Setting passphrase"
    ser.write("WSTU1031234567890\r\n")
    print readResponse(ser) #Should get ACK back

    print "Starting Socket..."
    ser.write("WSOS8080\r\n")
    print readResponse(ser) #SOK1,1,8080,0.0.0.0,0 (i.e. now listening on port 8080)

    print "AP waiting for connection..."
    apConnected=False
    socketConnected=False
    while True:
        line = ser.readline()
        if len(line) > 0 and apConnected == False and line == "CON0,AC3FA4668DF0\r\n":
            print line
            print "AP Connected!!! Waiting for socket connection..."
            apConnected = True                  
        elif len(line) > 0 and apConnected == True and line == "SOK2,2,8080,192.168.1.1,49153\r\n":
            print "Socket connected..."  
            print line
            socketConnected=True
        elif len(line) > 0 and apConnected == True and socketConnected == True:
            print line[2:(len(line)-1)] #Data format is <STX><CH><data: up to 1400 bytes><ETX>
          
            print "Sending a message back..."
            message = "Hello back from server\n"
            ser.write("\x02\x02"+message+"\x03")
            print readResponse(ser) #should get ACK back
            print readResponse(ser) #should get the DOK back, TCP data sent
          
            while True: #wait for socket to close
                print readResponse(ser) #should get NAKEB when closed
                print readResponse(ser) #followed by SCL2
                exit()
if __name__ == "__main__": main()            