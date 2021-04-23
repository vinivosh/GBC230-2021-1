# Integrantes do grupo:
# Vinícius Henrique Almeida Praxedes
# # Mateus Pereira
# Mateus Damaceno

# import math
import csv
import os
import random
# import shutil

random.seed()   #Seedando a função random com a hora do sistema

#Funções

def euclDist(obj1 = None, obj2 = None): #Calcula a distância euclidiana entre dois objetos. Presume-se que sejam dois iterators com valores que sejam floats ou que possam ser transformados em. Caso algum erro seja encontrado, valor -1.0 é retornado.
    if (obj1 == None or obj2 == None or obj1 == [] or obj2 == []):
        print('\nErro! Algum dos objetos é nulo ou vazio. Retornando valor de erro (-1.0)…\n')
        return -1.0
    if (obj1 == obj2):
        return 0.0
    try:
        dist = 0
        for i in range(len(obj1)):
            dist +=  (float(obj1[i]) - float(obj2[i]))**2
        dist = dist**0.5
        return dist
    except Exception as e:
        print('\nErro: ' + str(e) + '\n')
        print(f'Cálculo da distância entre o objeto {obj1} e o objeto {obj2} falhou. Retornando valor de erro (-1.0)…\n')
        return -1.0

def rmDupes(_list=[]):  #Remove valores duplicados de listas
    if(_list == [] or _list == None):
        return []
    return list(dict.fromkeys(_list))

### Variáveis globais

# filePath = './iris.data'
# k = 3
# separator = ','
# colDist = [0, 1, 2 ,3]
# ignore1stLine = False
# truncateLine = len(list(csvFile))-1

while True: #Obtendo arquivo de entrada
    filePath = input('Insira o nome do arquivo: ')
    try:
        file = open(filePath, 'r', encoding='utf-8')
        break
    except Exception as e:
        print('\nErro: ' + str(e) + '\nTente novamente! Obs.: se o arquivo não estiver na mesma pasta deste script, use um caminho relativo ou absoluto\n')

while True: #Obtendo a quantidade de grupos (k)
    try:
        k = input('\nInsira a quantidade de grupos desejado (apenas aperte enter para usar o padrão do Iris Dataset de 3 grupos): ').strip()
        if k == '':
            k =  3
        else:
            k = int(k)
            if k <= 0:
                raise ValueError
        break
    except Exception:
        print('\nFavor inserir um número maior que zero!\n')

while True: #Obtendo o caractere separador
    try:
        separator = input('\nInsira o caractere separador do arquivo (apenas aperte enter para usar o padrão de vírgulas): ').strip()
        if separator == '':
            separator =  ','
        else:
            if len(separator) != 1:
                raise(Exception)
        csvFile = csv.reader(file, delimiter=separator)
        break
    except Exception:
        print('\nFavor insira um separador de exatamente um caractere!\n')

while True: #Obtendo as variáveis relevantes para o cálculo de distância
    colDist = input('\nInsira as colunas que representam as variáveis a serem consideradas para o cálculo de distância, separadas por espaços e iniciando em um. Por exemplo, se as variáveis relevantes forem as da 1ª, 3ª e 4ª colunas, bastaria inserir "1 3 4", sem as aspas. (Apenas aperte enter para usar o padrão para o Iris Dataset.): ').strip().split()
    if (colDist ==  []):
        colDist = [0, 1, 2 ,3] #O padrão do Iris Dataset, todas as 5 colunas, exceto a última.
        file.seek(0)   #Voltando a leitura do arquivo para o começo…
        break
    try:
        colDist = rmDupes(list(map(lambda x: int(x)-1, colDist)))
        break
    except Exception as e:
        print('\nErro: ' + str(e) + '\nInsira um conjunto de colunas válido!')

while True: #Ignorar primeira linha?
    answer = input('\nA primeira linha possui os nomes das variáveis? (S)im ou (N)ão? (Enter para selecionar a opção padrão, que é não): ').strip().upper()
    if (answer == ''):
        ignore1stLine = False
        break
    elif (answer in ['S', 'SIM', 'Y', 'YES']):
        ignore1stLine = True
        break
    elif (answer in ['N', 'NÃO', 'NAO', 'NO']):
        ignore1stLine = False
        break
    else:
        print('\nFazor inserir uma resposta válida!\n')

file.seek(0)
lenCsvFile = len(list(csvFile))

while True: #Truncamento do arquivo
    answer = input('\nDeseja truncar o arquivo? Isto é recomendado para arquivos enormes. Se sim, insira até qual linha deseja que o arquivo seja lido. Se não, apenas pressione enter: ')    
    try:
        if (answer == ''):
            truncateLine = lenCsvFile-1 #Não haverá truncamento do arquivo, ou seja, a linha de "truncamento" é a última linha do arquivo
            break
        elif (int(answer) > 0 and int(answer) <= lenCsvFile):
            truncateLine = int(answer)-1
            break
        else:
            raise(ValueError)
    except Exception as e:
        print(f'\nErro: {e}')
        print(f'Insira um número inteiro entre 1 e {lenCsvFile}!')
file.seek(0)

# csvFileArray = []  #Criando uma lista que contém todas rows do csv. Isto carregará o arquivo inteiro na memória, mas vai acabar sendo computacionalmente mais barato quando precisarmos 
# for row in csvFile:
#     csvFileArray.append(row)

print('\nCriando arquivo ResultadosKMeans.csv que terá os agrupamentos…')
fileResults = open('./ResultadosKMeans.csv', 'w', encoding='utf-8')

file.seek(0)

print(f'\nIniciando k-means com {k} grupos…')
centroids = []
print(f'Selecionando {k} centróides aleatoriamente…')
if ignore1stLine:
    start = 1
else:
    start = 0
for i in range(k):  #Selecionando k centróides aleatoriamente…
    centroid = random.randrange(start, truncateLine + 1)    #Gera um inteiro aleatório entre a primeira linha relevante do csv e a última linha a se considerar
    j = 0
    while j <= truncateLine:    #Enquanto estivermos entre 0 e a última linha a se considerar…
        row = next(csvFile)
        if j == centroid:   #Se chegamos na linha correspondente ao número aleatório gerado…
            centroids.append(row)   #Adicionamos este objeto como um centróide inicial
            break
        j += 1
    file.seek(0)    #Voltando o arquivo para o começo

#DEBUG
# centroids = [[5.1,3.5,1.4,0.2], [4.9,3.0,1.4,0.2], [4.7,3.2,1.3,0.2]]

print('centróides selecionados! São eles:\n')
i = 1
for centroid in centroids:
    print(f'centróide #{i}: {centroid}')
    i += 1

i = 0
rowGroups = []  #Vetor com a informação de qual grupo cada datapoint pertence à. O grupo é o index do centróide correspondente em "centroids".
for row in csvFile: #Para cada datapoint…
    if i > truncateLine:   #Se chegamos na última linha a ser considerada, parar após ela
        break
    if (ignore1stLine == True) and (i == 0):    #Ignorar a primeira linha se ignore1stLine for True.
        i += 1
        continue
    if (len(row) == 0): #Se estivermos numa linha cazia, ignorá-la…
        i += 1
        continue
    dist = []   #Vetor de distâncias
    for centroid in centroids:  #Para cada centróide…
        rowRelevant = []
        centroidRelevant = []
        for var in colDist: #Considerar apenas as colunas de index especificados em colDist para calcular a distância…
            rowRelevant.append(row[var])
            centroidRelevant.append(centroid[var])
        dist.append(euclDist(rowRelevant, centroidRelevant))

    #Adiciona ao vetor rowGroups uma lista, onde o primeiro elemento é o número da linha do datapoint atual, e o segundo é o index (na lista "centroids") correspondente ao centróide mais próximo ao datapoint
    rowGroups.append([i, dist.index(min(dist))])
    i += 1

file.seek(0)    #Voltando o arquivo para o começo

#Parte do Mateus Pereira

# 1 a 100 - ok
# recalcular K centroides de cada classe (colDist) - ok
  # Somatoria de cada coluna, divide por N, temos um novo centroide - ok
# atualiza os centroids[]
# calcular distancia de cada row, para clusterizar
# reescrever rowGroups

# append informacoes no arquivo
# plotar grafico

# i = 0
for iter in range(1,100 + 1):
    file.seek(0)
    print(f'\nIteração #{iter}\n')

    centroids = []
    for cluster in range(k):
        clusterAculumator = []
        for col in colDist:
            clusterAculumator.append(0)

        clusterSize = 0
        for data in rowGroups:
            row = next(csvFile)
            if (data[1] == cluster):
                j = 0
                for col in colDist:
                    clusterAculumator[j] += float(row[col])
                    j += 1
                clusterSize += 1

        for col in colDist:
            if clusterSize != 0:
                clusterAculumator[col] /= clusterSize

        centroids.append(clusterAculumator)
        file.seek(0)

    i = 0
    rowGroups = []  #Vetor com a informação de qual grupo cada datapoint pertence à. O grupo é o index do centróide correspondente em "centroids".
    for row in csvFile: #Para cada datapoint…
        if i > truncateLine:   #Se chegamos na última linha a ser considerada, parar após ela
            break
        if (ignore1stLine == True) and (i == 0):    #Ignorar a primeira linha se ignore1stLine for True.
            i += 1
            continue
        if (len(row) == 0): #Se estivermos numa linha vazia, ignorá-la…
            i += 1
            continue
        dist = []   #Vetor de distâncias
        for centroid in centroids:  #Para cada centróide…
            rowRelevant = []
            for var in colDist: #Considerar apenas as colunas de index especificados em colDist para calcular a distância…
                rowRelevant.append(row[var])
            dist.append(euclDist(rowRelevant, centroid))

        #Adiciona ao vetor rowGroups uma lista, onde o primeiro elemento é o número da linha do datapoint atual, e o segundo é o index (na lista "centroids") correspondente ao centróide mais próximo ao datapoint
        rowGroups.append([i, dist.index(min(dist))])
        i += 1

    fileResults.write(f'rowGroups = {rowGroups}\n')

print('\nConcluído, finalmente! Os resultados se encontram no arquivo ResultadosKMeans.csv, localizado na mesma pasta de onde este script foi rodado.')

file.close()
# fileAux.close()
# if os.path.exists('./temp.csv'):
#     print('\nApagando arquivo temporário…')
#     os.remove('./temp.csv')

print('\nFinalizando programa…\n\n')