#! /usr/bin/python
import socket
import sys
HostName=""
#root_p = 53
#top_p = 54
output=[]

if len(sys.argv) == 4:
    rsHostName = str(sys.argv[1])
    try:
        rsListenPort = int(sys.argv[2])
    except ValueError:
        exit("Argument error give port number")
    try:
        tsListenPort = int(sys.argv[3])
    except ValueError:
        exit("Argument error give port number")
else:
    exit("Not enough argument")


buff=[]
for line in open("PROJI-HNS.txt"):
    buff.append(line.strip('\n'))


try:
    rs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[C]: Client socket created")
except socket.error as err:
    print('socket open error: {} \n'.format(err))
    exit()

# Define the port on which you want to connect to the server


#print(socket.gethostname)
#print(root_p)
#print(top_p)

# connect to the server on local machine
#localhost_addr = socket.gethostbyname(socket.gethostname())
localhost_addr = socket.gethostbyname(rsHostName)
server_binding = (localhost_addr, rsListenPort)
rs.connect(server_binding)


for ll in buff:
    inp = ll
    if not inp:     # nothing was input
        continue


    rs.send(inp.encode())
    server1_reply = rs.recv(1024).decode()
    print("message sent from root server1 %s" %(server1_reply))
    if(server1_reply[-2::]=="NS"):
        #print("get new one ")
        for attempt in range(2):
            try:
                ts.send(inp.encode('utf-8'))
                server2_reply = ts.recv(1024).decode()
                print("message sent from top server2 %s" % ( server2_reply))
                output.append(server2_reply)
                f = open("RESOLVED.txt", 'a')  # create the write file and write the data
                f.write(server2_reply)
                f.write('\n')
                break
            except:
                try:
                    ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    print("[C]: Client socket created")
                except socket.error as err:
                    print('socket open error: {} \n'.format(err))
                    exit()

                print(server1_reply.split()[0])
                second_look=server1_reply.split()[0]
                tsServer_addr = socket.gethostbyname(second_look)
                tsServer_binding = (tsServer_addr, tsListenPort)
                ts.connect(tsServer_binding)
    else:
        f = open("RESOLVED.txt", 'a')  # create the write file and write the data
        f.write(server1_reply)
        f.write('\n')
        output.append(server1_reply)

print(output)



'''
    f = open("out-proj0.txt",'a') #create the write file and write the data
    f.write(server_reply)
    f.write('\n')
    i=i+1
'''
# close the client socket
rs.close()
ts.close()
f.close()
exit()