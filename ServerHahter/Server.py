import socket

data = ''
sensor = ''

connUnity = None
connRaspberry = None

# получаем данные с подключенного пользователя
def dataAcceptance(conn):
    conn.settimeout(3)
    try:
        data = conn.recv(1024)
        if not data:
            return 0
        return data.decode()
    except socket.timeout:
        print("Error ---- Time OUT")
        return b'0'.decode()

def connect(conn,addr):
    global connUnity,connRaspberry
    if addr[0] == '127.0.0.1':
        print("Parser - Unity")
        connUnity = conn
    else:
        print("Parser - raspberry")
        connRaspberry = conn

def mainLoop():
    global data, sensor, connUnity, connRaspberry
    print("Main Loop")
    while 1:
        data = None
        data = dataAcceptance(connUnity)
        print(data)
        if data != '':
            if data == 'D':
                #print("Dat --- Ok")

                connRaspberry.send('D'.encode())
                sensor = dataAcceptance(connRaspberry)
                print("Sensor = " + str(sensor))
                connUnity.send(sensor.encode())

                data = ''
                sensor = ''
            else:
                connRaspberry.send(data.encode())
                data = ''


def StopServer():
    global connRaspberry, connUnity

    if connRaspberry != None:
        connRaspberry.close()
        print("stop connect raspberry")
    if connUnity !=None:
        connUnity.close()
        print("stop connect Unity")


if __name__ == '__main__':  # Program start from here

    sock = socket.socket()
    sock.bind(('', 8599))
    sock.listen(2)
    while 1:
        conn, addr = sock.accept()
        #print('connected:', addr[0])
        try:
            connect(conn, addr)
            if (connUnity != None) and (connRaspberry != None):
                mainLoop()
        except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
            StopServer()

