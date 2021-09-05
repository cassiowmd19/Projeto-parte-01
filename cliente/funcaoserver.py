#!/usr/bin/python3
#server.py
#!/usr/bin/python                           # This is server.py file
from hashtable import HashTable
from hashtable import HashTable

hash = HashTable()
hashTarefas = HashTable()
dados = ["nome", "senha"]
key = "01"
hash.insert(key, dados)


class FuncaoServer:


  def Login(self, key, senha):
    status = hash.validaSenha(key, senha)
    return status

  def InsereTarefa(self, key, keyTarefa, nomeTarefa):
    dados = [nomeTarefa, "PENDENTE", keyTarefa]
    status = hashTarefas.insert(key, dados)
    return status

  def AlteraTarefa(self, key, keyTarefa, nomeTarefa):
    status = hashTarefas.setnometarefa(key, keyTarefa, nomeTarefa)
    return status

  def ListaTarefa(self, key):
    status = hashTarefas.listaTarefas(key)
    return status

  def ListaTarefaConcluidas(self, key):
   status = hashTarefas.listaConcluidas(key)
   return status

  def ApagarTarefa(self, key, keyTarefa):
   status = hashTarefas.removeTarefa(key, keyTarefa)
   return status

  def ConcluirTarefa(self, key, keyTarefa):
   status = hashTarefas.concluitarefa(key, keyTarefa)
   return status

  def InsereCliente(self, key, nome, senha):
   dados = [nome, senha]
   status = hash.insert(key, dados)
   return status

  def AlteraCliente(self, key, nome, senha):
      if nome != None:
          status1 = hash.setnome(key, nome)
      if senha != None:
          status2 = hash.setsenha(key, senha)
      if status1 != 'True':
          return 'Nome não Alterado'
      if status1 != 'True':
          return 'Senha não Alterada'
      return 'True'

  def BuscaCliente(self, key):
      cliente = hash.find(key)
      return cliente

  def ApagarCliente(self, key):
      status = hash.remove(key)
      return status

  def BuscaTarefa(self, key, keyTarefa):
      status = hashTarefas.findtarefa(key, keyTarefa)
      return status


