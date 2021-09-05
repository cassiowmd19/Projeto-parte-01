#!/user/bin/env python3
import time

from funcaoserver import FuncaoServer
import paho.mqtt.client as mqtt
import socket


# FUNÇÕES MQTT
def on_connect(client, userdata, flags, rc):
    print("Connected - rc:", rc)


def on_message(client, userdata, message):
    global FLAG
    global chat
    if str(message.topic) != pubtop:
        msgm = str(message.payload.decode("utf-8"))
        if msgm is not None:
            funcao = msgm.split(",")[0]
            key = msgm.split(",")[1]

            if funcao == "InsereCliente":
                nome = msgm.split(",")[2]
                senha = msgm.split(",")[3]
                msg = func.InsereCliente(key, nome, senha)
                print("Requisição", funcao)
                client.publish(pubtop, msg)

            elif funcao == "AlteraCliente":
                nome = msgm.split(",")[2]
                senha = msgm.split(",")[3]
                msg = func.AlteraCliente(key, nome, senha)
                print("Requisição", msg)
                client.publish(pubtop, msg)

            elif funcao == "BuscaCliente":
                msg = func.BuscaCliente(key)
                print("Requisição", msg)
                client.publish(pubtop, str(msg))

            elif funcao == "ApagarCliente":
                msg = func.ApagarCliente(key)
                print("Requisição", msg)
                client.publish(pubtop, msg)

            elif funcao == "RemoveTarefa":
                keytarefa = msgm.split(",")[2]
                msg = func.ApagarTarefa(key, keytarefa)
                print("Requisição", msg)
                client.publish(pubtop, msg)

            elif funcao == "InsereTarefa":
                keytarefa = msgm.split(",")[2]
                nomeTarefa = msgm.split(",")[3]
                print(msgm)
                msg = func.InsereTarefa(key, keytarefa, nomeTarefa)
                print("Requisição", msg)
                client.publish(pubtop, msg)

            elif funcao == "AlteraTarefa":
                keytarefa = msgm.split(",")[2]
                nomeTarefa = msgm.split(",")[3]
                msg = func.InsereTarefa(key, keytarefa, nomeTarefa)
                print("Requisição", msg)
                client.publish(pubtop, msg)

            elif funcao == "BuscaTarefa":
                keytarefa = msgm.split(",")[2]
                msg = func.BuscaTarefa(key, keytarefa)
                print("Requisição", msg)
                client.publish(pubtop, str(msg))


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed:", str(mid), str(granted_qos))


def on_unsubscirbe(client, userdata, mid):
    print("Unsubscribed:", str(mid))


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected Disconnection")


# CONEXÃO VIA SOCKET COM CLIENTE
s = socket.socket()
host = socket.gethostname()
port = 12345
s.bind((host, port))
s.listen(5)

# CONEXÃO MQTT
broker_address = host
port = 1883
client = mqtt.Client()
client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscirbe
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port)

pubtop = "/Request/client"
subtop = "/Request/Adm"
FLAG = True
chat = None
msgm = None
request = None

client.loop_start()
client.subscribe(subtop)

func = FuncaoServer()

print('Aguradando conexão de um cliente')
conn, ender = s.accept()
print('conectado em', ender)

while True:
    try:
        if not conn:
            conn, ender = s.accept()
            print('conectado em', ender)
        data = conn.recv(1024)
        if str(data.decode()).split(",") != [""]:
            funcao = str(data.decode()).split(",")[0]
            key = str(data.decode()).split(",")[1]
            senha = str(data.decode()).split(",")[2]
        else:
            funcao = None
            key = None
            senha = None

        if funcao == "login":
            msg = func.Login(key, senha)
            conn.sendall(msg.encode())
            print("resultado login", msg)

        elif funcao == "insereTarefa":
            msg = func.Login(key, senha)
            print("key, senha", key, senha)
            print("resultado login", msg)
            if (msg == "True"):
                keyTarefa = str(data.decode()).split(",")[3]
                nomeTarefa = str(data.decode()).split(",")[4]
                msg = func.InsereTarefa(key, keyTarefa, nomeTarefa)
                conn.sendall(str(msg).encode())
            else:
                msg = "USUÁRIOS NÃO AUTENTICADO!"
                resposta = conn.sendall(msg.encode())

        elif funcao == "alteraTarefa":
            msg = func.Login(key, senha)
            if (msg == "True"):
                keyTarefa = str(data.decode()).split(",")[3]
                nomeTarefa = str(data.decode()).split(",")[4]
                msg = func.AlteraTarefa(key, keyTarefa, nomeTarefa)
                conn.sendall(msg.encode())
            else:
                msg = "USUÁRIOS NÃO AUTENTICADO!"
                resposta = s.sendall(msg.encode())

        elif funcao == "listaTarefa":
            ret = func.Login(key, senha)
            if (ret == "True"):
                msg = func.ListaTarefa(key)
                if msg == "LISTA DE TAREFAS NÃO ENCONTRADA":
                    conn.sendall(msg.encode())
                else:
                    conn.sendall(str(msg).encode())
            else:
                msg = "USUÁRIOS NÃO AUTENTICADO!"
                conn.sendall(msg.encode())

        elif funcao == "buscaTarefaConcl":
            ret = func.Login(key, senha)
            if (ret == "True"):
                msg = func.ListaTarefaConcluidas(key)
                if msg == "LISTA DE TAREFAS NÃO ENCONTRADA":
                    conn.sendall(msg.encode())
                else:
                    conn.sendall(str(msg).encode())
            else:
                msg = "USUÁRIOS NÃO AUTENTICADO!"
                conn.sendall(msg.encode())

        elif funcao == "apagarTarefa":
            msg = func.Login(key, senha)
            if (msg == "True"):
                keyTarefa = str(data.decode()).split(",")[3]
                msg = func.ApagarTarefa(key, keyTarefa)
                conn.sendall(msg.encode())
            else:
                msg = "USUÁRIOS NÃO AUTENTICADO!"
                conn.sendall(msg.encode())

        elif funcao == "concluirTarefa":
            msg = func.Login(key, senha)
            if (msg == "True"):
                keyTarefa = str(data.decode()).split(",")[3]
                msg = func.ConcluirTarefa(key, keyTarefa)
                conn.sendall(msg.encode())
            else:
                msg = "USUÁRIOS NÃO AUTENTICADO!"
                conn.sendall(msg.encode())
    except ConnectionRefusedError:
        print("Encerrada conexão com cliente %s" % ender)

client.disconnect()
client.loop_stop()
conn.close()  # Close the connection
