#Author : Nithin G
#Roll Number: EE24B046

def matrix_multiply(matrix1, matrix2):
    if (matrix1 == []) or (matrix2 == []):
        raise ValueError("Empty matrices cannot be multiplied")
    else:
        r1 = len(matrix1)
        c1 = len(matrix1[0])
        r2 = len(matrix2)
        c2 = len(matrix2[0])
        matrix = [[0 for _ in range(c2)] for _ in range(r1)]
        if (c1 == r2):
            for i in range(r1):
                for j in range(c2):
                    for k in range(r2):
                        matrix[i][j] += matrix1[i][k] * matrix2[k][j]
        else:
            raise ValueError("Incompatible dimensions for multiplication")
    return matrix
