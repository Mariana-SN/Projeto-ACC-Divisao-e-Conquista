def zeros(n):
    return [[0 for _ in range(n)] for _ in range(n)]

def traditional_matrix_mult(A, B):
    r = len(A)
    m = len(A[0])
    c = len(B[0])

    print()
    print("R: ", r)
    print("M: ", m)
    print("C: ", c)

    C = [[0 for _ in range(c)] for _ in range(r)]
    for i in range(r):
        for k in range(m):
            for j in range(c):
                C[i][j] += A[i][k] * B[k][j]
    return C

if __name__ == "__main__":
    A = [[1, 2, 3], [4, 5, 6]]  # Matriz 2x3
    B = [[7, 8], [9, 10], [11, 12]]  # Matriz 3x2

    traditional_result = traditional_matrix_mult(A, B)
    print("Traditional Matrix Multiplication Result:\n", traditional_result)