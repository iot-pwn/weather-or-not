
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

temperature_flag = False
alarm_1_on=False
weather_alert=False

PORT = 6668

#key = b"c333d96185bb0737"
key = b"788cd66452425844"

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

command_list = {
    "129F":b'\x01\x00\x02\x00',
    "129":b'\x01\x01\x02\x00',
    "127off":b'\x01\x7f\x00\x00\x00\x00\x02\x7f\x00\x00\x00\x00\x03\x7f\x00\x00\x00\x00',
    "127":b'\x01\xef\x00\x00\x0a\x1e\x02\xef\x00\x00\x00\x00\x03\xef\x00\x00\x00\x00',
    "128off":b'\x65\x00\x03\x01\xf4\xff\x9c\x67\x00\x03\x02\xbc\xfe\x0c\x69\x00\x03\x02\xbc\xfc\x68\x6b\x00\x03\x02\xbc\xfe\x0c',
    "128":b'\x65\x03\x03\x01\xf4\xff\x9c\x67\x03\x03\x02\xbc\xfe\x0c\x69\x03\x03\x02\xbc\xfc\x68\x6b\x03\x03\x02\xbc\xfe\x0c',
    "101":100,
    "102":423,
    "103":423,
    "104":423,
    "105":423,
    "106":423,
    "107":423,
    "108":423
}

command_menu = [["Toggle F/C", "129"],
                ["Send DPS 101", "101"],
                ["Send DPS 102", "102"],
                ["Channel 1 temp", "103"],
                ["Channel 1 humidity", "104"],
                ["Channel 2 temp", "105"],
                ["Channel 2 humidity", "106"],
                ["Channel 3 temp", "107"],
                ["Channel 3 humidity", "108"],
                ["Toggle Alarms State", "127"],
                ["Toggle Local Weather Alarm", "128"],
                ]

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
        if(cmd == "129"):
            if temperature_flag:
                cmd = "129F"
                temperature_flag = False
            else:
                temperature_flag = True

        if(cmd == "127"):
            if alarm_1_on:
                cmd = "127off"
                alarm_1_on = False
            else:
                alarm_1_on = True
        if(cmd == "128"):
            if weather_alert:
                cmd = "128off"
                weather_alert = False
            else:
                weather_alert = True

        try:
            iot_message.create_json_data(control_cmd,command_list[cmd])
            handled = True
        except Exception as e:
            print(f'Error running command for cmd: {cmd}!: {e}')

        """ if(cmd == "101"):
            iot_message.create_json_data("101",423)
            handled = True
        if(cmd == "102"):
            iot_message.create_json_data("102",454)
            handled = True """
        if(handled):
            iot_message.cmd = CMD_TYPE(7).name
            iot_message.seq_num = seq_num

            data = creator.build_message(iot_message)
            send_queue.put(data)
            seq_num += 1
        time.sleep(2)

def ui_thread():
    global command_queue
    while(not Done):
        print("Menu:")
        print("  Send type:")
        for idx,item in enumerate(command_menu):
            print(f'{idx}: {item[0]}')
        # print("    1 - C/F Button")
        # print("    2 - Temp to 52.3 C ")
        # print("    3 - Humidity to 55.4%")
        option = input()
        #command = 0
        try:
            command = command_menu[int(option)][1]
        except:
            print("Invalid option!")
        # if(option == "1"):
        #     command = "129"
        # if(option == "2"):
        #     command = "101"
        # if(option == "3"):
        #     command = "102"
        command_queue.put(command)

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
