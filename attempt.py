import socket
import sys

try:
    tsSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print('socket open error: {} \n'.format(err))
    exit()


print(socket.gethostbyname("localhost"))