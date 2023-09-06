import numpy as np
import time

def read_file(file):
    with open(file, 'r') as f:
        size = list(map(int, f.readline().split()))
        matrix = []
        for i in range (size[0]):
            line = list(map(float,f.readline().split()))
            matrix.append(line)

        return(matrix)

def write_file(matrix,file):
    with open(file, 'w') as f:
        f.write(f"{len(matrix)} {len(matrix[0])}\n")
        for row in matrix:
            f.write(' '.join(map(str, row)) + '\n')

def multiply_matrix(m1, m2):
    matrix1 = np.array(m1)
    matrix2 = np.array(m2)
    result = np.dot(matrix1,matrix2)
    return result.tolist()



if __name__ == "__main__":
    matrix1 = read_file("4_int.txt")
    matrix2 = read_file("4_int.txt")

    if len(matrix1[0]) != len(matrix2):
        print('Não podem ser multiplicadas, dimensões incompatíveis')
    else:

        inicio = time.time()
        fim = time.time()
        tempofinal = inicio - fim

        result = multiply_matrix(matrix1,matrix2)
        
        with open('resultado.txt', 'w') as arquivo_saida:
            arquivo_saida.write("Variacao do programa: P1 \n")
            arquivo_saida.write("Numero de Cores: \n")
            arquivo_saida.write("Numero de computadores Remotos: \n")
            arquivo_saida.write("Numero de linhas da matriz: {}\n".format(len(result)))
            arquivo_saida.write("Numero de colunas da matriz: {}\n".format(len(result[0])))
            arquivo_saida.write("Tempo de processamento: {:.10f}\n".format(tempofinal))
            arquivo_saida.write("\n")
            for row in result:
                arquivo_saida.write(' '.join(map(str, row)) + '\n')

        print("Multiplicado com sucesso")