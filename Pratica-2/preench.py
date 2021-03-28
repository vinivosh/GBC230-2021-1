# Integrantes do grupo:
# Vinícius Henrique Almeida Praxedes
# Mateus Damaceno
# Mateus Pereira

import math
import csv

# fileName = './Dados teste.csv'
# columnMissing = 'Patrimônio total no dia da morte'
# colNamesLine = 1
# missingChar = '?'

while True:
    fileName = input('Insira o nome do arquivo: ')
    try:
        file = open(fileName, 'r', newline='', encoding='utf-8')
        csvFile = csv.reader(file, delimiter=',')
        break
    except FileNotFoundError:
        print('\nErro, arquivo não encontrado, tente novamente!')
        print('Obs.: se o arquivo não estiver na mesma pasta deste script, use um caminho relativo ou absoluto\n')

while True:
    try:
        colNamesLine = input('Insira o número (iniciando em 1) da linha que contém os nomes da coluna (apenas aperte enter para usar a primeira linha): ').strip()
        # print('[DEBUG] columnMissing =', columnMissing)
        if colNamesLine == '':
            colNamesLine =  1
        else:
            colNamesLine = int(colNamesLine)
            if colNamesLine < 1:
                raise(Exception)
        break
    except Exception:
        print('\nFavor insira um número inteiro >= 1\n')

while True:
    columnMissing = input('Insira o nome da coluna a ter seus valores ausentes preenchidos: ')
    if (columnMissing.strip() ==  ''):
        print('\nFazor inserir um nome não-vazio\n')
    else:
        break

while True:
    missingChar = input('Insira o caractere que representa um valor ausente (apenas aperte enter para considerar uma célula vazia como um valor ausente): ')
    if (len(missingChar) > 1):
        print('\nFazor inserir nenhum ou apenas um caractere!\n')
    else:
        break


i = 1
while True:
    fRow = next(csvFile, None)
    # print('[DEBUG]', fRow)
    if (fRow == None):
        print('\nErro! Linha especificada não encontrada\n')
        break #Se fRow for None, chegou ao final do csv e não achamos
    if (i == colNamesLine):
        # print(f'[DEBUG] Linha encontrada! Index de tal linha: {i}')
        if columnMissing != None:
            foundCol = False    #Boolean que indica se foi encontrada a coluna requerida, se houver uma
            colIndex = 0
            for col in fRow:
                # print(f'[DEBUG] Coluna sendo analizada: {col}')
                # print('[DEBUG] col == columnMissing?', (col == columnMissing))
                if col == columnMissing:
                    # print(f'[DEBUG] Coluna encontrada: {col}\n[DEBUG] Índice de tal coluna: {colIndex}')
                    foundCol = True
                    break
                colIndex+=1
            if (foundCol == False):
                print('\nErro! Coluna especificada não encontrada\n')
                exit()
            break   #Linha e coluna corretas encontradas
        else:   #Se columnMissing for None então o usuário não especificou a coluna. Será usada a primeira com valores (numéricos) faltando
            print('Função à implementar…')
            exit()
    i+=1

file.seek(0)    #Volta o arquivo para o começo

print('\nIniciando contagem da média…\n')
avg=0.0; i=1; qnt=0
for row in csvFile:
    print('[DEBUG] Índice atual:', i)
    print('[DEBUG]', row)
    if (i==colNamesLine):
        i += 1
        continue

    try:
        if row != []:
            avg += float(row[colIndex].replace(',', '.'))
            qnt += 1
    except ValueError as e:
        # print('[DEBUG] DEU RUIM MOFI! Erro =', e)
        pass

    # print(f'[DEBUG] row[colindex] = {row[colIndex]}, avg = {avg}, qnt = {qnt}')
    i += 1

avg /= qnt

# print(f'[DEBUG] Média final = {avg}')

# print(f'[DEBUG] Filmename - extensão = {fileName[0:-4]}')

print('\nIniciando criação do novo arquivo…\n')

try:
    newFile = open((fileName[0:-4]+'_novo.csv'), 'w+', newline='', encoding='utf-8')
except Exception as e:
    print(f'\nErro, impossível criar novo arquivo: {e}\n')
    exit()

file.seek(0)    #Resetando a leitura do arquivo original…

i=1
for row in csvFile:
    print(f'[DEBUG] row = {row}')
    if(i == colNamesLine):  #Não modificar nada na linha dos nomes…
        # print(f"[DEBUG] ', '.join(map(lambda item: item.replace(',', '.'), row)) = {', '.join(map(lambda item: item.replace(',', '.'), row))}")
        newFile.write(', '.join(map(lambda item: item.replace(',', '.'), row)) + '\n')
        i += 1
        continue
    newRow = row
    if (row != []):
        if (row[colIndex] == missingChar):
            newRow[colIndex] = str(avg).replace(',','.')
        # print(f"[DEBUG] ', '.join(map(lambda item: item.replace(',', '.'), newRow)) = {', '.join(map(lambda item: item.replace(',', '.'), newRow))}")
        newFile.write(', '.join(map(lambda item: item.replace(',', '.'), newRow)) + '\n')

    i += 1

file.close()
newFile.close()
print('\nFinalizando programa...\n')