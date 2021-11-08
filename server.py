import socket
import sys
Root_table = {}
TSHostname=""
#rsListenPort = 53

if len(sys.argv) == 2:
    try:
        rsListenPort = int(sys.argv[1])
    except ValueError:
        exit("please provide port number")

else:
    exit("Not enough argument")



buff=[]
for line in open("PROJI-DNSRS.txt"):
    buff.append(line.strip('\n'))

for ll in buff:
        lineSplit = ll.split()
        if lineSplit[2] == "NS":
            TSHostname = ll
        else:
            Root_table[lineSplit[0].lower()] = ll

print(Root_table)

try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[S]: Server socket created")
except socket.error as err:
    print('socket open error: {}\n'.format(err))
    exit()

server_binding = ('', rsListenPort)
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
    str = client_data.lower()
    print(str)
    if str in Root_table:
        send_msg = Root_table[str]
        # print("[S]: "+ send_msg)
        csockid.send(send_msg.encode('utf-8'))
    else:
        csockid.send(TSHostname.encode('utf-8'))
# Close the server socket
#conn.close()
ss.close()
exit()
