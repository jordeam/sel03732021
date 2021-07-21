import socketio

# standard Python
sio = socketio.Client()

server_ip = 'http://192.168.0.4:5000'


@sio.event
def connect():
    print("Conectado ao server!")

@sio.event
def connect_error(data):
    print("Conecção falhou!!!")

@sio.event
def disconnect():
    print("Desconectado do server!")

pos_X = 0
pos_Y = 0
gdata = 0

@sio.on('robot1_get_input')
def on_message(data):

    global pos_X, pos_Y, gdata
    pos_X = data[0]
    pos_Y = data[1]
    gdata = data
    

if __name__ == '__main__':
    print('########### Controle 1 ###########')
    sio.connect(server_ip)
    msg_antes = 0
    while(1):

        if msg_antes != gdata:
            print('Controle 1:\n','X = ',pos_X,' ; ', 'Y = ',pos_Y)
            msg_antes = gdata
