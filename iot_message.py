
from enum import IntEnum
import json
import base64
import time
import binascii
import os

class MSG_FIELDS(bytes):
    HEADER = b'\x00\x00\x55\xAA'
    FOOTER = b'\x00\x00\xAA\x55'
    VERSION_HEADER = b'\x00\x00\x00\x00'
    VERSION_3_4 = b'\x33\x2E\x34'
    VERSION_3_3 = b'\x33\x2E\x33'
    CMD_PAD = b'\x00\x00\x00\x01'
    PAD = b'\x00\x00\x00\x00'
    MSG_NUM = b'\x00\x00\x00\x00'

class MSG_FORMAT(int):
    HEADER = 4
    CMD_PAD = 4
    CMD = 4
    MSG_LENGTH = 4
    RET_CODE = 4
    VERSION = 3
    VERSION_HEADER = 4
    SEQ_NUM = 4
    MSG_NUM = 4
    MSG_DATA = 48
    CRC32 = 4
    FOOTER = 4

class MSG_OFFSETS(int):
    HEADER = 0
    CMD_PAD = 4
    CMD = 8
    MSG_LENGTH = 12
    RET_CODE = 16
    VERSION = 20
    VERSION_HEADER = 23
    SEQ_NUM = 27
    MSG_NUM = 31
    MSG_DATA = 35
    CRC32 = -8
    FOOTER = -4

class CMD_TYPE(IntEnum):
    UDP = 0
    AP_CONFIG = 1
    ACTIVE = 2
    BIND = 3
    RENAME_GW = 4
    RENAME_DEVICE = 5
    UNBIND = 6
    CONTROL = 7
    STATUS = 8
    HEART_BEAT = 9
    DP_QUERY = 10
    QUERY_WIFI = 11
    TOKEN_BIND = 12
    CONTROL_NEW = 13
    ENABLE_WIFI = 14
    DP_QUERY_NEW = 16
    SCENE_EXECUTE = 17
    UDP_NEW = 19
    AP_CONFIG_NEW = 20
    LAN_GW_ACTIVE = 240
    LAN_SUB_DEV_REQUEST = 241
    LAN_DELETE_SUB_DEV = 242
    LAN_REPORT_SUB_DEV = 243
    LAN_SCENE = 244
    LAN_PUBLISH_CLOUD_CONFIG = 245
    LAN_PUBLISH_APP_CONFIG = 246
    LAN_EXPORT_APP_CONFIG = 247
    LAN_PUBLISH_SCENE_PANEL = 248
    LAN_REMOVE_GW = 249
    LAN_CHECK_GW_UPDATE = 250
    LAN_GW_UPDATE = 251
    LAN_SET_GW_CHANNEL = 252
    UNKNOWN = -1

class JSON_RPC_TYPE(IntEnum):
    REQUEST = 0,
    RESPONSE = 1,
    NOTIFICATION = 2,
    ERROR = 3,
    WRONG_OBJECT = 4

base64_messages = ['127', '128', '129', '130', '131', '132', '133']

if os.path.exists("data.json"):
    with open("data.json", "r") as file:
        data_dict = json.load(file)

else:
    key = input("Please enter a value for 'key': ")
    devId = input("Please enter a value for 'devId': ")
    data_dict = {"key": key, "devId": devId}
    with open("data.json", "w") as file:
        json.dump(data_dict, file)

class IoT_Message:
    def __init__(self):
        self.cmd = 0
        self.length = 0
        self.version = ""
        self.msg_num = 0
        self.data = ""

    def parse_json_data(self):
        return_data = b""
        json_data = self.data.decode('utf-8')
        data = json.loads(json_data)
        #print(json.dumps(data))
        dps_data = data["dps"]
        local_time = time.ctime(data["t"])
        print(local_time)
        print(dps_data)
        if('101' in dps_data):
            return_data = str(dps_data['101'] / 10) + " C"
        if('102' in dps_data):
            return_data = str(dps_data['102'] / 10) + " %"
        if('103' in dps_data):
            return_data = str(dps_data['103'] / 10) + " C"
        if('104' in dps_data):
            return_data = str(dps_data['104'] / 10) + " %"
        if('105' in dps_data):
            return_data = str(dps_data['105'] / 10) + " C"
        if('106' in dps_data):
            return_data = str(dps_data['106'] / 10) + " %"
        if('107' in dps_data):
            return_data = str(dps_data['107'] / 10) + " C"
        if('108' in dps_data):
            return_data = str(dps_data['108'] / 10) + " %"
        if('126' in dps_data):
            return_data = dps_data['126']
        if('127' in dps_data):
            #print(dps_data['128'])
            b64_decoded_data = base64.b64decode(dps_data['127'])
            #print(b64_decoded_data)
            return_data = b64_decoded_data.hex(" ")
        if('128' in dps_data):
            #print(dps_data['128'])
            b64_decoded_data = base64.b64decode(dps_data['128'])
            #print(b64_decoded_data)
            return_data = b64_decoded_data.hex(" ")
        if('129' in dps_data):
            #print(dps_data['129'])
            b64_decoded_data = base64.b64decode(dps_data['129'])
            #print(b64_decoded_data)
            return_data = b64_decoded_data.hex(" ")
        if('130' in dps_data):
            b64_decoded_data = base64.b64decode(dps_data['130'])
            #print(b64_decoded_data)
            return_data = b64_decoded_data.hex(" ")
        if('131' in dps_data):
            b64_decoded_data = base64.b64decode(dps_data['131'])
            #print(b64_decoded_data)
            return_data = b64_decoded_data.hex(" ")
        if('132' in dps_data):
            b64_decoded_data = base64.b64decode(dps_data['132'])
            #print(b64_decoded_data)
            return_data = b64_decoded_data.hex(" ")
        if('133' in dps_data):
            b64_decoded_data = base64.b64decode(dps_data['133'])
            #print(b64_decoded_data)
            return_data = b64_decoded_data.hex(" ")
        return(return_data)



    def create_json_data(self,dps,data):
        if(dps in base64_messages):
            data = base64.b64encode(data).decode('utf-8')
        dps_data = {}
        dps_data[dps] = data
        json_data = {}
        json_data["devId"] = data_dict["gw_di"]["id"]#"eba3e8421dd9524756bxls"
        json_data["uid"] = data_dict["gw_di"]["s_id"]#"000003c1yv"
        json_data["t"] = int(time.time())
        json_data["dps"] = dps_data

        #print(json_data)
        data = json.dumps(json_data)
        data = data.replace(" ","")
        self.data = data.encode('utf-8')

    def create_udp_json_data(self,key,value):
        json_data = {}
        json_data["json_rpc"] = "2.0"
        json_data["method"] = 3
        json_data["id"] = "eb5a5716575b946adeu2fc"
        json_data["params"] = 0
        json_data["error"] = 0
        json_data["result"] = 0
        data = json.dumps(json_data)
        data = data.replace(" ","")
        self.data = data.encode('utf-8')
