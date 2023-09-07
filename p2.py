import numpy as np
import multiprocessing
import time
import os

def load_matrix(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        size = tuple(map(int, lines[0].strip().split()))
        matrix_data = [list(map(float, line.strip().split())) for line in lines[1:]]
        return np.array(matrix_data), size

def compute_partial_product(A, B, start_row, end_row, start_col, end_col):
    return np.dot(A[start_row:end_row, :], B[:, start_col:end_col])

def distribute_workload(rows, cols, num_processes):
    workload = []
    step_row = rows // num_processes
    step_col = cols // num_processes

    for i in range(num_processes):
        start_row = i * step_row
        end_row = start_row + step_row if i < num_processes - 1 else rows
        for j in range(num_processes):
            start_col = j * step_col
            end_col = start_col + step_col if j < num_processes - 1 else cols
            workload.append((start_row, end_row, start_col, end_col))
    
    return workload

def write_matrix_to_file(filename, matrix):
    with open(filename, 'w') as file:
        rows, cols = matrix.shape
        file.write(f"{rows} {cols}\n")
        for row in matrix:
            file.write(" ".join(map(str, row)) + "\n")

def main():
    A_filename = "4_int.txt"
    B_filename = "4_int.txt"
    result_filename = "./resultado.txt"

    A, (A_rows, A_cols) = load_matrix(A_filename)
    B, (B_rows, B_cols) = load_matrix(B_filename)

    if A_cols != B_rows:
        print("Matriz incompatível")
        return

    num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(num_processes)

    partial_results = []
    workload = distribute_workload(A_rows, B_cols, num_processes)
    inicio = time.time()
    for work in workload:
        partial_result = pool.apply_async(compute_partial_product, args=(A, B, *work))
        partial_results.append(partial_result)

    pool.close()
    pool.join()

    result = np.zeros((A_rows, B_cols))

    for i, partial_result in enumerate(partial_results):
        start_row, end_row, start_col, end_col = workload[i]
        result[start_row:end_row, start_col:end_col] = partial_result.get()


    
    fim = time.time()
    tempofinal =  fim - inicio


    with open('resultado_P2.txt', 'w') as arquivo_saida:
        arquivo_saida.write("Variacao do programa: P2 \n")
        arquivo_saida.write("Numero de Cores: {}\n".format(num_processes))
        arquivo_saida.write("Numero de computadores Remotos: 0 \n")
        arquivo_saida.write("Numero de linhas da matriz: {}\n".format(len(result)))
        arquivo_saida.write("Numero de colunas da matriz: {}\n".format(len(result[0])))
        arquivo_saida.write("Tempo de processamento: {:.10f}\n".format(tempofinal))
        arquivo_saida.write("\n")
        for row in result:
            arquivo_saida.write(' '.join(map(str, row)) + '\n')

    print(f"Salvo em: {result_filename}.")

    print(f"Tempo de processamento: {tempofinal} segundos")

if __name__ == "__main__":
    main()
