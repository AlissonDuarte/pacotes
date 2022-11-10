import pandas as pd
import re


#Abertura de arquivo e organização em ordem alfabética
file_antes = open("antes.txt")
linhas_antes = sorted(file_antes.readlines())

file_depois = open("depois.txt")
linhas_depois = sorted(file_depois.readlines())

#Estas duas listas irão receber o nome do pacote
lista_antes = []
lista_depois = []

#Cada um dos dois "for" abaixo itera sobre o arquivo e os adiciona na lista
#através da RE recortando todo trecho recortando o código equivalente à versão.
for pack_antes in linhas_antes:
  pack_antes = ''.join(re.findall(r'[a-z]+[.0-9a-z]+[-]', pack_antes))
  lista_antes.append(pack_antes)

for pack_depois in linhas_depois:
  pack_depois =''.join(re.findall(r'[a-z]+[.0-9a-z]+[-]', pack_depois))
  lista_depois.append(pack_depois)


lista_versao_antes = []
lista_versao_depois = []


#Estes iteradores fazem o inverso do ultimo, recorta o código equivalente à versão e 
#salva eles na lista_versão_antes/depois
for pack in linhas_antes:
  versao_antes = re.sub(r'[a-z]+[.0-9a-z]+[-]', "", pack)
  lista_versao_antes.append(versao_antes.replace("\n", ""))

for pack in linhas_depois:
  versao_depois = re.sub(r'[a-z]+[.0-9a-z]+[-]', "", pack)
  lista_versao_depois.append(versao_depois.replace("\n", ""))

nome = list(sorted(list(set(lista_antes+lista_depois))))


#novos: 54
#Este iterador encontra os nomes dos pacotes presentes no arquivo "depois.txt"
#e busca cada um desses nomes na lista "antes.txt", caso esteja nas duas listas
#esse pacote pode ter sido atualizado ou mantido igual, caso esteja na segunda e
#não na primeira, esse pacote foi adicionado
novos_key = []
for x in lista_depois:
  if x not in lista_antes:
    novos_key.append(x)

#Este iterador procura, com o auxilio da RE, pelo nome do pacote na na lista equi-
#valente ao "depois.txt", com o método "match" ele recupera o nome completo(nome do
#pacote + versão) e adiciona em uma nova lista chamada "novos_pkg"
novos_pkg = []
for x in linhas_depois:
  for y in novos_key:
    if re.match(y,x):
      novos_pkg.append(x.replace("\n", ''))



#lista de pacotes sem alterações: 67
#estes pacotes estavam presentes em ambas as listas sem modificações.
sem_alteracoes = []
for x in linhas_depois:
  if x in linhas_antes:
    sem_alteracoes.append(x.replace('\n', ''))


#deletados 2
#Foi buscado pelos nomes dos pacotes que estavam no arquivo "antes.txt"
#e não estavam no arquivo "depois", interpretado como arquivos deletados.

deletados = []
for x in lista_antes:
  if x not in lista_depois:
    deletados.append(x)

#a versão do pacote deletado é buscada dentro da lista "linhas_antes" 
#também com o método "match" que recuperará o nome completo do arquivo
pacotes_deletados = []
for x in linhas_antes:
  for y in deletados:
    if re.match(y,x):
      pacotes_deletados.append(x.replace('\n', ''))


# -----------------------Pacotes atualizados-------------------------
#Criada uma nova lista com os valores do arquivo "antes.txt"
#os pacotes no arquivos antes é composto pelos seguintes segmentos:
#pacotes mantidos + pacotes deletados + pacotes atualizados
#Como queremos apenas dessa lista os pacotes com suas versões antigas,
#iremos percorrer a lista eliminando respectivamente os pacotes deletados
#e em seguida os pacotes que foram mantidos iguais
lista1 = [x.replace('\n', '') for x in linhas_antes]
for x in pacotes_deletados:
    lista1.remove(x)

for x in sem_alteracoes:
    lista1.remove(x)
    
#a lista2 recebe os pacotes presentes em "depois.txt" 
#essa lista é composta por:
#pacotes mantidos + pacotes adicionados + pacotes atualizados
#iremos remover dela os pacotes mantidos e os pacotes adicionados
lista2 = [x.replace('\n', '') for x in linhas_depois]
for x in sem_alteracoes:
    lista2.remove(x)




#Este for irá completar o tratamento armazenando na lista3 apenas os valores
#restantes que não são classificados como novos pacotes
#restará nessas duas listas (lista1 e lista3) apenas os pacotes que foram 
#atualizados, com suas versões antigas e versões novas.
lista3 = []
for x in lista2:
    if x not in novos_pkg:
        lista3.append(x)

 #-----Descrição do que contém em cada uma das listas-----
#lista1 > pacotes versão antiga
#lista3 > pacotes versão atual
#novos_pkg > pacotes novos instalados
#sem_alteracoes > pacotes que não foram alterados
#pacotes_deletados > pacotes que foram deletados


#dicionário de arquivos
data_f = {

    "pacotes_atualizados_v1":lista1,
    "pacotes_atualizados_v2":lista3,
    "novos_pacotes_instalados":novos_pkg,
    "pacotes_sem_alteracoes":sem_alteracoes,
    "pacotes_deletados":pacotes_deletados

}

#dataframe de arquivos
df = pd.DataFrame(data={"pacotes_atualizados_v1":pd.Series(lista1),
                        "pacotes_atualizados_v2":pd.Series(lista3),
                        "novos_pacotes_instalados":pd.Series(novos_pkg),
                        "pacotes_sem_alteracoes":pd.Series(sem_alteracoes),
                        "pacotes_deletados":pd.Series(pacotes_deletados)})

print(df.head(10))
