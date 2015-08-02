import socket
import platform
import threading
import sys

threads = []

def checkNewMessage(name, s, host, port):
    while True:
        recieved = s.recv(1024)[:-1]
        if recieved == "/ping":
            s.send("/hello")

        s.send("/ping")
        recieved = s.recv(1024)[:-1]
        if recieved != "/hello":
            print recieved
            break
            
    print "Lost connection to server."
    raw_input()
            
def execComm(comm):
    print "Command sent to server."
    return 1

def main():
    connected = False
    host = raw_input("Enter host: ")
    if host == "local":
        host = socket.gethostname()
    print "Connecting to server..."
    
    try:
        s = socket.socket()
        port = 1116

        s.connect((host,port))

        print "Connected!"
        s.send(platform.node())
        print s.recv(1024)
        print "---------------------\n"

        t = threading.Thread(target=checkNewMessage, args=("checkNewMessage", s, host, port))
        t.start()
        threads.append(t)

        nameChange = "/name " + raw_input("Enter name: ") + "\n"
        s.send(nameChange)
        connected = True
    except socket.error:
        print "Could not connect to the server!"


    if connected == True:
        while True:
            inp = sys.stdin.readline()
            if inp[:1] == "/":
                returnVal = execComm(inp)
                if returnVal == 0:
                    continue
            s.send(inp)

        s.close()

if __name__ == "__main__":
    main()
