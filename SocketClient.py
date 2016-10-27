#This code was tested on Python 2.7.12 on a Windows 7 machine
#pyserial must be installed for script to work

#Tested with TYSA-W version 2.00.00 
#API document: TY_WLAN_WYSACVLXY-XX_AppAPI_V2.00_20160315
#To get a copy of the API document visit http://www.ty-top.com/ and contact your local sales office.

import time
import serial
import sys

def readResponse(ser):
    var=2
    while var != 0:
        line = ser.readline()
        linelength = len(line)
        if linelength > 0:
            var = var -1 
        if var == 0:
            return line

def main():
    #Set serial port to N,8,1  @ 115200     
    ser = serial.Serial(sys.argv[1], 115200, timeout=2)

    print "Performing Soft Reset..."
    ser.write("WRST\r\n")
    print readResponse(ser) #Should get ACK back
    print readResponse(ser) #After reset module sends version number. Read version number.

    print "Configuring client settings using STI command..."
    print "Setting AP Name..."
    ser.write("WSTI101MW300AP\r\n")
    print readResponse(ser) #Should get ACK back

    print "Enabling DHCP..."
    ser.write("WSTI1041\r\n")
    print readResponse(ser) #Should get ACK back

    print "Enabling WPA2 with PSK..."
    ser.write("WSTI1024\r\n")
    print readResponse(ser) #Should get ACK back

    print "Setting passphrase"
    ser.write("WSTI1031234567890\r\n")
    print readResponse(ser) #Should get ACK back

    print "Connecting..."
    ser.write("WICO1\r\n")
    print readResponse(ser) #should get "CON1,MW300AP\r\n" on successful connection
            
    print "Opening socket, using TCP, IP address 192.168.254, Port 8080..."
    ser.write("WSOC0192.168.001.2548080\r\n")
    print readResponse(ser) #should get "SOK1,0,0,192.168.1.254,8080\r\n" successful open

    #send message
    print "Sending message..."
    message = "Hello from client"
    ser.write("\x02\x01"+message+"\x03") #Data format is <STX><CH><data: up to 1400 bytes><ETX>
    print readResponse(ser) #should get ACK back
    print readResponse(ser) #should get the DOK back, TCP data sent

    time.sleep(5) #give the server some time to respond
    line = ser.readline() #read message from server
    print line[2:(len(line)-1)] #Data format is <STX><CH><data: up to 1400 bytes><ETX>
        
    ser.write("WCSO1\r\n") #close socket
    print readResponse(ser) #should get SCL1 back
if __name__ == "__main__": main()