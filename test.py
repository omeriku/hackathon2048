
import random



# magic_cookie = "{0:08b}".format(int("0xfeedbeef", 16))
# message_type = "{0:08b}".format(int("0x2", 16))
# server_port = "{0:08b}".format(int("BB6C", 16))     # 47980 port in hex is BB6C
#
# message = magic_cookie + message_type + server_port
# message = str.encode(message)
# print(message)
# print(type(message))
# print(len(magic_cookie))
# print(len(message_type))
# print(len(server_port))


data = ["aa", "df", "sfs", "sdsd" , "sdfsghhh", "eee", "jjjj", "asdf", "ertert"]
random.shuffle(data)
half_num_of_teams = int(9 / 2)

one_group = data[:half_num_of_teams]
two_group = data[half_num_of_teams:]
print(one_group)
print(two_group)