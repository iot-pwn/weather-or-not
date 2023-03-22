
import message_creator
from iot_message import MSG_FIELDS, MSG_FORMAT, MSG_OFFSETS, CMD_TYPE, IoT_Message

def main():
    key = b"c333d96185bb0737"

    iot_message = IoT_Message()
    iot_message.create_json_data("128",b'\x01\x01\x02\x00')
    print(iot_message.data)
    iot_message.cmd = CMD_TYPE(8).name
    iot_message.seq_num = 384

    creator = message_creator.Message_Creator(key)
    data = creator.build_message(iot_message)
    print(data.hex())

    iot_message = IoT_Message()
    iot_message.create_json_data("128",b'\x01\x01\x02\x00')
    print(iot_message.data)
    iot_message.cmd = CMD_TYPE(7).name
    iot_message.seq_num = 384

    creator = message_creator.Message_Creator(key)
    data = creator.build_message(iot_message)
    print(data.hex())



if __name__ == "__main__":
   main()
