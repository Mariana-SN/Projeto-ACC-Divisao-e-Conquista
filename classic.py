def zeros(n):
    return [[0 for _ in range(n)] for _ in range(n)]

def traditional_matrix_mult(A, B):
    r = len(A)
    m = len(A[0])
    c = len(B[0])
    
    print()
    print("Linhas: ", r)
    print("Meio: ", m)
    print("Colunas: ", c)


    C = [[0 for _ in range(c)] for _ in range(r)]
    for i in range(r):
        for k in range(m):
            for j in range(c):
                C[i][j] += A[i][k] * B[k][j]
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

def multiply_traditional(A, B):
    validate_multiplicable(A, B)
    return traditional_matrix_mult(A, B)

if __name__ == "__main__":
    A = [[1, 2, 3], [4, 5, 6]]  # Matriz 2x3
    B = [[7, 8], [9, 10], [11, 12]]  # Matriz 3x2

    traditional_result = multiply_traditional(A, B)
    print("Traditional Matrix Multiplication Result:\n", traditional_result)