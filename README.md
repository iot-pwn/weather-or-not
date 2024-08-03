# weather-or-not

## Notes for messages to from Tuya devices


STATUS message from device
```
HEADER   CMD_PAD  CMD      MSG_     RET_     VERSION VERSION    SEQ_   MSG_    DATA                                                                                              CRC32    FOOTER
                           LENGTH   CODE             _HEADER     NUM    NUM

0      3        7       11       15       19     22       26       30       34                               50                               66                               82       86       90
000055aa 00000000 00000008 0000004b 00000000 332e33 00000000 0000bff9 00000001 a2ec212cfc0b56f9f9ffcf338f1a9cc2 28f97f4fe589aa05ff40797a138a0870 315db88089aea73b6dd13375727aacca d788fb8b 0000aa55
000055aa 00000000 00000008 0000004b 00000000 332e33 00000000 0000bffa 00000001 a2ec212cfc0b56f9f9ffcf338f1a9cc2 2117e4915d5a15c784357e3d522e915d 315db88089aea73b6dd13375727aacca 409c13c6 0000aa55
000055aa 00000000 00000008 0000004b 00000000 332e33 00000000 0000bffb 00000001 a2ec212cfc0b56f9f9ffcf338f1a9cc2 28f97f4fe589aa05ff40797a138a0870 62e014b4c8e694d95d4a0e133f0b9658 879c9f87 0000aa55
000055aa 00000000 00000008 0000004b 00000000 332e33 00000000 0000bffc 00000001 a2ec212cfc0b56f9f9ffcf338f1a9cc2 2117e4915d5a15c784357e3d522e915d 16bccc7a5babf3eb461c3c182c99227b 74a29bbd 0000aa55
000055aa 00000000 00000008 0000004b 00000000 332e33 00000000 0000bffd 00000001 a2ec212cfc0b56f9f9ffcf338f1a9cc2 28f97f4fe589aa05ff40797a138a0870 16bccc7a5babf3eb461c3c182c99227b 1e071372 0000aa55
000055aa 00000000 00000008 0000004b 00000000 332e33 00000000 0000bffe 00000001 a2ec212cfc0b56f9f9ffcf338f1a9cc2 2117e4915d5a15c784357e3d522e915d a2d0614ee952e2b5ca0ef1b62ad696b9 ec5c113e 0000aa55
000055aa 00000000 00000008 0000004b 00000000 332e33 00000000 0000bfff 00000001 a2ec212cfc0b56f9f9ffcf338f1a9cc2 28f97f4fe589aa05ff40797a138a0870 2104839913cce06f35f9c67d32668bf4 8420fac7 0000aa55
000055aa 00000000 00000008 0000004b 00000000 332e33 00000000 0000c000 00000001 a2ec212cfc0b56f9f9ffcf338f1a9cc2 2117e4915d5a15c784357e3d522e915d 079bf4d1e16a60ca8568779b55188854 b40820c5 0000aa55
```

ERROR CODE from device
```
HEADER   CMD_PAD  CMD      MSG_     RET_     DATA                                                              CRC32    FOOTER
                           LENGTH   CODE
0      3        7       11       15       19                               35                               51       55       59
000055aa 00000000 00000007 0000002c 00000001 2b30e2733dd33074a5be9f3b9b25f56f 56f1410f434c43ba2c456809d7cfcc57 e6dc9474 0000aa55

```

CMD to device
```
HEADER   CMD_PAD  CMD      MSG_     VERSION VERSION    SEQ_   MSG_    DATA
                           LENGTH           _HEADER    NUM    NUM

0      3        7       11       15     18       21       25       29                               45                               61                               77                               93
000055aa 00000000 00000007 0000007b 332e33 00000000 00000180 00000001 c37dd4826c894db64a93dff5da29071b 86a1a68aa2023d78b68d409fbdca7e0e 96590d4f2c09656af401958a1e697354 15058f73a64208dbf8ad201759a0c60e
                                                                  CRC32    FOOTER
                             109                              125      129      134
2299e408b69ad8e19f109e9119444e43 2aa1c04e6a90fb825c723165300c1c6f 41016614 0000aa55
```



cmd data formats:
"data field":<data length>
{"133":16, "132":5, "130":8, "129":4, "128":28, "127":6}

["Toggle F/C", "129"],
  "129F":b'\x01\x00 \x02\x00',
  "129" :b'\x01\x01 \x02\x00',
["Send DPS 101", "101"],
["Send DPS 102", "102"],
["Channel 1 temp", "103"],
["Channel 1 humidity", "104"],
["Channel 2 temp", "105"],
["Channel 2 humidity", "106"],
["Channel 3 temp", "107"],
["Channel 3 humidity", "108"],
["Toggle Alarms State", "127"],
  "127":b'\x01\x7f\x00\x00\x15\x88 \x02\x7f\x00\x00\x00\x00 \x03\x7f\x00\x00\x00\x00 \xFF\x7f\x00\x00\00\x1f',# the last byte here changes the hour
             alarm 1                  alarm2                   alarm3                          ?? causes overflow
["Toggle Local Weather Alarm", "128"],
  "128off":b'\x65\x00\x03\x01\xf4\xff\x9c \x67\x00\x03\x02\xbc\xfe\x0c \x69\x00\x03\x02\xbc\xfc\x68 \x6b\x00\x03\x02\xbc\xfe\x0c',
  "128"   :b'\x65\x03\x03\x01\xf4\xff\x9c \x67\x03\x03\x02\xbc\xfe\x0c \x69\x03\x03\x02\xbc\xfc\x68 \x6b\x03\x03\x02\xbc\xfe\x0c',


?? "133":b'\x65\x00 \x66\x00 \x67\x04 \x68\x03 \x69\x03 \x6a\x03 \x6b\x00 \x6c\x00',
?? "132":b'\x05\x00\x02\x00\x00',
?? "130":b'\x00\x0f \x01\x04 \x02\x04 \x03\x04',
