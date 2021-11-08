import socket
import sys

tsListenPort=0
if len(sys.argv) == 2:
    # check that this is an integer
    try:
        tsListenPort=int(sys.argv[1])
    except ValueError:
        exit(1)

else:
    # error, too many or too few command line args-> exit()
    exit(1)

TS_DNS_Table = {}

def populateData(filename):
    lines = [line.rstrip('\r\n') for line in open(filename)]
    for line in lines:
        lineSplit = line.split()
        global TS_DNS_Table
        TS_DNS_Table[lineSplit[0].lower()] = line





populateData("PROJI-DNSTS.txt")

try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #print("[S]: Server socket created")
except socket.error as err:
    #print('socket open error: {}\n'.format(err))
    exit()

server_binding = ('', tsListenPort)
serverSocket.bind(server_binding)
serverSocket.listen(1)
host = socket.gethostname()
#print("[S]: Server host name is {}".format(host))
localhost_ip = (socket.gethostbyname(host))
#print("[S]: Server IP address is {}".format(localhost_ip))
csockid, addr = serverSocket.accept()
#print ("[S]: Got a connection request from a client at {}".format(addr))

# send a intro message to the client.
#msg = "Connected to TS server!"
#csockid.send(msg.encode('utf-8'))

while True:
    data_from_client = csockid.recv(200)
    recv_msg = data_from_client.decode('utf-8')
    #print("[C]: "+ recv_msg)

    orig_msg=recv_msg
    recv_msg=recv_msg.lower()
    if recv_msg == "done":
        break
    else:
        if recv_msg in TS_DNS_Table:
            values= TS_DNS_Table[recv_msg]
            send_msg =TS_DNS_Table[recv_msg]
            #print("[S]: "+ send_msg)
            csockid.send(send_msg.encode('utf-8'))
        else:
            send_msg = orig_msg+ " - Error:HOST NOT FOUND"
            #print("[S]: " + send_msg)
            csockid.send(send_msg.encode('utf-8'))

# Close the server socket
serverSocket.close()
exit()