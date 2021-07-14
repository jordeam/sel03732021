import socketio

# standard Python
sio = socketio.Client()

server_ip = 'http://192.168.0.4:5000'

pos_X = 0
pos_Y = 0

@sio.on('robot_get_input')
def on_message(data):
    #print('I received a message!')
    #print(data)
    global pos_X, pos_Y
    pos_X = int(data['X'])
    pos_Y = int(data['Y'])


if __name__ == '__main__':
    sio.connect(server_ip)

    while(1):
        print('X = ',pos_X,' ; ', 'Y = ',pos_Y)

