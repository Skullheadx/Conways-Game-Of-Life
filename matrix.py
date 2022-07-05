from fractions import Fraction
# [[1, 2, 3],
#  [4, 5, 6],
#  [7, 8, 9]]


class Matrix:

    def __init__(self, info=None):
        if info is None:
            info = [[0]]  # 1x1 matrix
        self.value = info
        self.rows = len(self.value)
        self.cols = len(self.value[0])

    def get_determinant(self):
        if not (self.rows == self.cols == 2):
            raise Exception("Too lazy to code other than 2x2 matrices :P")
        return self.value[0][0] * self.value[-1][-1] - self.value[0][-1] * self.value[-1][0]

    def get_adjugate(self):
        if not (self.rows == self.cols == 2):
            raise Exception("Too lazy to code other than 2x2 matrices :P")
        out = [[self.value[-1][-1], -self.value[0][1]],
               [-self.value[1][0], self.value[0][0]]]
        return Matrix(out)

    def get_inverse(self, fraction=False):
        return MultiplyScalar(1 / self.get_determinant(), self.get_adjugate(), fraction)

def DotProduct(lis1, lis2):
    dot_product = 0
    for ele1, ele2 in zip(lis1, lis2):
        dot_product += ele1 * ele2
    return dot_product

def MultiplyMatrices(matrix1, matrix2):
    if matrix1.cols != matrix2.rows:
        raise ValueError(f"Multiplication is not defined between these two matrices: {matrix1} and {matrix2}")
    output_matrix = []
    for row in range(matrix1.rows):
        output_matrix.append([])
        for col in range(matrix2.cols):
            r = matrix1.value[row]
            c = []
            for i in range(matrix2.rows):
                c.append(matrix2.value[i][col])
            output_matrix[row].append(DotProduct(r, c))


    return Matrix(output_matrix)


def MultiplyScalar(value, matrix, fraction=False):
    out = [[] for _ in range(matrix.rows)]
    for i, row in enumerate(matrix.value):
        for col in row:
            if fraction:
                out[i].append(str(Fraction.from_float(col / (1/value)).limit_denominator()))
            else:
                out[i].append(col * value)
    return Matrix(out)

def get_matrix_from_input():
    # rows = int(input("Enter the number of rows: "))
    # cols = int(input("Enter the number of cols: "))
    print("Enter the values of the matrix with spaces in between entries and an empty line to finish.")
    out = []
    row = 0
    while True:
        user_input = input(f"Enter row {row+1}: ")
        if user_input == "":
            break
        else:
            out.append(list(map(float, user_input.split())))
            row += 1

    return Matrix(out)

def print_matrix(matrix):
    for row in matrix.value:
        print(*row)

# print("Matrix Calculator")
# matrix1 = get_matrix_from_input()
# matrix2 = get_matrix_from_input()
#
# print_matrix(MultiplyMatrices(matrix1.get_inverse(), matrix2))
# print_matrix(MultiplyMatrices(matrix1, matrix2))
# print(matrix1.get_determinant())
# print_matrix(matrix1.get_inverse(True))



