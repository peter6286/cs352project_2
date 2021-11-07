import socket
import sys

"""Root level name server program"""

#populate DNS table
RS_DNS_Table = {}
TSHostname="" #hold the string to send back to client if there is no match in table

'''
def populateData(filename):
    lines = [line.rstrip('\r\n') for line in open(filename)]
    for line in lines:
        lineSplit = line.split()
        if lineSplit[2] == "NS":
            global TSHostname
            TSHostname = line
        else:
            global RS_DNS_Table
            RS_DNS_Table[lineSplit[0].lower()] = line



if __name__ == '__main__':
    populateData("PROJI-DNSRS.txt")
    ##print(RS_DNS_Table)
'''
lines = [line.rstrip('\r\n') for line in open("PROJI-DNSRS.txt")]


for line in lines:
        lineSplit = line.split()
        if lineSplit[2] == "NS":
            TSHostname = line
        else:
            RS_DNS_Table[lineSplit[0].lower()] = line

print(RS_DNS_Table)
#check command line args
rsListenPort = 0

if len(sys.argv) == 2:
    try:
        rsListenPort = int(sys.argv[1])
        #print(sys.argv[1])
    except ValueError:
        exit(1)

else:
    # error, too many or too few command line args-> exit()
    exit(1)

#create server socket
try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #print("[S]: Server socket created")
except socket.error as err:
    #print('socket open error: {}\n'.format(err))
    exit()

server_binding = ('', rsListenPort)
serverSocket.bind(server_binding)
serverSocket.listen(1)
host = socket.gethostname()
#print("[S]: Server host name is {}".format(host))
localhost_ip = (socket.gethostbyname(host))
#print("[S]: Server IP address is {}".format(localhost_ip))
csockid, addr = serverSocket.accept()
#print("[S]: Got a connection request from a client at {}".format(addr))

# send a intro message to the client.
#msg = "Connected to RS server"
#csockid.send(msg.encode('utf-8'))


while True:
    data_from_client = csockid.recv(200)
    recv_msg = data_from_client.decode('utf-8')
    #print("[C]: "+ recv_msg)

    recv_msg=recv_msg.lower()
    if recv_msg == "done":
        break
    else:
        if recv_msg in RS_DNS_Table:
            send_msg =RS_DNS_Table[recv_msg]
            #print("[S]: "+ send_msg)
            csockid.send(send_msg.encode('utf-8'))
        else:
            #print("[S]: " + TSHostname)
            csockid.send(TSHostname.encode('utf-8'))



# Close the server socket
serverSocket.close()
exit()