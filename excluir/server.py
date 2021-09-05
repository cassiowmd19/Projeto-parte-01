#!/user/bin/env python3
import time

from funcaoserver import FuncaoServer
import paho.mqtt.client as mqtt
import socket, threading

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
                client.publish(pubtop, msg)


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed:", str(mid), str(granted_qos))

def on_unsubscirbe(client,userdata,mid):
    print("Unsubscribed:", str(mid))

def on_disconnect(client,userdata,rc):
    if rc !=0:
        print("Unexpected Disconnection")

def run(conn):
    while True:
        data = conn.recv(1024) # receber informacao
        if not data: # se o cliente tiver desligado
            conns.remove(conn)
            break
        for c in conns: # enviar mensagem para todos os outros clientes
            if c is not conn: # excepto para o que a enviou
                c.send('{}: {}'.format(conn.getpeername(), data.decode()).encode('utf-8'))


# CONEXÃO VIA SOCKET COM CLIENTE
s = socket.socket()
host = socket.gethostname()
port = 12345
s.bind((host, port))
s.listen(5)


broker_address = host
port = 1883

client = mqtt.Client()
client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscirbe
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port)

pubtop = "/Pub/client"
subtop = "/Sub/Adm"
FLAG = True
chat = None
msgm = None
request = None

client.loop_start()
client.subscribe(subtop)

func = FuncaoServer()

conns = set() # armazenar conxoes aqui
host = socket.gethostname()
port = 12345

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reutilizar endereco logo a seguir a fechar o servidor
s.bind((host, port))
s.listen(5)

conn, addr = s.accept()  # esperar que alguem se conect
conn.send('WELCOME {}'.format(addr).encode())
conns.add(conn)  # adicionar conexao ao nosso set de coneccoes
threading.Thread(target=run, args=(conn,)).start()  # esta coneccao vai ser independente das outra a partir de agora, vamos correr a thread na funcao run


while True:
 try:

   data = conn.recv(1024)

   funcao = str(data.decode()).split(",")[0]
   key = str(data.decode()).split(",")[1]
   senha = str(data.decode()).split(",")[2]

   print("key, senha", key, senha)

   if funcao == "login":
    msg = func.Login(key, senha)
    conn.sendall(msg.encode())
    print("resultado login", msg)

   elif funcao == "insereTarefa":
    msg = func.Login(key, senha)
    print("key, senha", key, senha)
    print("resultado login" ,msg)
    if(msg == "True"):
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
   else:
        print("FALHA!!!")
 except ConnectionError:
     print("Encerrada conexão com cliente %s" % ender)

client.disconnect()
client.loop_stop()
conn.close()                                # Close the connection





