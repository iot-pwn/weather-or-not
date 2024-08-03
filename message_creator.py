
from cryptography.hazmat.backends import openssl
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

import json
import base64
import time
import binascii
from iot_message import MSG_FIELDS, MSG_FORMAT, MSG_OFFSETS, CMD_TYPE, IoT_Message



class Message_Creator:
    def __init__(self,local_key):
        self.key = local_key
        #self.cmd = cmd
        #self.data = json

    def pad(self,msg_data):
        pad_size = 0
        if((len(msg_data) % 16) != 0):
            pad_size = 16 - (len(msg_data) % 16)
        msg_buf = msg_data
        msg_buf += pad_size * chr(pad_size).encode()
        return(msg_buf)

    def encrypt_message(self, message_data):
        backend = openssl.backend

        padded_message_data = self.pad(message_data)
        cipher = Cipher(algorithms.AES(self.key), modes.ECB(), backend=backend)
        encryptor = cipher.encryptor()
        enc_data = encryptor.update(padded_message_data) + encryptor.finalize()
        return(enc_data)

    def calculate_crc(self, msg_data):
        calc_crc = binascii.crc32(msg_data).to_bytes(4,byteorder='big')
        return(calc_crc)

    def build_message(self, iot_message):
        msg_buf = b''
        msg_buf += MSG_FIELDS.HEADER
        msg_buf += MSG_FIELDS.CMD_PAD
        cmd = (iot_message.cmd)
        msg_buf += CMD_TYPE[cmd].to_bytes(4,byteorder='big')
        data = self.encrypt_message(iot_message.data)
        length = len(data) + 23
        msg_buf += length.to_bytes(4,byteorder='big')
        #if(cmd != CMD_TYPE(7).name):
        #    msg_buf += MSG_FIELDS.PAD
        msg_buf += MSG_FIELDS.VERSION_3_3
        msg_buf += MSG_FIELDS.VERSION_HEADER
        msg_buf += iot_message.seq_num.to_bytes(4,byteorder='big')
        msg_buf += MSG_FIELDS.MSG_NUM
        msg_buf += data
        msg_buf += self.calculate_crc(msg_buf)
        msg_buf += MSG_FIELDS.FOOTER
        return(msg_buf)

    def build_udp_message(self, iot_message):
        msg_buf = b''
        msg_buf += MSG_FIELDS.HEADER
        msg_buf += MSG_FIELDS.PAD
        cmd = (iot_message.cmd)
        msg_buf += CMD_TYPE[cmd].to_bytes(4,byteorder='big')
        data = self.encrypt_message(iot_message.data)
        length = len(data) + 23
        msg_buf += length.to_bytes(4,byteorder='big')
        msg_buf += MSG_FIELDS.PAD
        msg_buf += data
        msg_buf += self.calculate_crc(msg_buf)
        msg_buf += MSG_FIELDS.FOOTER
        return(msg_buf)
