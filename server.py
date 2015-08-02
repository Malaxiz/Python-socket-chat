import socket
import platform
import threading
import sys

connections = []
threads = []

def execComm(comm, name, client):
    oldName = name[0]
    try:
        if comm[:6] == "/name ":
            try:
                change = comm.split(" ")[1][:-1]
                name.append(change)
                name.pop(0)
                print oldName + " changed name to " + name[0]
                massSendAll(oldName + " changed name to " + name[0] + "\n")
                return "Name changed!"
            except IndexError:
                return "Name not changed! (0)"
        elif comm == "/who\n":
            msg = "Connected: "
            for connName in connections:
                msg += connName[1] + ", "
            msg = msg[:-2]
            client[0].send(msg)
        else:
            print comm
            return "Command error (0)"
    except IndexError:
        return "Command error! (1)"

def massSendAll(msg):
    for conn in connections:
        conn[0].send(msg)

def massSend(msg, client):
    for conn in connections:
        if conn != client:
            conn[0].send(msg)

def clientConn(name, client):
    clientName = ["PythonChatUser"]
    while True:
        inp = client[0].recv(1024)
        msg = clientName[0] + ": " + inp
        if inp[:1] == "/":
            msg = str(execComm(inp, clientName, client)) + "\n"
            client[0].send(msg)
            continue
        if inp != "":
            print msg[:-1]
            massSend(msg, client)

        client[0].send("/ping\n")                                                           # Send ping to client
        recieved = client[0].recv(1024)
        if recieved != "/hello":
            print recieved
            break

        recieved = client[0].recv(1024)                                                     # Get ping request from client
        if recieved == "/ping":
            client[0].send("/hello\n")

    connections.remove(client)
    print "# lost connection to: " + clientName[0] + " (" + client[1] + ")"
    massSendAll("# lost connection to: " + clientName[0] + " (" + client[1] + ")") 

def newConn(name, s):
    while True:
        c, addr = s.accept()
        conn = c.recv(1024) + "@" + str(addr[0])
        print "# connected: " + conn
        massSendAll("# connected: " + conn)
        c.send("Thank you for connecting " + conn)
        client = []
        client.append(c)
        client.append(conn)
        client.append(addr)
        connections.append(client)

        t = threading.Thread(target=clientConn, args=("clientConnThread", client))
        t.start()
        threads.append(t)

def main():
    s = socket.socket()
    host = socket.gethostname()
    port = 1116
    s.bind((host,port))

    print "Server started!"

    s.listen(5)

    t = threading.Thread(target=newConn, args=("newConnThread", s))
    t.start()
    threads.append(t)
    
    while True:
        command = sys.stdin.readline()[:-1]
        if command == "/quit":
            print "Shutting down"
            s.close()
            for thread in threads:
                thread._Thread__stop()
            break

if __name__ == "__main__":
    main()
