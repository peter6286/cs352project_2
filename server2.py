import socket
import sys
Top_table = {}
TSHostname=""
#tsListenPort = 54

if len(sys.argv) == 2:
    try:
        tsListenPort = int(sys.argv[1])
    except ValueError:
        exit("please provide port number")

else:
    exit("Not enough argument")


buff=[]
for line in open("PROJI-DNSTS.txt"):
    buff.append(line.strip('\n'))

for ll in buff:
        lineSplit = ll.split()
        if lineSplit[2] == "NS":
            TSHostname = ll
        else:
            Top_table[lineSplit[0].lower()] = ll

print(Top_table)

try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[S]: Server socket created")
except socket.error as err:
    print('socket open error: {}\n'.format(err))
    exit()

server_binding = ('', tsListenPort)
ss.bind(server_binding)
ss.listen(1)
host = socket.gethostname()
print("[S]: Server host name is {}".format(host))
localhost_ip = (socket.gethostbyname(host))
print("[S]: Server IP address is {}".format(localhost_ip))
csockid, addr = ss.accept()
print("[S]: Got a connection request from a client at {}".format(addr))

while True:
    client_data = csockid.recv(1024).decode()      # 接收信息
    if client_data == "":       # if empety space escape connection
        exit("close connection")
    orig_msg = client_data
    str = client_data.lower()
    print(str)
    if str in Top_table:
        send_msg = Top_table[str]
        # print("[S]: "+ send_msg)
        csockid.send(send_msg.encode('utf-8'))
    else:
        send_msg = orig_msg + " - Error:HOST NOT FOUND"
        csockid.send(send_msg.encode('utf-8'))
# Close the server socket
#conn.close()
ss.close()
exit()
