
import socket
import os
import time
import threading
import sys
import selectors
import queue
import message_parser
import message_creator
from random import randbytes
from iot_message import MSG_FIELDS, MSG_FORMAT, MSG_OFFSETS, CMD_TYPE, IoT_Message

temperature_flag = False
alarm_1_on=False
weather_alert=False
fuzzed_bytes = []

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
    print("   python3 iot_command_sender.py <IP of IoT device>")

def printMsgs(msgBuf):
    global parser
    #print(msgBuf.hex())
    print("------")
    iot_message = parser.parse_message(msgBuf)
    print("received: ",iot_message.data)
    if(iot_message.data != ""):
        data = iot_message.parse_json_data()
        print(data)
    print("------")

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
            print("received: ",msg.hex())

def receive_thread(iotSocket,ip):
    global Done
    global receive_queue
    print("receiver running")
    msgBuf = b""
    while(not Done):
        msgBuf += iotSocket.recv(150)
        offset = msgBuf.find(b"\x00\x00\xaa\x55")
        while(offset != -1) and (offset != 0):
            msg = msgBuf[:offset+4]
            receive_queue.put(msg)
            msgBuf = msgBuf[offset+5:]
            offset = msgBuf.find(b"\x00\x00\xaa\x55")
        time.sleep(.25)
    print("receiver done")

def send_thread(iotSocket,ip):
    global send_queue
    print("sender running")
    while(1):
        iot_msg = send_queue.get()
        iotSocket.sendall(iot_msg)
        print("sent msg", iot_msg.hex())
        time.sleep(0.25)

command_list = {"133":16, "132":5, "130":8, "129":4, "128":28, "127":18}

def fuzz_gen_command(cmd):
    return randbytes(command_list[cmd])

def command_sender_thread():
    global Done
    global creator
    global send_queue
    global command_queue
    global command_list
    global alarm_1_on
    global weather_alert
    global temperature_flag

    seq_num = 384
    print("Starting command sender")
    while(not Done):
        cmd = command_queue.get()
        iot_message = IoT_Message()
        handled = False
        control_cmd = cmd

        # This is where we fuzz the crap out of this

        for i in range(0,10000):
            command_bytes = fuzz_gen_command(cmd)

            if command_bytes not in fuzzed_bytes:

                iot_message.create_json_data(control_cmd,command_bytes)
                handled = True
                fuzzed_bytes.append(command_bytes)

                if(handled):
                    iot_message.cmd = CMD_TYPE(7).name
                    iot_message.seq_num = seq_num

                    data = creator.build_message(iot_message)
                    send_queue.put(data)
                    seq_num += 1
                #time.sleep(0.1)

def ui_thread():
    global command_queue
    while(not Done):
        print("Menu:")
        print("  Send type:")
        for item in command_list:
            print(f'{item}: Byte Length = {command_list[item]}')

        option = input()

        if option not in command_list:
            print("Invalid option!")
        else:
            command_queue.put(option)

def main(argv):
    if(len(argv) < 1):
        print_help();
        return

    sel = selectors.DefaultSelector()
    iotSocket = socket.socket(socket.AF_INET,
    socket.SOCK_STREAM)
    iotSocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    sel.register(iotSocket, selectors.EVENT_READ, data=None)
    ip = argv[0]
    print("connecting to ", ip)
    iotSocket.connect((ip,PORT))
    #sel.select()
    time.sleep(2)
    #connectMsg = b"Client Header \"0.2\" Name:\"PF Eth Client\"\n"
    #iotSocket.send(connectMsg)
    receiver = threading.Thread(target=receive_thread,args=((iotSocket,ip)))
    receiver.start()
    sender = threading.Thread(target=send_thread, args=(iotSocket,ip), daemon=True)
    sender.start()
    process_msg = threading.Thread(target=process_message_thread, args=())
    process_msg.start()
    command_sender = threading.Thread(target=command_sender_thread, args=())
    command_sender.start()
    ui_sender = threading.Thread(target=ui_thread, args=())
    ui_sender.start()
    receiver.join()
    #sender.join()
    process_msg.join()
    command_sender.join()

if __name__ == "__main__":
   main(sys.argv[1:])
