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

import grpc

from excluir import helloworld_pb2, helloworld_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)

        response = "False"

        while(response != "True"):
            key = input("Entre ID: ")
            senha = input("Entre senha: ")
            response = stub.Login(helloworld_pb2.HelloRequest(name=key + "," + senha))
            if(response.message == "True"):
                print("SUCESSO")
                break
            else:
                print("FALHA LOGIN")


        while(response.message == "True"):
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
            print("  10   | SAIR")
            valor = input("INFORME UM CÓDIGO AÇÃO DESEJADA:")
            print("")
            print("-------------------------------------------------------------")


            if valor == "1":
                key = input("INFORME O CID: ")
                nome = input("INFORME O NOME: ")
                senha = input("INFORME SENHA: ")
                insereCliente = stub.InsereCliente(helloworld_pb2.HelloRequest(name=key, nome=nome, senha=senha))
                if insereCliente == "True":
                    return "SUCESSO NO CADASTRO!"
                else:
                    return insereCliente

            elif valor == "2":
                key = input("INFORME O CID: ")
                print("SÓ INFORME VALOR CASO PRECISE ALTERAR A INFORMAÇÃO, DO CONTRÁRIO APERTE ENTER")
                novonome = input("INFORME O NOVO NOME: ")
                novasenha = input("INFORME A NOVA SENHA: ")
                alteraCliente = stub.AlteraCliente(
                    helloworld_pb2.HelloRequest(name=key + "," + novonome + "," + novasenha))
                if alteraCliente == "True":
                    return "DADOS ALTERADOS COM SUCESSO!"
                else:
                    return alteraCliente

            elif valor == "3":
                key = input ("INFORME O CID: ")
                buscaCliente = stub.BuscaCliente(helloworld_pb2.HelloRequest(name=key))
                if buscaCliente == "False":
                    return "CLIENTE NÃO ENCONTRADO!"
                else:
                    nome = buscaCliente.split(" ")[0]
                    senha = buscaCliente.split(" ")[1]
                    return ("CLIENTE %s, SENHA: %s" % nome % senha)

            elif valor == "4":
                key = input("INFORME O CID: ")
                apagarCliente = stub.ApagarCliente(helloworld_pb2.HelloRequest(name=key))
                if apagarCliente == "True":
                    return ("CLIENTE %s APAGADO DA BASE!" % key)
                else:
                    return ("CLIENTE %s NÃO LOCALIZADO!" % key)

            elif valor == "5":
                key = input("INFORME O CID DA TAREFA: ")
                removeTarefa = stub.RemoveTarefa(helloworld_pb2.HelloRequest(name=key))
                if removeTarefa == "True":
                    return ("TAREFA %s APAGADA!" % key)
                else:
                    return ("TAREFA %s NÃO LOCALIZADA!" % key)

            elif valor == "6":
                keyTarefa = input("INFORME O CID DA TAREFA: ")
                nome = input("INFORME O NOME DA TAREFA: ")
                key = input("INFORME O CID DO CLIENTE: ")
                insereTarefa = stub.InsereTarefa(helloworld_pb2.HelloRequest(name=keyTarefa + "," + nome + "," + key))
                if insereTarefa == "True":
                    return "TAREFA INSERIDA COM SUCESSO"
                else:
                    return insereTarefa

            elif valor == "7":
                keyTarefa = input("INFORME O CID DA TAREFA: ")
                print("SÓ INFORME VALOR CASO PRECISE ALTERAR A INFORMAÇÃO, DO CONTRÁRIO APERTE ENTER")
                keyTarefaNovo = input("INFORME O NOVO CID DA TAREFA: ")
                nomeNovo = input("INFORME O NOVO NOME DA TAREFA: ")
                alteraTarefa = stub.AlteraTarefa(
                    helloworld_pb2.HelloRequest(name=keyTarefa + "," + keyTarefaNovo + "," + nomeNovo))
                if alteraTarefa == "True":
                    return "TAREFA ALTERADA COM SUCESSO"
                else:
                    return alteraTarefa

            elif valor == "8":
                key = input("INFORME O CID: ")
                nome = input("INFORME O NOME: ")
                senha = input("INFORME SENHA: ")
                insereAdm = stub.InsereAdm(helloworld_pb2.HelloRequest(name=key, nome=nome, senha=senha))
                if insereAdm.message == "True":
                    print("SUCESSO NO CADASTRO!")
                else:
                    print(insereAdm.message)

            elif valor == "9":
                key = input("INFORME O CID: ")
                print("SÓ INFORME VALOR CASO PRECISE ALTERAR A INFORMAÇÃO, DO CONTRÁRIO APERTE ENTER")
                novonome = input("INFORME O NOVO NOME: ")
                novasenha = input("INFORME A NOVA SENHA: ")
                alteraAdm = stub.AlteraAdm(helloworld_pb2.HelloRequest(name=key + "," + novonome + "," + novasenha))
                if alteraAdm.message == "True":
                    print("DADOS ALTERADOS COM SUCESSO!")
                else:
                    print(alteraAdm.message)

            elif valor == "10":
                response.message = "False"
                return

            else:
                print("CÓDIGO INVÁLIDO!")



if __name__ == '__main__':
    logging.basicConfig()
    run()
