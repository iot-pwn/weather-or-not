
import socket
import os
import time
import threading
import sys
import selectors
import queue
import message_parser
import message_creator
from iot_message import MSG_FIELDS, MSG_FORMAT, MSG_OFFSETS, CMD_TYPE, IoT_Message

PORT = 6668

key = b"c333d96185bb0737"

Done = False

parser = message_parser.Message_Parser(key)
creator = message_creator.Message_Creator(key)

send_queue = queue.Queue()
receive_queue = queue.Queue()
command_queue = queue.Queue()

def print_help():
    print("Usage:")
    print("   python3 iot_device_mock.py")

def printMsgs(msgBuf):
    global parser
    #print(msgBuf.hex())

    iot_message = parser.parse_message(msgBuf)
    print("received: ",iot_message.data)
    if(iot_message.data != ""):
        data = iot_message.parse_json_data()
        print(data)



def process_message_thread():
    global Done
    global receive_queue
    print("starting process message thread")
    while(not Done):
        msg = receive_queue.get()
        try:
            printMsgs(msg)
        except:
            print("error decoding message!!")

def receive_thread(iotSocket):
    global Done
    global receive_queue
    print("receiver running")
    msgBuf = b""
    while(not Done):
        try:
            msgBuf += iotSocket.recv(150)
            offset = msgBuf.find(b"\x00\x00\xaa\x55")
            while(offset != -1) and (offset != 0):
                msg = msgBuf[:offset+4]
                receive_queue.put(msg)
                msgBuf = msgBuf[offset+5:]
                offset = msgBuf.find(b"\x00\x00\xaa\x55")
        except OSError:
            continue
        time.sleep(.25)
    print("receiver done")

def send_thread(iotSocket):
    global send_queue
    print("sender running")
    while(1):
        iot_msg = send_queue.get()
        iotSocket.send(iot_msg)
        print("sent msg", iot_msg.hex())
        time.sleep(0.25)

def command_sender_thread():
    global Done
    global creator
    global send_queue
    global command_queue
    seq_num = 384
    cmd = "128"
    print("Starting command sender")
    while(not Done):
        iot_message = IoT_Message()
        handled = False
        if(cmd == "128"):
            iot_message.create_json_data("128",b'\x01\x01\x02\x00')
            cmd = "101"
            handled = True
        elif(cmd == "101"):
            iot_message.create_json_data("101",523)
            cmd = "102"
            handled = True
        elif(cmd == "102"):
            iot_message.create_json_data("102",554)
            cmd = "128"
            handled = True
        if(handled):
            iot_message.cmd = CMD_TYPE(8).name
            iot_message.seq_num = seq_num

            data = creator.build_message(iot_message)
            send_queue.put(data)
            seq_num += 1

        time.sleep(2)

def main():

    sel = selectors.DefaultSelector()

    iotSocket = socket.socket(socket.AF_INET,
    socket.SOCK_STREAM)
    try:
        print("Waiting for connection")
        iotSocket.bind(("",PORT))
        iotSocket.listen(1)
        conn,addr = iotSocket.accept()
        print("Connection from ",addr)
        #sel.register(iotSocket, selectors.EVENT_READ, data=None)
        iotSocket.setblocking(0)
        time.sleep(2)
        #sel.select()
        #connectMsg = b"Client Header \"0.2\" Name:\"PF Eth Client\"\n"
        #iotSocket.send(connectMsg)
        receiver = threading.Thread(target=receive_thread,args=((conn,)))
        receiver.start()
        sender = threading.Thread(target=send_thread, args=(conn,), daemon=True)
        sender.start()
        process_msg = threading.Thread(target=process_message_thread, args=())
        process_msg.start()
        command_sender = threading.Thread(target=command_sender_thread, args=())
        command_sender.start()
        receiver.join()
        #sender.join()
        process_msg.join()
        command_sender.join()
    except KeyboardInterrupt:
        iotSocket.close()

if __name__ == "__main__":
   main()
