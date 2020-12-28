




magic_cookie = "{0:08b}".format(int("0xfeedbeef", 16))
message_type = "{0:08b}".format(int("0x2", 16))
server_port = "{0:08b}".format(int("BB6C", 16))     # 47980 port in hex is BB6C

message = magic_cookie + message_type + server_port
message = str.encode(message)
print(message)
print(type(message))
print(len(magic_cookie))
print(len(message_type))
print(len(server_port))
