import json
import socket
import sklearn
from joblib import load


def load_learned_models(path):
    lr = load(path + 'lr.joblib')
    knr = load(path + 'knr.joblib')
    svr = load(path + 'svr.joblib')
    reg = load(path + 'reg.joblib')
    return lr, knr, svr, reg


# load models
lr, knr, svr, reg = load_learned_models('')


def predict_glucose(data):
    y_pred_lr = lr.predict(data)
    print('lr', y_pred_lr)
    y_pred_knr = knr.predict(data)
    print('knr', y_pred_knr)
    y_pred_svr = svr.predict(data)
    print('svr', y_pred_svr)
    y_pred_reg = reg.predict(data)
    print('reg', y_pred_reg)

    return (y_pred_lr + y_pred_knr + y_pred_svr + y_pred_reg) / 4


def server_program():
    # get the hostname
    #host = socket.gethostname()
    host = '192.168.1.39'
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))

        dia_dict = json.loads(data)

        #s = [[int(i) for i in str(data).split(',')]]
        print(dia_dict)
        predict = str(predict_glucose(dia_dict)) + '\n'

        # сравнение 2 методов (сама модель предсказывает 2+ значчений (Multi-Output Regression) или на основе предыдущик значений)
        # реализовать систему переобучения
        # без персонализвации данных можно сделать, спрость
        # md5 шифрование на android

        print(predict)
        conn.send(predict.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
