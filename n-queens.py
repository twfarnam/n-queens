#! /usr/bin/env python3

import time


# https://en.wikipedia.org/wiki/Backtracking
def backtrack(nqueens, candidate):
    if reject(nqueens, candidate): return
    if accept(nqueens, candidate): yield candidate
    for extension in extend(nqueens, candidate):
        yield from backtrack(nqueens, extension)


def reject(nqueens, candidate):
    n = len(candidate)
    # no collisions in rows and columns, respectively
    for i in range(n):
        if sum(candidate[i]) > 1: return True
        if sum(row[i] for row in candidate) > 1: return True
    if diagonal_conflict(candidate): return True
    return False


def accept(nqueens, candidate):
    n = len(candidate)
    if n != nqueens: return False
    # rows and columns, respectively, should all have one and only one queen
    for i in range(n):
        if sum(candidate[i]) != 1: return False
        if sum(row[i] for row in candidate) != 1: return False
    if diagonal_conflict(candidate): return False
    return True


def diagonal_conflict(candidate):
    n = len(candidate)
    # left-to-right diagonals
    for i in range(-n+2, n-1):
        start = max(-i,0)
        end = min(n-i, n)
        if sum(candidate[j][j+i] for j in range(start, end)) > 1:
            return True
    # right-to-left diagonals
    for i in range(1, 2*n-2):
        start = max(0,i-n+1)
        end = min(n, i+1)
        if sum(candidate[j][i-j] for j in range(start, end)) > 1:
            return True
    return False


def extend(nqueens, candidate):
    if len(candidate) >= nqueens: return
    n = len(candidate) + 1
    blank = (0, ) * n
    for i in range(n+1):
        new_row = blank if i >= n else blank[:i] + (1,) + blank[i+1:]
        for j in range(n):
            rows = ()
            for row_i in range(len(candidate)):
                new_value = 1 if row_i == j else 0 
                rows += ( candidate[row_i] + ( new_value, ), )
            yield rows + ( new_row, )


# https://en.wikipedia.org/wiki/Eight_queens_puzzle#Counting_solutions
# http://www.ic-net.or.jp/home/takaken/e/queen/
answers = [ 0, 1, 0, 0, 2, 10, 4, 40, 92, 352, 724, 2680, 14200, 73712,
        365596, 2279184, 14772512, 95815104, 666090624, 4968057848,
        39029188884, 314666222712, ]

print("    N        correct       computed       time")
print("=====   ============   ============   ========")

for n, answer in enumerate(answers):
    ts = time.time()
    computed = list(backtrack(n, ( )))
    string = "{:>5} {:>14} {:>14} {:8.2f} s"
    print(string.format(n, answer, len(computed), time.time() - ts))


