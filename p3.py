import time
import threading
import os

def read_from_file(file_name):
    matrix = []
    with open(file_name, 'r') as arquivo:
        size = arquivo.readline().split()
        row = int(size[0])
        for _ in range(row):
            row = [float(num) for num in arquivo.readline().split()]  
            matrix.append(row)
    return matrix

def check_compatibility(a,b):
    if a!=b:
        print("Matrizes incompatíveis para multiplicação")
        return False
    else:
        return True

def partial_multiplication(result,m1, m2, r0, rn, c0, cn):
    for i in range(r0,rn):
        for j in range(c0, cn):
            result[i][j] = 0
            for k in range (len(m1[0])):
                result[i][j] += m1[i][k] * m2[k][j]



def threading_multiplication(m1,m2,num_threads):
    m1_r = len(m1)
    m1_c = len(m1[0])
    m2_r = len(m2)
    m2_c = len(m2[0])
    
    check_compatibility(m1_c,m2_r)

    result = [[0 for _ in range(m2_c)] for _ in range(m1_r)]

    threads = []
    rows_per_thread = m1_r // num_threads

    for i in range(num_threads):
        r0 = i * rows_per_thread
        rn = r0 + rows_per_thread if i != num_threads -1 else m1_r
        thread = threading.Thread(target=partial_multiplication,args=(result,m1,m2,r0,rn,0,m2_c))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return result


def main():

    m1 = read_from_file('4_int.txt')
    m2 = read_from_file('4_int.txt')

    cores = os.cpu_count()

    threads = cores * 2

    start = time.time()

    result = threading_multiplication(m1,m2,threads)
    end = time.time()
    full_time = end - start

    with open('resultado_P3.txt', 'w') as arquivo_saida:
        arquivo_saida.write("Variacao do programa: P3\n")
        arquivo_saida.write("Numero de Cores: {}\n".format(cores))
        arquivo_saida.write("Numero de threads: {}\n".format(threads))
        arquivo_saida.write("Numero de linhas da matriz: {}\n".format(len(result)))
        arquivo_saida.write("Numero de colunas da matriz: {}\n".format(len(result[0])))
        arquivo_saida.write("Tempo de processamento com threads: {:.10f}\n".format(full_time))
        arquivo_saida.write("\n")

        for linha in result:
            arquivo_saida.write(" ".join(map(str, linha)) + "\n")

    print("Dobro de Cores gravado em resultado_P3.txt")


main()