from multiprocessing import Process
import socket
import time
import json


def consume():
    while True:
        print("1")
        time.sleep(5)

def produce():
    while True:
        print("2")
        time.sleep(1)



if __name__ == "__main__":

    ip = '192.168.1.37'
    port = 5050
    # output_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # output_socket.bind((ip, port))
    # output_socket.listen()
    #
    # input_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # input_socket.bind((ip, port+1))
    # input_socket.listen()

    print("[SERVER STARTED]")

    # input, addr = input_socket.accept()
    # output, addr = output_socket.accept()

    print("[CLE CONNECTED]")

    anchors = []
    with open("config/anchors.json", "r") as file:
        for line in file:
            anchors.append(json.loads(line))

    for anchor in anchors:
        print(anchor)

    time.sleep(10)

    filename = 'logs/01072021105028peers.log'
    f = open(filename, 'r')
    msgs = []
    for line in f:
        msg = {}
        a = line.split()
        msg["company"] = "MPEI"
        msg["room"] = "Z408"
        msg["time"] = float(a[0])

        if a[1] == "CS_TX":
            msg["receiver"] = a[2]
            msg["sender"] = a[3]
            if msg["receiver"] == msg["sender"]:
                msg["type"] = "CS_TX"
            else:
                msg["type"] = "CS_RX"
            msg["seq"] = int(a[4])
            msg["timestamp"] = float(a[5])
            msgs.append(msg)
        elif a[1] == "BLINK":
            msg["receiver"] = a[2]
            msg["sender"] = a[3]
            msg["type"] = "BLINK"
            msg["sn"] = int(a[4])
            msg["timestamp"] = float(a[5])
            msgs.append(msg)
    f.close()

    print("File readed")

    for msg in msgs:
        print(msg)


    pConsumer = Process(target=consume, args=[])
    pConsumer.start()

    pProducer = Process(target=produce, args=[])
    pProducer.start()

