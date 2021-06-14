# Integrantes do grupo:
# Vinícius Henrique Almeida Praxedes
# # Mateus Pereira
# Mateus Damaceno

import csv
import random
import shutil

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

def relevant(obj = None, rel=[]): #Retorna um novo iterator que é um sub-conjunto do iterator passado em obj. O resultado terá apenas os elementos de índice i em obj, para todo i contido em rel. Presume-se que rel não possui repetições de índices.
  if ((not obj) or (not rel)): # Se alguma entrada for vazia ou nula…
    return None
  objRelevant = []
  try:
    for i in rel:
      objRelevant.append(obj[int(i)])
  except Exception as e:
    print(f'\nErro: {e}\n')
    print(f'\nFalha ao tentar filtrar as variáveis relevantes do datapoint {obj}.')
    return None
  return objRelevant

### Variáveis globais

inf = float('inf')
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
        print('\nErro: ' + str(e) + '\nTente novamente! Obs.: se o arquivo não estiver na mesma pasta deste script, use um caminho relativo ou absoluto.\n')

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
    colDist = input('\nInsira as colunas que representam as variáveis a serem consideradas para o cálculo de distância, separadas por espaços. Por exemplo, se as variáveis relevantes forem as da 1ª, 3ª e 4ª colunas, bastaria inserir "1 3 4", sem as aspas. (Apenas aperte enter para usar o padrão para o Iris Dataset.): ').strip().split()
    if (colDist ==  []):
        colDist = [0, 1, 2 ,3] #O padrão do Iris Dataset, todas as colunas, exceto a última.
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
# file.seek(0)

# Classe da matriz de distâncias
class DistMatrix:
    def __init__(self, path=filePath, sep=separator, colDist=colDist, ignore1stLine=ignore1stLine, truncateLine=truncateLine):
        self.colDesc = [] # Descrição de quais elementos estão sendo representados por cada coluna (e linha também). Cada colDesc[i] dessa lista é uma outra lista contendo os elementos que a coluna (e/ou linha) representa; isto é, representa os grupos criados pelo Single Link na etapa atual. Cada elemento é representado por um dictionary, com duas chaves: 'line', que indica a linha do arquivo do dataset que corresponde contem esse elemento; e 'element', que é uma cópia de tal linha, descrevendo o elemento.
        self.matrix = [] # As distâncias em si, entre cada elemento ou sub-conjunto

        self.file = open(path, 'r', encoding='utf-8')
        self.csvFile = csv.reader(self.file, delimiter=sep)
        self.fileAux = open(path, 'r', encoding='utf-8')
        self.csvFileAux = csv.reader(self.fileAux, delimiter=sep)

        # Preenchendo a matriz de distâncias inicial…
        for i, row1 in enumerate(self.csvFile): # Para cada datapoint…
            if ignore1stLine and i == 0: continue
            if i == truncateLine: break

            line = []
            for j, row2 in enumerate(self.csvFileAux):
                if ignore1stLine and j == 0: continue
                if j == truncateLine: break
                if i >= j: continue # Construindo apenas a diagonal superior da matriz para economizar espaço. A diagonal principal sempre terá distância zero, e a diagonal inferior é o espelho da superior, então ambas não precisam ser guardadas.
                if (row2 == [] or row2 == '' or row2 is None): continue # Se a row2 for vazia, pule-a

                # Adiciona na matriz de distâncias uma lista com quatro elementos, onde [0] = a lista 
                line.append(euclDist(relevant(row1, colDist), relevant(row2, colDist)))                
            self.fileAux.seek(0) # Reseta o arquivo aux para o início

            self.matrix.append(line)

        self.file.seek(0)

        # Preenchendo colDist para descrever o que cada coluna (e linha) da matriz de distâncias representa (isto é, os grupos formados pelo algoritmo, que inicialmente será um por elemento, obviamente).
        for i, row in enumerate(self.csvFile): # Para cada datapoint…
            if ignore1stLine and i == 0: continue
            if i == truncateLine: break
            if (row == [] or row == '' or row is None): continue            
            
            col = [{'line': i+1, 'element': row}]
            self.colDesc.append(col)
        self.file.seek(0)

    # Função auxiliar que devolve a distância entre um elemento ou grupo de elementos, e outro.
    def _CalcDist(self, col1=None, col2=None):
        pass

    # Função auxiliar que "traduz" a matriz econômica (só com a diagonal superior salva) para a sintaxe de uma matriz normal. Retorna o conteúdo em tal índice (traduzido) da matriz.
    def _GetElement(self, i=0, j=0):
        if i==j:
            return inf # Valor infinito é retornado para que nunca sejam consideradas as distâncias de um elemento ou sub-grupo consigo mesmo, que seria sempre zero.
        elif i >= len(self.matrix) or j >= len(self.matrix):
            return None # Se procurar um index maior que o tamanho da matriz, retorna erro!
        elif (i > j):
            return self.matrix[j][i-(j+1)]
        else:
            return self.matrix[i][j-(i+1)]

    # Função auxiliar que devolve uma lista contendo os dois índices da matriz de distâncias onde está a menor distância dela. 
    def _MinDist(self):
        smallest = inf # Inicia a "menor distância" como infinito
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if i >= j: continue # Pula a diagonal principal e inferior
                dist = self._GetElement(i,j)
                if not dist: continue # Se algum erro, pula
                if dist < smallest:
                    smallest = dist
                    answer = [i, j]

        return answer
    
    # Função que retorna uma string com os grupos da iteração atual do single link
    def StringForCsv(self):
        answer = ''
        for group in self.colDesc:
            answer += '{'
            for item in group:
                answer += str(item['element']) + ','
            answer = answer[:-1] + '},'# Retirando a última vírgula e adicionando o fim do grupo + uma vírgula
        
        return answer[:-1] # Retira a última vírgula, pois chegou no último grupo

    # Executa um passo do algoritmo single link, encontrando a menor distância na matriz de distâncias, unindo os elementos ou sub-grupos da linha e coluna correspondente, e atualizando a matrix (e colDist) para refletir a nova matriz de distâncias gerada. Returna True se sucesso e False se falha (quando não há outro passo a ser realizado, por exemplo)
    def GroupUp(self):
        return True    

print('\nCriando arquivo ResultadosSingleLink.csv que terá os grupos…')
fileResults = open('./ResultadosSingleLink.csv', 'w', encoding='utf-8')

print('\nCriando arquivo temporário temp.csv…')
shutil.copy(filePath, './temp.csv') #Copiando o arquivo para um segundo arquivo auxiliar
fileAux = open('./temp.csv', 'r', encoding='utf-8')
csvFileAux = csv.reader(fileAux, delimiter=separator)

file.seek(0)
fileAux.seek(0)

print('\nIniciando single link…')
distMatrix = DistMatrix()

# print(f'\n[DEBUG] Tamanho da distMatrix = {len(distMatrix)}')
# print(f'\n[DEBUG] colDesc = {distMatrix.colDesc}')
# print(f'\n[DEBUG] Matriz de distâncias = {distMatrix.matrix}')

# for i in range(len(distMatrix.matrix)):
#     for j in range(len(distMatrix.matrix)):
#         print(f'matrix.[{i}][{j}] = {distMatrix._GetElement(i,j)}')

# minDist = distMatrix._MinDist()
# print(f'\n[DEBUG] Distância mínima = matrix.{minDist} = {distMatrix._GetElement(minDist[0], minDist[1])}')
# print(f'\n[DEBUG] Grupos = {distMatrix.StringForCsv()}')



# Escrevendo arquivo de resultados…
# file.seek(0)
# i = 0
# for row in csvFile:
#     if (row != []):
#         fileResults.write(f'{row},{rowGroups[i][1]}\n') 
#     i += 1

print('\nConcluído, finalmente! Os resultados se encontram no arquivo ResultadosSingleLink.csv, localizado na mesma pasta de onde este script foi rodado.')

file.close()

print('\nFinalizando programa…\n\n')