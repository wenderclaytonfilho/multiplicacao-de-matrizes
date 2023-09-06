import threading
import os
import numpy as np
import time


def read_file(file):
    with open(file, 'r') as f:
        size = list(map(int, f.readline().split()))
        matrix = []
        for i in range(size[0]):
            line = list(map(float, f.readline().split()))
            matrix.append(line)
        return matrix


def write_file(matrix, file):
    with open(file, 'w') as f:
        f.write(f"{len(matrix)} {len(matrix[0])}\n")
        for row in matrix:
            f.write(' '.join(map(str, row)) + '\n')


def multiply_matrix_part(matrix1, matrix2, start_row, end_row, result):
    for i in range(start_row, end_row):
        for j in range(len(matrix2[0])):
            result[i][j] = sum(matrix1[i][k] * matrix2[k][j]
                               for k in range(len(matrix2)))


def multiply_matrix(matrix1, matrix2, num_threads):
    rows = len(matrix1)
    cols = len(matrix2[0])
    result = [[0 for _ in range(cols)] for _ in range(rows)]

    chunk_size = rows // num_threads
    threads = []

    for i in range(0, rows, chunk_size):
        start_row = i
        end_row = min(i + chunk_size, rows)
        thread = threading.Thread(target=multiply_matrix_part, args=(
            matrix1, matrix2, start_row, end_row, result))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return result


if __name__ == "__main__":
    matrix1 = read_file("4_int.txt")
    matrix2 = read_file("4_int.txt")

    if len(matrix1[0]) != len(matrix2):
        print('Não podem ser multiplicadas, dimensões incompatíveis')
    else:
        num_cores = os.cpu_count()
        num_threads = num_cores // 2

        inicio = time.time()
        result = multiply_matrix(matrix1, matrix2, num_threads)
        fim = time.time()
        tempofinal = fim - inicio

        with open('resultado.txt', 'w') as arquivo_saida:
            arquivo_saida.write("Variacao do programa: P4 \n")
            arquivo_saida.write("Numero de Cores: {}\n".format(num_cores))
            arquivo_saida.write("Numero de computadores Remotos: \n")
            arquivo_saida.write(
                "Numero de linhas da matriz: {}\n".format(len(result)))
            arquivo_saida.write(
                "Numero de colunas da matriz: {}\n".format(len(result[0])))
            arquivo_saida.write(
                "Tempo de processamento: {:.10f}\n".format(tempofinal))
            arquivo_saida.write("\n")
            for row in result:
                arquivo_saida.write(' '.join(map(str, row)) + '\n')

        print("Multiplicado com sucesso")
