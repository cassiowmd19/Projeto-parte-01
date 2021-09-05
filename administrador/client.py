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
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import logging

import case as case
import grpc
import switch as switch

import administrador_pb2
import administrador_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = administrador_pb2_grpc.HelloServiceStub(channel)

        response = "False"

        while(response != "True"):
            key = input("Entre ID: ")
            senha = input("Entre senha: ")
            response = stub.Hello(administrador_pb2.HelloRequest(funcao="Login", id=key, senha=senha))
            if(response.mensagem == "True"):
                print("SUCESSO")
                break
            else:
                print("FALHA LOGIN")


        while(response.mensagem == "True"):
            print("")
            print("-------------------------------------------------------------")
            print("CÓDIGO | AÇÃO")
            print("   1   | INSERIR CLIENTE")
            print("   2   | MODIFICAR CLIENTE")
            print("   3   | BUSCAR CLIENTE")
            print("   4   | APAGAR CLIENTE")
            print("   5   | REMOVER TAREFA CLIENTE")
            print("   6   | INSERIR TAREFA PARA CLIENTE")
            print("   7   | MODIFICAR TAREFA CLIENTE")
            print("   8   | INSERIR NOVO ADMINISTRADOR")
            print("   9   | MODIFICAR ADMINISTRADOR")
            print("  10   | BUSCAR TAREFA")
            print("  11   | SAIR")
            valor = input("INFORME UM CÓDIGO AÇÃO DESEJADA:")
            print("")
            print("-------------------------------------------------------------")


            if valor == "1":
                key = input("INFORME O CID: ")
                nome = input("INFORME O NOME: ")
                senha = input("INFORME SENHA: ")
                insereCliente = stub.Hello(administrador_pb2.HelloRequest(funcao="InsereCliente", idcliente=key, senhacliente=senha, nomecliente=nome))
                if insereCliente.mensagem == "True":
                    print("SUCESSO NO CADASTRO!")
                else:
                    print(insereCliente)

            elif valor == "2":
                key = input("INFORME O CID: ")
                print("SÓ INFORME VALOR CASO PRECISE ALTERAR A INFORMAÇÃO, DO CONTRÁRIO APERTE ENTER")
                novonome = input("INFORME O NOVO NOME: ")
                if novonome == "":
                    novonome = None
                novasenha = input("INFORME A NOVA SENHA: ")
                if novasenha == "":
                    novasenha = None
                alteraCliente = stub.Hello(administrador_pb2.HelloRequest(funcao="AlteraCliente", idcliente=key, nomecliente=novonome, senhacliente=novasenha))
                if alteraCliente.mensagem == "True":
                    print("DADOS ALTERADOS COM SUCESSO!")
                else:
                    print(alteraCliente)

            elif valor == "3":
                key = input("INFORME O CID: ")
                buscaCliente = stub.Hello(administrador_pb2.HelloRequest(funcao="BuscaCliente", idcliente=key))
                if buscaCliente.mensagem is None:
                    print("CLIENTE NÃO ENCONTRADO!")
                else:
                    print(buscaCliente.mensagem)

            elif valor == "4":
                key = input("INFORME O CID: ")
                apagarCliente = stub.Hello(administrador_pb2.HelloRequest(funcao="ApagarCliente", idcliente=key))
                if apagarCliente.mensagem == "True":
                    print("CLIENTE %s APAGADO DA BASE!" % key)
                else:
                    print("CLIENTE %s NÃO LOCALIZADO!" % key)

            elif valor == "5":
                key = input("INFORME O CID DO CLIENTE: ")
                keytarefa = input("INFORME O CID DA TAREFA: ")
                removeTarefa = stub.Hello(administrador_pb2.HelloRequest(funcao="RemoveTarefa", idcliente=key, idtarefa=keytarefa))
                if removeTarefa.mensagem == "True":
                    print("TAREFA %s APAGADA!" % key)
                else:
                    print("TAREFA %s NÃO LOCALIZADA!" % key)

            elif valor == "6":
                keyTarefa = input("INFORME O CID DA TAREFA: ")
                nome = input("INFORME O NOME DA TAREFA: ")
                key = input("INFORME O CID DO CLIENTE: ")
                insereTarefa = stub.Hello(administrador_pb2.HelloRequest(funcao="InsereTarefa", idtarefa=keyTarefa, nometarefa=nome, idcliente=key))
                if insereTarefa.mensagem == "True":
                    print("TAREFA INSERIDA COM SUCESSO")
                else:
                    print(insereTarefa)

            elif valor == "7":
                keyTarefa = input("INFORME O CID DA TAREFA: ")
                key = input("INFORME O CID DO CLIENTE: ")
                nomeNovo = input("INFORME O NOVO NOME DA TAREFA: ")
                alteraTarefa = stub.Hello(administrador_pb2.HelloRequest(funcao="AlteraTarefa", idcliente=key, idtarefa=keyTarefa, nometarefa=nomeNovo))
                if alteraTarefa.mensagem == "True":
                    print("TAREFA ALTERADA COM SUCESSO")
                else:
                    print(alteraTarefa)

            elif valor == "8":
                key = input("INFORME O CID: ")
                nome = input("INFORME O NOME: ")
                senha = input("INFORME SENHA: ")
                insereAdm = stub.Hello(administrador_pb2.HelloRequest(funcao="InsereAdm", id=key, nome=nome, senha=senha))
                if insereAdm.mensagem == "True":
                    print("SUCESSO NO CADASTRO!")
                else:
                    print(insereAdm.mensagem)

            elif valor == "9":
                key = input("INFORME O CID: ")
                print("SÓ INFORME VALOR CASO PRECISE ALTERAR A INFORMAÇÃO, DO CONTRÁRIO APERTE ENTER")
                novonome = input("INFORME O NOVO NOME: ")
                novasenha = input("INFORME A NOVA SENHA: ")
                alteraAdm = stub.Hello(administrador_pb2.HelloRequest(funcao="AlteraAdm", nome=novonome, senha=novasenha))
                if alteraAdm.mensagem == "True":
                    print("DADOS ALTERADOS COM SUCESSO!")
                else:
                    print(alteraAdm.mensagem)

            elif valor == "10":
                keyTarefa = input("INFORME O CID DA TAREFA: ")
                key = input("INFORME O CID DO CLIENTE: ")
                buscaTarefa = stub.Hello(administrador_pb2.HelloRequest(funcao="BuscaTarefa", idcliente=key, idtarefa=keyTarefa))
                print(buscaTarefa.mensagem)

            elif valor == "11":
                response.mensagem = "False"
                return

            else:
                print("CÓDIGO INVÁLIDO!")



if __name__ == '__main__':
    logging.basicConfig()
    run()
