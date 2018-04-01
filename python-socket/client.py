import socket
from messages import *

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #tcp

def start_client():	
	try:
		soc.connect(("127.0.0.1", 12345))
		print(CONNECTED)
	except:
		print(CONNECTION_ERROR)


def encode_input(val_1, val_2, val_3):
	try:
		val_1 = float(val_1)
		val_2 = float(val_2)
		val_3 = float(val_3)
	except:
		print(INPUT_ERROR)

	return str(val_1) + "#" + str(val_2) + "#" + str(val_3)

start_client()

while True:
	print("=============================")
	print(op1)
	print(op2)
	print("=============================")

	opc = input()
	if opc == '2': break
	elif opc == '1':

		print('\n'+INPUT_INST+'\n')

		print(VAL1)
		input1 = input()
		print('\n'+VAL2)
		input2 = input()
		print('\n'+VAL3)
		input3 = input()

		msg = encode_input(input1,input2,input3)

		soc.send(msg.encode("utf8"))                   # encode string para bytes  
		result_bytes = soc.recv(4096)                  # quao grande a msg pode ser em bytes  
		result_string = result_bytes.decode("utf8")    # decodifica o retorno em bytes

		print("Response: {}".format(result_string))
	
	else:
		print("Invalid option")
