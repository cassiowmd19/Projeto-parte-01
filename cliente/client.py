#!/usr/bin/env python3
#!/usr/bin/python                      # This is client.py file
import socket
###################### CONEXÃO SOCKET ##############################

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

response = ""

###################### VERIFICAÇÃO DE LOGIN ##############################

while (response != "True"):

    key = input("Entre ID: ")
    senha = input("Entre senha: ")
    msg = ("login," + key + "," + senha)
    s.sendto(msg.encode(), (MCAST_GRP, MCAST_PORT))
    data = s.recv(1024)
    response = data.decode()

    if (response == "True"):
        print("SUCESSO")
        break
    else:
        print("FALHA LOGIN")

##################### OPÇÃO DE FUNÇÕES ####################################

while (response == "True"):
  try:
    print("")
    print("-------------------------------------------------------------")
    print("CÓDIGO | AÇÃO")
    print("   1   | INSERIR TAREFA")
    print("   2   | MODIFICAR TAREFA")
    print("   3   | LISTAR TAREFAS")
    print("   4   | LISTAR TAREFAS CONCLUÍDAS")
    print("   5   | APAGAR TAREFA")
    print("   6   | CONCLUIR TAREFA")
    print("   7   | SAIR")
    valor = input("INFORME UM CÓDIGO AÇÃO DESEJADA:")
    print("")
    print("-------------------------------------------------------------")

    if valor == "1":
        keyTarefa = input("INFORME O CID DA TAREFA: ")
        nomeTarefa = input("INFORME O NOME: ")
        msg = ("insereTarefa" + "," + key + "," + senha + "," + keyTarefa + "," + nomeTarefa)
        s.sendto(msg.encode(), (MCAST_GRP, MCAST_PORT))
        data = s.recv(1024)
        insereTarefa = data.decode()
        if insereTarefa == "True":
            print("SUCESSO NO CADASTRO!")
        else:
            print(insereTarefa)

    elif valor == "2":
        keyTarefa = input("INFORME O CID DA TAREFA: ")
        nomeTarefa = input("INFORME O NOVO NOME: ")
        msg = ("alteraTarefa" + "," + key + "," + senha + "," + keyTarefa + "," + nomeTarefa)
        s.sendto(msg.encode(), (MCAST_GRP, MCAST_PORT))
        data = s.recv(1024)
        alteraTarefa = data.decode()
        if alteraTarefa == "True":
            print("DADOS ALTERADOS COM SUCESSO!")
        else:
            print(alteraTarefa)

    elif valor == "3":
        msg = ("listaTarefa" + "," + key + "," + senha)
        s.sendto(msg.encode(), (MCAST_GRP, MCAST_PORT))
        data = s.recv(1024)
        buscaTarefa = data.decode()
        print(buscaTarefa)

    elif valor == "4":
        msg = ("buscaTarefaConcl" + "," + key + "," + senha)
        s.sendto(msg.encode(), (MCAST_GRP, MCAST_PORT))
        data = s.recv(1024)
        buscaTarefaConcl = data.decode()
        print(buscaTarefaConcl)

    elif valor == "5":
        keyTarefa = input("INFORME O CID DA TAREFA: ")
        msg = ("apagarTarefa" + "," + key + "," + senha + "," + keyTarefa)
        s.sendto(msg.encode(), (MCAST_GRP, MCAST_PORT))
        data = s.recv(1024)
        apagarTarefa = data.decode()
        if apagarTarefa == "True":
            print("TAREFA %s APAGADA DA BASE!" % keyTarefa)
        else:
            print("CLIENTE %s NÃO LOCALIZADO!" % keyTarefa)

    elif valor == "6":
        keyTarefa = input("INFORME O CID DA TAREFA: ")
        msg = ("concluirTarefa" + "," + key + "," + senha + "," + keyTarefa)
        s.sendto(msg.encode(), (MCAST_GRP, MCAST_PORT))
        data = s.recv(1024)
        concluirTarefa = data.decode()
        if concluirTarefa == "True":
            print("TAREFA %s CONCLUÍDA!" % keyTarefa)
        else:
            print("TAREFA %s NÃO LOCALIZADA!" % keyTarefa)

    elif valor == "7":
        break

    else:
        print("CÓDIGO INVÁLIDO!")

  except ConnectionError:
      print("Encerrada conexão com cliente %s" % ender)

s.close()


