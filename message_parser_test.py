
import message_parser

def main():
    key = b"c333d96185bb0737"

    msg_array = [ "000055aa00000000000000080000004b00000000332e33000000000000a68c00000001a2ec212cfc0b56f9f9ffcf338f1a9cc22117e4915d5a15c784357e3d522e915db24e67d663fd68c891a20f304065da8708c456250000aa55",
    "000055aa00000000000000080000004b00000000332e33000000000000a68d00000001a2ec212cfc0b56f9f9ffcf338f1a9cc228f97f4fe589aa05ff40797a138a08704ced999f354135965e7f7b752612219a4cfae9750000aa55",
    "000055aa00000000000000080000004b00000000332e33000000000000a68e00000001a2ec212cfc0b56f9f9ffcf338f1a9cc22117e4915d5a15c784357e3d522e915dfac3b8d1716c928b5109efd82cc23d8b096148700000aa55",
    "000055aa00000000000000080000004b00000000332e33000000000000a68f00000001a2ec212cfc0b56f9f9ffcf338f1a9cc228f97f4fe589aa05ff40797a138a0870fac3b8d1716c928b5109efd82cc23d8b63c4c0bf0000aa55",
    "000055aa00000000000000080000006b00000000332e33000000000000a6900000000181d4f7ab9b32634e151a479040d032afd1c564887677dbc9736674bbadef8848b8bae14cfbaf33dd8d64f89a4829c6f0d6e3816ee098434b7c9f870cda038191eac50e2c8198fab02560804810761f1767ba45c80000aa55",
    "000055aa00000000000000080000006b00000000332e33000000000000a6910000000181d4f7ab9b32634e151a479040d032afb9fd97dd585857eadce22191139516ca0607deb352b8197fafa382d0cdb67f16d6e3816ee098434b7c9f870cda03819154341173152e8e5ab283a5f7e44968a4360c95530000aa55",
    "000055aa00000000000000080000006b00000000332e33000000000000a6920000000181d4f7ab9b32634e151a479040d032afd1c564887677dbc9736674bbadef8848b8bae14cfbaf33dd8d64f89a4829c6f0d6e3816ee098434b7c9f870cda0381915a23c1e672f45d087858e12f7e376085300e8a280000aa55",
    "000055aa00000000000000080000006b00000000332e33000000000000a6930000000181d4f7ab9b32634e151a479040d032afb9fd97dd585857eadce22191139516ca0607deb352b8197fafa382d0cdb67f16d6e3816ee098434b7c9f870cda0381915574b9b941a24260055d3e899fe95d63508b0fb30000aa55",
    "000055aa00000000000000080000006b00000000332e33000000000000a6940000000181d4f7ab9b32634e151a479040d032afd1c564887677dbc9736674bbadef8848b8bae14cfbaf33dd8d64f89a4829c6f0d6e3816ee098434b7c9f870cda0381910b2a23fbb85fc1326d9cad3d59be6a07480e750c0000aa55",
    "000055aa00000000000000080000006b00000000332e33000000000000a6950000000181d4f7ab9b32634e151a479040d032afb9fd97dd585857eadce22191139516ca0607deb352b8197fafa382d0cdb67f16d6e3816ee098434b7c9f870cda038191a6883750269323b921795f31444373cc51bcd49f0000aa55",
    "000055aa00000000000000080000006b00000000332e33000000000000a6960000000181d4f7ab9b32634e151a479040d032afd1c564887677dbc9736674bbadef8848b8bae14cfbaf33dd8d64f89a4829c6f0d6e3816ee098434b7c9f870cda038191affad516ccac36cbb8f524947073225784fe6b8f0000aa55",
    "48b8bae14c",
    "000055aa00000000000000080000004b00000000332e3300000000000085bc00000001b8a0296f69b85b441024b1cb975557ef8286045259be9777bcdd2ab1704e3b061665e547ec21d256f2e9a63f4c29f1d516b268630000aa55000055aa00000000000000080000004b00000000332e3300000000000085bd00000001c1be99f1539c4d67abefe48809f86115c22d3ec4eaa3cacb",
    "000055aa00000000000000080000003b00000000332e3300000000000085a800000001c05bdc03cb4389467c221bdb05d68b9cd3fe60a684d03b0c7b2feaa3ddcf5d490a15452d0000aa55",
    "000055aa00000000000000070000002c000000012b30e2733dd33074a5be9f3b9b25f56f56f1410f434c43ba2c456809d7cfcc57e6dc94740000aa55",
    "000055aa00000001000000070000000c00000000a505a9140000aa55",
    "000055aa00000001000000070000002c000000014d005b7516c9cbd3c7599782573fc2862c1c7e5b02fea731a8b1b36922d9e1edf2f4f8b80000aa55" ]

    for msg in msg_array:
        parser = message_parser.Message_Parser(key)
        raw_msg = bytes.fromhex(msg)
        iot_message = parser.parse_message(raw_msg)
        print("Cmd:", iot_message.cmd)
        print("Length:", iot_message.length)
        print(iot_message.data)
        if(iot_message.data != ""):
            if(b"{" in iot_message.data):
                data = iot_message.parse_json_data()
            else:
                data = iot_message.data
            print(data)
            #print(data.hex(" "))
        print("")


if __name__ == "__main__":
   main()