# Integrantes do grupo:
# Vinícius Henrique Almeida Praxedes
# # Mateus Pereira
# Mateus Damaceno

# import math
import csv
import os
import shutil

#Funções
def euclDist(obj1 = None, obj2 = None): #Calcula a distância euclidiana entre dois objetos. Presume-se que sejam dois iterators com valores que sejam floats ou que possam ser transformados em. Caso algum erro seja encontrado, valor -1.0 é retornado.
    if (obj1 == None or obj2 == None or obj1 == [] or obj2 == []):
        print('\nErro! Algum dos objetos é nulo ou vazio. Retornando valor de erro (-1.0)…\n')
        return -1.0
        print()
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

def rmDupes(list_=[]):  #Remove valores duplicados de listas
    if(list_ == [] or list_ == None):
        return []
    return list(dict.fromkeys(list_))

### Variáveis globais

# # filePath = './urbanGB.all/urbanGB.txt'
# # separator = ','
# # colDist = [0, 1]
# ignore1stLine = False

while True:
    filePath = input('Insira o nome do arquivo: ')
    try:
        file = open(filePath, 'r', encoding='utf-8')
        break
    except Exception as e:
        print('\nErro: ' + str(e) + '\nTente novamente! Obs.: se o arquivo não estiver na mesma pasta deste script, use um caminho relativo ou absoluto\n')

while True:
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

while True:
    colDist = input('\nInsira as colunas que representam as variáveis a serem consideradas para o cálculo de distância, separadas por espaços e iniciando em um. Apenas aperte enter para usar todas as colunas. (Por exemplo, se as variáveis relevantes forem as da 1ª, 3ª e 6ª colunas, bastaria inserir "1 3 6", sem as aspas): ').strip().split()
    if (colDist ==  []):
        colDist = list(range(len(next(csvFile)))) #Cria uma lista de 0 até o número de colunas - 1
        file.seek(0)   #Voltando a leitura do arquivo para o começo…
        break
    try:
        colDist = rmDupes(list(map(lambda x: int(x), colDist)))
        break
    except Exception as e:
        print('\nErro: ' + str(e) + '\nInsira um conjunto de colunas válido!')

while True:
    answer = input('\nA primeira linha possui nome das variáveis? (S)im ou (N)ão? (Enter para selecionar a opção padrão, que é não): ').strip().upper()
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

shutil.copy(filePath, './temp.csv') #Copiando o arquivo para um segundo arquivo auxiliar
fileAux = open('./temp.csv', 'r', encoding='utf-8')
csvFileAux = csv.reader(fileAux, delimiter=separator)
fileDists = open('./Distâncias.csv', 'w', encoding='utf-8')

file.seek(0)
fileAux.seek(0)

i = 0
j = 0

for row in csvFile:
    if (ignore1stLine and i == 0):
        pass
    else:
        rowRelevant = []
        strToWrite = ''
        for index in colDist:
            rowRelevant.append(row[index])
        for row2 in csvFileAux:
            if (ignore1stLine and j == 0):
                pass
            else:
                rowRelevant2 = []
                for index in colDist:
                    rowRelevant2.append(row2[index])
                # print(euclDist(rowRelevant, rowRelevant2))
                strToWrite += str(euclDist(rowRelevant, rowRelevant2)) + ', '
            j += 1
    fileDists.write(strToWrite[:-2] + '\n')
    i += 1

# file.seek(0)    #Resetando a leitura do arquivo para o começo…

file.close()
fileAux.close()
if os.path.exists('./temp.csv'):
    os.remove('./temp.csv')

# i = 1
# while True:
#     fRow = next(csvFile, None)
#     # print('[DEBUG]', fRow)
#     if (fRow == None):
#         print('\nErro! Linha especificada não encontrada\n')
#         break #Se fRow for None, chegou ao final do csv e não achamos
#     if (i == separator):
#         # print(f'[DEBUG] Linha encontrada! Index de tal linha: {i}')
#         if columnMissing != None:
#             foundCol = False    #Boolean que indica se foi encontrada a coluna requerida, se houver uma
#             colIndex = 0
#             for col in fRow:
#                 # print(f'[DEBUG] Coluna sendo analizada: {col}')
#                 # print('[DEBUG] col == columnMissing?', (col == columnMissing))
#                 if col == columnMissing:
#                     # print(f'[DEBUG] Coluna encontrada: {col}\n[DEBUG] Índice de tal coluna: {colIndex}')
#                     foundCol = True
#                     break
#                 colIndex+=1
#             if (foundCol == False):
#                 print('\nErro! Coluna especificada não encontrada\n')
#                 exit()
#             break   #Linha e coluna corretas encontradas
#         else:   #Se columnMissing for None então o usuário não especificou a coluna. Será usada a primeira com valores (numéricos) faltando
#             print('Função à implementar…')
#             exit()
#     i+=1

# file.seek(0)    #Volta o arquivo para o começo

# print('\nIniciando contagem da média…\n')
# avg=0.0; i=1; qnt=0
# for row in csvFile:
#     print('[DEBUG] Índice atual:', i)
#     print('[DEBUG]', row)
#     if (i==separator):
#         i += 1
#         continue

#     try:
#         if row != []:
#             avg += float(row[colIndex].replace(',', '.'))
#             qnt += 1
#     except ValueError as e:
#         # print('[DEBUG] DEU RUIM MOFI! Erro =', e)
#         pass

#     # print(f'[DEBUG] row[colindex] = {row[colIndex]}, avg = {avg}, qnt = {qnt}')
#     i += 1

# avg /= qnt

# # print(f'[DEBUG] Média final = {avg}')

# # print(f'[DEBUG] Filmename - extensão = {filePath[0:-4]}')

# print('\nIniciando criação do novo arquivo…\n')

# try:
#     newFile = open((filePath[0:-4]+'_novo.csv'), 'w+', newline='', encoding='utf-8')
# except Exception as e:
#     print(f'\nErro, impossível criar novo arquivo: {e}\n')
#     exit()

# file.seek(0)    #Resetando a leitura do arquivo original…

# i=1
# for row in csvFile:
#     print(f'[DEBUG] row = {row}')
#     if(i == separator):  #Não modificar nada na linha dos nomes…
#         # print(f"[DEBUG] ', '.join(map(lambda item: item.replace(',', '.'), row)) = {', '.join(map(lambda item: item.replace(',', '.'), row))}")
#         newFile.write(', '.join(map(lambda item: item.replace(',', '.'), row)) + '\n')
#         i += 1
#         continue
#     newRow = row
#     if (row != []):
#         if (row[colIndex] == missingChar):
#             newRow[colIndex] = str(avg).replace(',','.')
#         # print(f"[DEBUG] ', '.join(map(lambda item: item.replace(',', '.'), newRow)) = {', '.join(map(lambda item: item.replace(',', '.'), newRow))}")
#         newFile.write(', '.join(map(lambda item: item.replace(',', '.'), newRow)) + '\n')

#     i += 1

# file.close()
# newFile.close()
# print('\nFinalizando programa...\n')