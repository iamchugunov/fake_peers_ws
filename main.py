from multiprocessing import Process
import socket
import time
import json

def send_to_cle(data2send, s):
    data2send = json.dumps(data2send).encode()
    s.sendall(len(data2send).to_bytes(4, "little"))
    s.sendall(data2send)


def receive_from_cle(s):
    rcv_size = int.from_bytes(s.recv(4), 'little')
    msg = json.loads(s.recv(rcv_size).decode())
    return msg


def consume(in_put):
    while True:
        data = receive_from_cle(in_put)
        print(data)


def produce(out_put, room_config, msgs):
    # command = input("Input: ")
    # if command == "sc":
    #     send_to_cle(room_config, out_put)
    # elif command == "start":
    #     for msg in msgs:
    #         send_to_cle(msg, out_put)
    # else:
    #     print("Unknown command")
    print(room_config)
    send_to_cle(room_config, out_put)
    for msg in msgs:
        send_to_cle(msg, out_put)

if __name__ == "__main__":

    COMPANY = "MPEI"
    ROOM = "Z408"

    ip = '192.168.1.37'
    port = 5050
    output_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    output_socket.bind((ip, port))
    output_socket.listen()

    input_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    input_socket.bind((ip, port+1))
    input_socket.listen()

    print("[SERVER STARTED]")

    in_put, addr = input_socket.accept()
    out_put, addr = output_socket.accept()

    print("[CLE CONNECTED]")

    anchors = []
    with open("config/anchors.json", "r") as file:
        for line in file:
            anchors.append(json.loads(line))

    room_config = {}
    room_config["type"] = "room_config"
    room_config["company"] = COMPANY
    room_config["room"] = ROOM
    room_config["anchors"] = anchors

    # for anchor in anchors:
    #     print(anchor)

    # time.sleep(10)

    filename = 'logs/01072021105028peers.log'
    f = open(filename, 'r')
    msgs = []
    for line in f:
        msg = {}
        a = line.split()
        msg["company"] = COMPANY
        msg["room"] = ROOM
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

    # for msg in msgs:
    #     print(msg)


    pConsumer = Process(target=consume, args=[in_put])
    pConsumer.start()

    pProducer = Process(target=produce, args=[out_put, room_config, msgs])
    pProducer.start()

