import socket

data = b''
sensor = b''
getDataSensor = False

# получаем данные с подключенного пользователя
def dataAcceptance(conn):
    conn.settimeout(30)
    data = conn.recv(1024)
    if not data:
        return 0
    return data

# если пользователь unity
def ParserUnity(conn,addr):

    global data
    data = dataAcceptance(conn)
    print(data)

# если пользователь raspberry
def IfGetSensor(conn):
    global data, sensor, getDataSensor
    #print(data)
    if data == b"Dat":
        print("Запрос на данные с датчика")
        conn.send(sensor)
        sensor = b'no sensor'
        getDataSensor = True



def ParserRaspberry(conn,addr):
    global data,sensor, getDataSensor
    if getDataSensor:
        conn.send(b"Dat")
        sensor = dataAcceptance(conn)
        getDataSensor = False
    else:
        conn.send(data)



def connect(conn,addr):
    if addr[0] == '127.0.0.1':
        #print("Parser - Unity")
        ParserUnity(conn, addr)
        IfGetSensor(conn)
        conn.close()

    else:
        #print("Parser - raspberry")
        ParserRaspberry(conn, addr)
        conn.close()


if __name__ == '__main__':  # Program start from here

    sock = socket.socket()
    sock.bind(('', 8599))
    sock.listen(2)
    while 1:
        conn, addr = sock.accept()
        #print('connected:', addr[0])
        try:
            connect(conn, addr)
        except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
            conn.close()

