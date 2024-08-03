
import socket
import os
import time
import threading
import sys
import selectors
import message_parser

PORT = 6668

#key = b"c333d96185bb0737"
key = b"788cd66452425844"

def print_help():
    print("Usage:")
    print("   python3 iotsniffer.py <IP of IoT device>")

def printMsgs(msgBuf):
    print(msgBuf.hex())
    parser = message_parser.Message_Parser(key)
    #raw_msg = bytes.fromhex(msgBuf)
    raw_msg = msgBuf
    iot_message = parser.parse_message(raw_msg)
    print(iot_message.data)
    if(iot_message.data != ""):
        data = iot_message.parse_json_data()
        print(data)
        #print(iot_message.get_json_data().hex(" "))

    return(msgBuf)

def main(argv):
    if(len(argv) < 1):
        print_help();
        return
    #sel = selectors.DefaultSelector()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sel.register(s, selectors.EVENT_READ, data=None)
    ip = argv[0]
    print("connecting to ", ip)
    s.connect((ip,PORT))
    #sel.select()
    connectMsg = b""
    s.send(connectMsg)
    #s.setblocking(0)
    temp_data = b""
    while(1):
        #temp_data = b""
        parsing_msg = True
        while(parsing_msg):
            temp_data += s.recv(1)
            offset = temp_data.find(b"\x00\x00\xaa\x55")
            while(offset != -1) and (offset != 0):
            #if('0000aa55' in temp_data.hex()):
                try:
                    printMsgs(temp_data[:offset+4])
                except:
                    print("error decoding message!!")
                parsing_msg = False
                temp_data = temp_data[offset+5:]
                offset = temp_data.find(b"\x00\x00\xaa\x55")
        time.sleep(.25)

if __name__ == "__main__":
   main(sys.argv[1:])
