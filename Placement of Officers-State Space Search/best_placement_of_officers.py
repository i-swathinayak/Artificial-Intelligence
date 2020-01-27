#!/usr/bin/python

import numpy as numpy
import time
from functools import wraps

maxvalue = -1
rows = {}
columns = {}
diag = {}
cdiag = {}

global arrBT


def solveBT():
    btgrid = numpy.zeros((n, n))
    solvebt(btgrid, 0, o, 0, rows, columns, diag, cdiag)
    return maxvalue


def checkfeasible(self, row, column):
    if row in rows and rows[row] > 0:
        return False
    if column in columns and columns[column] > 0:
        return False
    if row - column in diag and diag[row - column] > 0:
        return False
    if row + column in cdiag and cdiag[row + column] > 0:
        return False
    return True


def solvebt(btgrid, col, officers, score, rows, columns, diag, cdiag):
    global maxvalue
    if (n - col < officers):
        return
    if ((col == n and officers == 0) or officers == 0):
        maxvalue = max(maxvalue, score)
        return
    if (col == n):
        return
    while col < n:
        for row in range(n):
            if (checkfeasible(btgrid, row, col)):
                btgrid[row][col] = 1
                rows[row] = True
                columns[col] = True
                diag[row - col] = True
                cdiag[row + col] = True
                solvebt(btgrid, col + 1, officers - 1, score + arrBT[row][col], rows, columns, diag, cdiag)
                btgrid[row][col] = 0
                rows[row] = False
                columns[col] = False
                diag[row - col] = False
                cdiag[row + col] = False
        col = col + 1


# check for conflicting officers
def conflictCheck(grid, n, row, col):
    for i in range(n):
        if grid[row][i] == 1 or grid[i][col] == 1:
            return False

    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if grid[i][j] == 1:
            return False

    for i, j in zip(range(row, n, 1), range(col, -1, -1)):
        if grid[i][j] == 1:
            return False

    for i, j in zip(range(row, -1, -1), range(col, n, 1)):
        if grid[i][j] == 1:
            return False

    for i, j in zip(range(row, n, 1), range(col, n, 1)):
        if grid[i][j] == 1:
            return False

    return True


# check for cell with maximum activity points
def maxPoints(M):
    largest = -1
    row = -1
    col = -1

    for r, row in enumerate(M):
        for c, num in enumerate(row):
            if num > largest or largest is None:
                largest = num
                row1 = r
                col = c
    return (largest, row1, col)


# bcheck
global defp
defp = 0


def bsolve(c, left, right, comp):
    global defp
    if comp == o:
        # solcount+=1
        total = 0
        for a, b in enumerate(sboard):
            total = total + bmatrix[a][b]
        defp = max(defp, total)
        return

    f_pos = defvals & ~(c | left | right)
    while f_pos != 0:
        c_pos = -f_pos & f_pos
        sboard.append((c_pos & -c_pos).bit_length() - 1)
        f_pos ^= c_pos
        bsolve((c | c_pos), (left | c_pos) >> 1, (right | c_pos) << 1, comp + 1)
        sboard.pop()

    return defp


# read the city dimensions, number of police officers and scooters from the input file
with open("input.txt") as finput:
    grid = [next(finput).strip() for x in range(3)]
# print grid

n, o, s = int(grid[0]), int(grid[1]), int(grid[2])

# print "The city dimensions are " + str(n) + "x" + str(n)
# print "The number of police officers are " + str(o)
# print "The number of scooters are " + str(s)

# read the scooter positions from the input file and store them in a list of lists
lists = [[] for _ in range(s)]

j = 0

with open("input.txt", "r") as finput:
    for i in range(s):
        for l, line in enumerate(finput):
            if l < 3 and i == 0:
                e = 1
            else:
                if j < 12:
                    j += 1
                    position = line.strip()
                    lists[i].append((position))
                else:
                    if i != s - 1:
                        position = line.strip()
                        lists[i + 1].append((position))
                        j = 1
                        break

# print "The scooter positions at different time slots are as below:"
# print lists

# record the number of scooter collisions in a matrix
w, h = n, n

Matrix = [[0 for x in range(w)] for y in range(h)]

for i in range(s):
    for j in range(12):
        a = lists[i][j].split(",")
        # print a
        Matrix[int(a[0])][int(a[1])] += 1

bboard = [[0 for x in range(n)] for y in range(n)]
# global solcount=0
defvals = (1 << n) - 1
sboard = []
bmatrix = map(list, Matrix)

# if number of police officer is 1
if o == 1:
    AP, r, c = maxPoints(Matrix)
    # print "Activity Points:" + str(AP)
    f = open("output.txt", "w+")
    f.write(str(AP) + '\n')
    f.close()
    exit()

Compare = [0 for x in range(1, n * n, 1)]


# print Compare

def placeOfficer():
    for i in range(1, n * n, 1):
        # print "Value of i is " +  str(i)
        Mnew = list(map(list, Matrix))
        M = [[0 for x in range(w)] for y in range(h)]

        j = 0
        k = 0
        AP = 0

        if i != 1:
            for x in range(1, i, 1):
                a, b, c = maxPoints(Mnew)
                Mnew[b][c] = -4
            APlocal, r, c = maxPoints(Mnew)
            Mnew = list(map(list, Matrix))
            Mnew[r][c] = -1
            M[r][c] = 1
            AP += APlocal
            k += 1
            j += 1

        while k < o and j < (n * n):
            APlocal, r, c = maxPoints(Mnew)
            if (conflictCheck(M, n, r, c)):
                M[r][c] = 1
                Mnew[r][c] = -1
                AP += APlocal
                k += 1
            else:
                Mnew[r][c] = -2

            j += 1

        if k == o:
            Compare[i - 1] = AP

        # print AP
        # print M


if n == o:
    acpoints = str(bsolve(0, 0, 0, 0))
elif (n <= 11):
    # N=n
    arrBT = list(map(list, Matrix))
    acpoints = str(solveBT())
else:
    placeOfficer()
    acpoints = str(max(Compare))

f = open("output.txt", "w+")
f.write(acpoints + '\n')
f.close()
print("Activity Points: " + str(acpoints))
