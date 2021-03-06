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
# truncateLine = -1

while True: #Obtendo arquivo de entrada
    filePath = input('Insira o nome do arquivo: ')
    try:
        file = open(filePath, 'r', encoding='utf-8')
        break
    except Exception as e:
        print('\nErro: ' + str(e) + '\nTente novamente! Obs.: se o arquivo não estiver na mesma pasta deste script, use um caminho relativo ou absoluto\n')

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

while True: #Ignorar primeira linha?
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

file.seek(0)
lenCsvFile = len(list(csvFile))

while True: #Truncamento do arquivo
    answer = input('\nDeseja truncar o arquivo? Isto é recomendado para arquivos enormes. Se sim, insira até qual linha deseja que o arquivo seja lido. Se não, apenas pressione enter: ')    
    try:
        if (answer == ''):
            truncateLine = -1
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

print('\nCriando arquivo temporário temp.csv…')
shutil.copy(filePath, './temp.csv') #Copiando o arquivo para um segundo arquivo auxiliar
print('\nCriando arquivo Distâncias.csv que terá os resultados…')
fileAux = open('./temp.csv', 'r', encoding='utf-8')
csvFileAux = csv.reader(fileAux, delimiter=separator)
fileDists = open('./Distâncias.csv', 'w', encoding='utf-8')

file.seek(0)
fileAux.seek(0)

print('\nCalculando todas as distâncias…')
print('Isso pode demorar muito! N² distâncias serão calculadas, onde N é a quantidade de objetos na base de dados menos aqueles após o truncamento.\n')

i = 0
for row in csvFile: #Caluclando as distâncias…
    if (ignore1stLine and i == 0):
        pass
    elif (i > truncateLine):
        break
    else:
        rowRelevant = []
        lineToWrite = ''
        for index in colDist:
            rowRelevant.append(row[index])
        j = 0
        for row2 in csvFileAux:
            if (ignore1stLine and j == 0):
                pass
            elif (j > truncateLine):
                break
            else:
                rowRelevant2 = []
                for index in colDist:
                    rowRelevant2.append(row2[index])
                # print(euclDist(rowRelevant, rowRelevant2))
                lineToWrite += f'{euclDist(rowRelevant, rowRelevant2)}, '
            j += 1
    fileDists.write(f'{lineToWrite[:-2]}\n')
    # fileDists.write('\n')
    fileAux.seek(0) #Voltando a leitura do arquivo auxiliar para o início
    i += 1

print('\nConcluído, finalmente! Os resultados se encontram no arquivo Distâncias.csv, localizado na mesma pasta de onde este script foi rodado.')

file.close()
fileAux.close()
if os.path.exists('./temp.csv'):
    print('\nApagando arquivo temporário…')
    os.remove('./temp.csv')

print('\nFinalizando programa…\n\n')