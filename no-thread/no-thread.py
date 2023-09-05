import numpy as np

def read_file(file):
    with open(file, 'r') as f:
        size = list(map(int, f.readline().split()))
        matrix = []
        for i in range (size[0]):
            line = list(map(float,f.readline().split()))
            matrix.append(line)
        print(size)
        print(matrix)
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
    #Por algum motivo, simplesmente só lê se colocar o Path completo
    matrix1 = read_file("../matrizes/4_int.txt")
    matrix2 = read_file("../matrizes/4_int.txt")

    if len(matrix1[0]) != len(matrix2):
        print('Não podem ser multiplicadas')
    else:
        result = multiply_matrix(matrix1,matrix2)
        write_file(result,"./resultado.txt")
        print("Multiplicado com sucesso")