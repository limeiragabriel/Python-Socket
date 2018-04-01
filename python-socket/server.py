import socket
import sys
import traceback
from threading import Thread
from messages import *
from perceptron import Perceptron

amostras = [[0.1, 0.4, 0.7],
            [0.3, 0.7, 0.2], 
            [0.6, 0.9, 0.8],
            [0.5, 0.7, 0.1]]

saidas = [1, -1, -1, 1]

rede = Perceptron(amostras=amostras, saidas=saidas,taxa_aprendizado=0.1, epocas=1000)
rede.treinar()

def process_input(input_string):
    print(PROCESSING)
    try:
        teste = [float(x) for x in input_string.split("#")]
        if teste == []: return NO_CONTENT
        result = rede.testar(teste, 'A', 'B')
        return OK + " - " + result
    except:
        return BAD_REQUEST

def client_thread(conn, ip, port, MAX_BUFFER_SIZE = 4096):

    while True:
        input_bytes = conn.recv(MAX_BUFFER_SIZE)

        siz = sys.getsizeof(input_bytes)
        if  siz >= MAX_BUFFER_SIZE:
            print(INPUT_LEN + ": {}".format(siz))

        # decodifica entrada e remove final de linha
        input_client = input_bytes.decode("utf8").rstrip()

        if input_client == "":
            break
            
        res = process_input(input_client)
        print("{} is: {}".format(input_client, res))

        result = res.encode("utf8")
        conn.sendall(result)
    
    conn.close()
    print(CONNECTION_ENDED + " | " + ip + ':' + port + " ended.")

def start_server():

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # start/kill socket

    try:
        soc.bind(("127.0.0.1", 12345))
    except socket.error as msg:
        print('Error: ' + str(sys.exc_info()))
        sys.exit()

    #Start listening
    soc.listen()
    
    print('Server started.')
    # loop principal
    while True:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        print('Establishing connection: ' + ip + ':' + port)
        try:
            Thread(target=client_thread, args=(conn, ip, port)).start()
        except:
            conn.sendall(SERVER_ERROR.encode("utf8"))
            traceback.print_exc()
    soc.close()

start_server()  