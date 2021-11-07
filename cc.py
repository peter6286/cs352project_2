import socket
import sys

"""Client program to connect to root and top level name servers"""
#python client.py rsHostname rsListenPort tsListenPort


rsHostName=""
rsListenPort = 0
tsListenPort = 0

results = []

# get command line arguments
if len(sys.argv) == 4:
    rsHostName = str(sys.argv[1])
    try:
        rsListenPort = int(sys.argv[2])
    except ValueError:
        exit(1)
    try:
        tsListenPort = int(sys.argv[3])
    except ValueError:
        exit(1)

#print(rsHostName)
#print(rsListenPort)
#print(tsListenPort)
else:
    print("Invalid Command Line Arguments")
    exit(1)

# socket to talk to rs server
try:
    rsSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#print("[C]: RS Client socket created")
except socket.error as err:
    print('socket open error: {} \n'.format(err))
    exit()

rsServer_addr=socket.gethostbyname(rsHostName)
rsServer_binding=(rsServer_addr,rsListenPort)
rsSocket.connect(rsServer_binding)

# Receive data from the server
#data_from_RSserver = rsSocket.recv(200)
#print("[C]: Data received from  rs server: {}".format(data_from_RSserver.decode('utf-8')))

#data_from_TSserver = tsSocket.recv(200)
#print("[C]: Data received from ts server: {}".format(data_from_TSserver.decode('utf-8')))

#print("")

with open("PROJI-HNS.txt") as file:
    lines = [line.rstrip('\r\n') for line in file]
    for line in lines:
        #print("[C]: "+ line)
        rsSocket.send(line.encode('utf-8'))
        data_from_RSserver = rsSocket.recv(200)
        #check if string has NS flag in it-> send to ts server
        msg_received = data_from_RSserver.decode('utf-8')
        #print("[RS]: " + msg_received)
        if(msg_received.endswith("NS")):
            #if tsSocket has not been opened yet do that in first attempt else send and receive
            for attempt in range(2):
                try:
                    #print("[C]: " + line)
                    tsSocket.send(line.encode('utf-8'))
                    data_from_TSserver = tsSocket.recv(200)
                    msg_received = data_from_TSserver.decode('utf-8')
                    #print("[TS]: " + msg_received)
                    break;
                except:
                    #open socket
                    try:
                        tsSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    #print("[C]: TS Client socket created")
                    except socket.error as err:
                        print('socket open error: {} \n'.format(err))
                        exit()

                    tsServer_addr = socket.gethostbyname(msg_received.split()[0])
                    tsServer_binding=(tsServer_addr, tsListenPort)
                    tsSocket.connect(tsServer_binding)

        #print("")
        results.append(msg_received)

    closing_msg="done"
    rsSocket.send(closing_msg.encode('utf-8'))
    tsSocket.send(closing_msg.encode('utf-8'))

# close the client socket
rsSocket.close()
tsSocket.close()

file = open("RESOLVED.txt","w")
for result in results:
    file.write(result + "\n")
file.close()

exit()