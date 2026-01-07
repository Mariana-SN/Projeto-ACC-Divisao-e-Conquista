from time import perf_counter

STRASSEN_RECURSIVE_CALLS = 0
STRASSEN_SPLIT_JOIN_TIME = 0.0

def zeros(n):
    return [[0 for _ in range(n)] for _ in range(n)]

def add(A, B):
    n = len(A)
    C = zeros(n)
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] + B[i][j]
    return C

def sub(A, B):
    n = len(A)
    C = zeros(n)
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] - B[i][j]
    return C

def split(matrix):
    n = len(matrix)
    mid = n // 2
    A11 = [row[:mid] for row in matrix[:mid]]
    A12 = [row[mid:] for row in matrix[:mid]]
    A21 = [row[:mid] for row in matrix[mid:]]
    A22 = [row[mid:] for row in matrix[mid:]]
    return A11, A12, A21, A22

def join(C11, C12, C21, C22):
    top = [a + b for a, b in zip(C11, C12)]
    bottom = [a + b for a, b in zip(C21, C22)]
    return top + bottom

def strassen_matrix_mult(A, B):
    global STRASSEN_RECURSIVE_CALLS
    STRASSEN_RECURSIVE_CALLS += 1

    n = len(A)
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    global STRASSEN_SPLIT_JOIN_TIME
    t0 = perf_counter()
    A11, A12, A21, A22 = split(A)
    B11, B12, B21, B22 = split(B)
    STRASSEN_SPLIT_JOIN_TIME += (perf_counter() - t0)

    M1 = strassen_matrix_mult(add(A11, A22), add(B11, B22))
    M2 = strassen_matrix_mult(add(A21, A22), B11)
    M3 = strassen_matrix_mult(A11, sub(B12, B22))
    M4 = strassen_matrix_mult(A22, sub(B21, B11))
    M5 = strassen_matrix_mult(add(A11, A12), B22)
    M6 = strassen_matrix_mult(sub(A21, A11), add(B11, B12))
    M7 = strassen_matrix_mult(sub(A12, A22), add(B21, B22))

    C11 = add(sub(add(M1, M4), M5), M7)
    C12 = add(M3, M5)
    C21 = add(M2, M4)
    C22 = add(sub(add(M1, M3), M2), M6)

    t1 = perf_counter()
    C = join(C11, C12, C21, C22)
    STRASSEN_SPLIT_JOIN_TIME += (perf_counter() - t1)

    return C

def shape(M):
    if not M:
        return 0, 0
    row_len = len(M[0])
    if any(len(row) != row_len for row in M):
        return len(M), None
    return len(M), row_len

def validate_multiplicable(A, B):
    ar, ac = shape(A)
    br, bc = shape(B)
    if ac is None or bc is None:
        raise ValueError("Matriz com linhas de comprimentos diferentes.")
    if ac != br:
        raise ValueError(f"Dimensões incompatíveis: A é {ar}x{ac}, B é {br}x{bc}.")

def next_pow2(x):
    p = 1
    while p < x:
        p <<= 1
    return p

def pad_matrix(M, rows, cols):
    padded = [row + [0] * (cols - len(row)) for row in M]
    for _ in range(rows - len(M)):
        padded.append([0] * cols)
    return padded

def unpad_matrix(M, rows, cols):
    return [row[:cols] for row in M[:rows]]

def multiply_strassen(A, B):
    validate_multiplicable(A, B)
    ar, ac = shape(A)
    br, bc = shape(B)
    size = next_pow2(max(ar, ac, bc))
    A_pad = pad_matrix(A, size, size)
    B_pad = pad_matrix(B, size, size)


    C_pad = strassen_matrix_mult(A_pad, B_pad)
    return unpad_matrix(C_pad, ar, bc)

def reset_strassen_stats():
    global STRASSEN_RECURSIVE_CALLS, STRASSEN_SPLIT_JOIN_TIME
    STRASSEN_RECURSIVE_CALLS = 0
    STRASSEN_SPLIT_JOIN_TIME = 0.0

def get_strassen_stats():
    return STRASSEN_RECURSIVE_CALLS, STRASSEN_SPLIT_JOIN_TIME


if __name__ == "__main__":
    A = [[1, 2, 3], [4, 5, 6]]  # Matriz 2x3
    B = [[7, 8], [9, 10], [11, 12]]  # Matriz 3x2

    reset_strassen_stats()
    strassen_result = multiply_strassen(A, B)
    calls, split_join = get_strassen_stats()

    print("\nResultado da multiplicação de matrizes pelo Algoritmo de Strassen:\n", strassen_result)
    print(f"\nEstatísticas: chamadas_recursivas={calls}, tempo_split_join_segundos={split_join:.6f}")
    print()