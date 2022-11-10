import pandas as pd
import re

file_antes = open("antes.txt")
linhas_antes = sorted(file_antes.readlines())
#Linhas antes e depois estão organizadas alfabeticamente


file_depois = open("depois.txt")
linhas_depois = sorted(file_depois.readlines())


lista_antes = []
lista_depois = []

for pack_antes in linhas_antes:
  pack_antes = ''.join(re.findall(r'[a-z]+[.0-9a-z]+[-]', pack_antes))
  lista_antes.append(pack_antes)

for pack_depois in linhas_depois:
  pack_depois =''.join(re.findall(r'[a-z]+[.0-9a-z]+[-]', pack_depois))
  lista_depois.append(pack_depois)


lista_versao_antes = []
lista_versao_depois = []


for pack in linhas_antes:
  versao_antes = re.sub(r'[a-z]+[.0-9a-z]+[-]', "", pack)
  lista_versao_antes.append(versao_antes.replace("\n", ""))

for pack in linhas_depois:
  versao_depois = re.sub(r'[a-z]+[.0-9a-z]+[-]', "", pack)
  lista_versao_depois.append(versao_depois.replace("\n", ""))

nome = list(sorted(list(set(lista_antes+lista_depois))))
nome.pop(0)


#novos: 54
novos_key = []
for x in lista_depois:
  if x not in lista_antes:
    novos_key.append(x)

novos_pkg = []
for x in linhas_depois:
  for y in novos_key:
    if re.match(y,x):
      novos_pkg.append(x.replace("\n", ''))



#lista de pacotes sem alterações: 67
sem_alteracoes = []
for x in linhas_depois:
  if x in linhas_antes:
    sem_alteracoes.append(x.replace('\n', ''))


#deletados 2
deletados = []
for x in lista_antes:
  if x not in lista_depois:
    deletados.append(x)

pacotes_deletados = []
for x in linhas_antes:
  for y in deletados:
    if re.match(y,x):
      pacotes_deletados.append(x.replace('\n', ''))


#persistindo apenas pacotes que foram alterados para outra versão
lista1 = [x.replace('\n', '') for x in linhas_antes]
for x in pacotes_deletados:
    lista1.remove(x)

for x in sem_alteracoes:
    lista1.remove(x)
lista2 = [x.replace('\n', '') for x in linhas_depois]
for x in sem_alteracoes:
    lista2.remove(x)

lista3 = []
for x in lista2:
    if x not in novos_pkg:
        lista3.append(x)

#lista1 > pacotes versão antiga
#lista3 > pacotes versão atual
#novos_pkg > pacotes novos instalados
#sem_alteracoes > pacotes que não foram alterados
#pacotes_deletados > pacotes que foram deletados

data_f = {

    "pacotes_atualizados_v1":lista1,
    "pacotes_atualizados_v2":lista3,
    "novos_pacotes_instalados":novos_pkg,
    "pacotes_sem_alteracoes":sem_alteracoes,
    "pacotes_deletados":pacotes_deletados

}


df = pd.DataFrame(data={"pacotes_atualizados_v1":pd.Series(lista1),
                        "pacotes_atualizados_v2":pd.Series(lista3),
                        "novos_pacotes_instalados":pd.Series(novos_pkg),
                        "pacotes_sem_alteracoes":pd.Series(sem_alteracoes),
                        "pacotes_deletados":pd.Series(pacotes_deletados)})

print(df)
