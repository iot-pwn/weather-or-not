
from cryptography.hazmat.backends import openssl
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from enum import IntEnum
import json
import base64
import time
import binascii
from iot_message import MSG_FIELDS, MSG_FORMAT, MSG_OFFSETS, CMD_TYPE, IoT_Message


class Message_Parser:
    def __init__(self,local_key):
        self.key = local_key

    def encrypt_message(self, message_data):
        backend = openssl.backend

        cipher = Cipher(algorithms.AES(self.key), modes.ECB(), backend=backend)
        encryptor = cipher.encryptor()
        enc_data = encryptor.update(message_data) + encryptor.finalize()
        return(enc_data)

    def unpad(self,msg_data):
        #print(msg_data)
        padlen = ord(msg_data[-1:])
        right_end = len(msg_data) - padlen
        #print(msg_data[:right_end+1])
        return(msg_data[:right_end])


    def decrypt_message(self, encrypted_data):
        backend = openssl.backend
        unpadder = padding.PKCS7(64).unpadder()

        cipher = Cipher(algorithms.AES(self.key), mode=modes.ECB(), backend=backend)
        decryptor = cipher.decryptor()
        padded_message_data = decryptor.update(encrypted_data) + decryptor.finalize()
        message_data = self.unpad(padded_message_data)
        #print(padded_message_data)
        #message_data = unpadder.update(padded_message_data) + b"}"
        #print(message_data)
        return(message_data)

    def validate_crc(self, msg_data, msg_crc):
        ret_code = False
        calc_crc = binascii.crc32(msg_data).to_bytes(4,byteorder='big')
        #print(calc_crc.hex())
        if(calc_crc == msg_crc):
            ret_code = True
        return(ret_code)


    def parse_message(self,raw_msg):
        msg = IoT_Message()

        if((MSG_FIELDS.HEADER in raw_msg) and (MSG_FIELDS.FOOTER in raw_msg)):
            #msg_end = len(raw_msg) - MSG_FORMAT.CRC32 - MSG_FORMAT.FOOTER
            end = raw_msg.find(MSG_FIELDS.FOOTER)+len(MSG_FIELDS.FOOTER)
            data = raw_msg[:end]
            #print(data.hex())
            data_offset = MSG_OFFSETS.VERSION
            if(MSG_FIELDS.VERSION_3_3 in data):
                data_offset = data.find(MSG_FIELDS.VERSION_3_3) + 15
            raw_data = data[data_offset:MSG_OFFSETS.CRC32]
            print(raw_data.hex())
            msg_data_length = len(raw_data)
            #print(msg_data_length)
            if(msg_data_length > 0):
                decrypted_msg = self.decrypt_message(raw_data)
                print(decrypted_msg)
                msg.data = decrypted_msg
            msg.length = int.from_bytes(raw_msg[MSG_OFFSETS.MSG_LENGTH:MSG_OFFSETS.MSG_LENGTH+4], byteorder='big')
            msg.cmd = CMD_TYPE(int.from_bytes(raw_msg[MSG_OFFSETS.CMD:MSG_OFFSETS.CMD+4], byteorder='big')).name
            return_code = int.from_bytes(raw_msg[MSG_OFFSETS.RET_CODE:MSG_OFFSETS.RET_CODE+4], byteorder='big')
            print("RET_CODE: ",return_code)
            if(self.validate_crc(raw_msg[:MSG_OFFSETS.CRC32], raw_msg[MSG_OFFSETS.CRC32:MSG_OFFSETS.FOOTER])):
                print("CRC validates")
            else:
                print("CRC mismatch")
            #msg.cmd = CMD_TYPE(cmd_int).name
        return(msg)
