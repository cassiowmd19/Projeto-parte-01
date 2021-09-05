# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
from hashtable import HashTable
import logging

import grpc
import administrador_pb2
import administrador_pb2_grpc
import paho.mqtt.client as mqtt

import paho.mqtt.client as mqtt
import time
import socket
host = socket.gethostname()

############################## FUNÇÕES MQTT ##############################

def on_connect(client, userdata, flags, rc):
    print("Connected - rc:", rc)

def on_message(client, userdata, message):
    global FLAG
    global chat
    if str(message.topic) != pubtop:
        msg = str(message.payload.decode("utf-8"))
        SetMsg(msg)
        print("Retorno: ", msg)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed:", str(mid), str(granted_qos))

def on_unsubscirbe(client,userdata,mid):
    print("Unsubscribed:", str(mid))

def on_disconnect(client,userdata,rc):
    if rc !=0:
        print("Unexpected Disconnection")

########################## CRIANDO CONEXÃO MQTT ########################

broker_address = host
port = 1883

client = mqtt.Client()
client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscirbe
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port)

time.sleep(1)
pubtop = "/Request/Adm"
subtop = "/Request/client"

client.subscribe(subtop)

client.loop_start()
client.subscribe(subtop)
FLAG = True
chat = None


######################### INSERE PRIMEIRO ADM ###########################

hash = HashTable()
dados = ["nome", "senha"]
key = "01"
hash.insert(key, dados)


def SetMsg(msg):
    global mensagem
    mensagem = msg

def GetMsg():
    return mensagem



class HelloServiceStub(administrador_pb2_grpc.HelloService):

    def Hello(self, request, context):
      try:
        funcao = request.funcao
        id = request.id
        senha = request.senha
        nome = request.nome
        idtarefa = request.idtarefa
        nometarefa = request.nometarefa
        idcliente = request.idcliente
        nomecliente = request.nomecliente
        senhacliente = request. senhacliente

        SetMsg(None)

        if funcao == "InsereCliente":
            text = str(funcao+","+idcliente+","+nomecliente+","+senhacliente)
            client.publish(pubtop, text)

        elif funcao == "AlteraCliente":
            text = str(funcao + "," + idcliente + "," + nomecliente + "," + senhacliente)
            client.publish(pubtop, text)

        elif funcao == "BuscaCliente":
            text = str(funcao + "," + idcliente)
            client.publish(pubtop, text)

        elif funcao == "ApagarCliente":
            text = str(funcao + "," + idcliente)
            client.publish(pubtop, text)

        elif funcao == "RemoveTarefa":
            text = str(funcao + "," + idcliente + "," + idtarefa)
            client.publish(pubtop, text)

        elif funcao == "InsereTarefa":
            text = str(funcao + "," + idcliente + "," + idtarefa + "," + nometarefa)
            client.publish(pubtop, text)

        elif funcao == "AlteraTarefa":
            text = str(funcao + "," + id + "," + idtarefa + "," + nometarefa)
            client.publish(pubtop, text)

        elif funcao == "BuscaTarefa":
            text = str(funcao + "," + idcliente + "," + idtarefa)
            client.publish(pubtop, text)

        elif funcao == "InsereAdm":
            key = request.id
            nome = request.nome
            senha = request.senha
            dados = [nome, senha]
            retorno = hash.insert(key, dados)
            return administrador_pb2.HelloResponse(mensagem=retorno)

        elif funcao == "AlteraAdm":
            key = request.name.id
            novonome = request.nome
            novasenha = request.senha

            nn = hash.setnome(key, novonome)
            ns = hash.setsenha(key, novasenha)

            if nn != novonome:
                return administrador_pb2.HelloResponse(mensagem=nn)
            elif ns != novasenha:
                return administrador_pb2.HelloResponse(mensagem=ns)
            else:
                return administrador_pb2.HelloReply(mensagem="True")

        elif funcao == "Login":
            key = request.id
            senha = request.senha
            status = hash.validaSenha(key, senha)
            return administrador_pb2.HelloResponse(mensagem=status)

        elif funcao == "BuscaCliente":
            return administrador_pb2.HelloResponse(mensagem='Nome: %s' % nome)
        time.sleep(1)
      except :
          print("FALHA NA CONEXÃO SERVER CLIENTE!!!")

      return administrador_pb2.HelloResponse(mensagem=GetMsg())


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    administrador_pb2_grpc.add_HelloServiceServicer_to_server(HelloServiceStub(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
