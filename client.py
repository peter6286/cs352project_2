#! /usr/bin/python
import threading
import time
import random
import socket

rsHostName=""
root_p = 53
top_p = 54
results=[]

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
localhost_addr = socket.gethostbyname(socket.gethostname())
server_binding = (localhost_addr, root_p)
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
                print("message sent from top server %s" % ( server2_reply))
                results.append(server2_reply)
                f = open("RESOLVED.txt", 'a')  # create the write file and write the data
                f.write(server2_reply)
                f.write('\n')
                break
            except:
                # open new socket
                try:
                    ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    print("[C]: Client socket created")
                except socket.error as err:
                    print('socket open error: {} \n'.format(err))
                    exit()


                tsServer_addr = socket.gethostbyname(server1_reply.split()[0])
                tsServer_binding = (tsServer_addr, top_p)
                ts.connect(tsServer_binding)
    else:
        f = open("RESOLVED.txt", 'a')  # create the write file and write the data
        f.write(server1_reply)
        f.write('\n')
        results.append(server1_reply)

print(results)



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