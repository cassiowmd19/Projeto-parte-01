#!/usr/bin/env python3
#!/usr/bin/python                      # This is client.py file

import socket                          # Import socket module

s = socket.socket()
host = socket.gethostname()
port = 12345
s.connect((host,port))

response = ""


while (response != "True"):

    key = input("Entre ID: ")
    senha = input("Entre senha: ")
    msg = ("login,"+ key +","+ senha)
    s.sendall(msg.encode())
    data = s.recv(1024)
    response = data.decode()

    if (response == "True"):
        print("SUCESSO")
        break
    else:
        print("FALHA LOGIN")


while (response == "True"):

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
        s.sendall(msg.encode())
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
        s.sendall(msg.encode())
        data = s.recv(1024)
        alteraTarefa = data.decode()
        if alteraTarefa == "True":
            print("DADOS ALTERADOS COM SUCESSO!")
        else:
            print(alteraTarefa)

    elif valor == "3":
        msg = ("listaTarefa" + "," + key + "," + senha)
        s.sendall(msg.encode())
        data = s.recv(1024)
        buscaTarefa = data.decode()
        print(buscaTarefa)

    elif valor == "4":
        msg = ("buscaTarefaConcl" + "," + key + "," + senha)
        s.sendall(msg.encode())
        data = s.recv(1024)
        buscaTarefaConcl = data.decode()
        print(buscaTarefaConcl)

    elif valor == "5":
        keyTarefa = input("INFORME O CID DA TAREFA: ")
        msg = ("apagarTarefa" + "," + key + "," + senha + "," + keyTarefa)
        s.sendall(msg.encode())
        data = s.recv(1024)
        apagarTarefa = data.decode()
        if apagarTarefa == "True":
            print("TAREFA %s APAGADA DA BASE!" % keyTarefa)
        else:
            print("CLIENTE %s NÃO LOCALIZADO!" % keyTarefa)

    elif valor == "6":
        keyTarefa = input("INFORME O CID DA TAREFA: ")
        msg = ("concluirTarefa" + "," + key + "," + senha + "," + keyTarefa)
        s.sendall(msg.encode())
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



s.close()                              # Close the socket when done

