import numpy as np
from itertools import chain
from collections import Counter

def _fmt_range(length, start):
    if length == 1:
        return str(start)
    elif length == 2:
        return str(start) + "," + str(start + 1)
    else:
        return str(start) + "-" + str(start + length - 1)

class Cell:
    def __init__(self, row, col, min=1, max=9):
        self.row = row
        self.col = col
        self.value = None
        self.possible = set(range(min, max + 1))

    def __str__(self):
        if self.value != None:
            return str(self.value)
        else:
            # format self.possible using ranges, i.e. 1-9
            possibles = sorted(self.possible)
            ret = "{"
            start = possibles[0]
            length = 1
            for j in possibles[1:]:
                if j == start + length:
                    length += 1
                else:
                    ret += _fmt_range(length, start)
                    start = j
                    length = 1
                    ret += ","
            ret += _fmt_range(length, start)
            ret += "}"
            return ret
        
    def __rep__(self):
        return f"({self.col},{self.row})->str(self)"
        
    def removeall(self, values: set) -> set:
        removed = self.possible & values
        self.possible -= removed
        if len(self.possible) == 0:
            raise Exception(f"No possible values left in cell {self.col}, {self.row} removing {removed}")
        elif len(self.possible) == 1:
            self.set(self.possible.pop())
        return removed
    
    def remove(self, value) -> bool:
        return len(self.removeall({value})) > 0
    
    def solved(self) -> bool:
        return self.value != None
    
    def set(self, value):
        self.value = value
        self.possible = {value}


class Sudoku:
    def __init__(self, block_size=3, blocks=3):
        self.block_size = block_size
        self.blocks = blocks
        self.grid = []
        for i in range(self.size()):
            row = []
            for j in range(self.size()):
                row.append(Cell(i+1, j+1, 1, self.size()))
            self.grid.append(row)

    def size(self):
        return self.block_size * self.blocks
    
    def pprint_grid(self):
        # collect strings
        strgrid = []
        for row in self.grid:
            strrow = []
            for cell in row:
                strcell = str(cell)
                strrow.append(strcell)
            strgrid.append(strrow)

        # collect necessary len per column
        maxlen = [0] * self.size()
        for r, c in np.ndindex(self.size(), self.size()):
            if len(strgrid[r][c]) > maxlen[c]:
                maxlen[c] = len(strgrid[r][c])
        
        hsep = ""
        for ridx, length in enumerate(maxlen):
            if ridx % self.block_size == 0:
                hsep += "*-"
            hsep += "-" * (length+1)
        hsep += "*"

        # print with | around it
        for ridx, row in enumerate(strgrid):
            if ridx % self.block_size == 0:
                print(hsep)
            for cidx, cell in enumerate(row):
                if cidx % self.block_size == 0:
                   print("| ", end="")
                print(cell.center(maxlen[cidx]), end=" ")
            print("|")
        print(hsep)
        
    def extract_row(self, row):
        return self.grid[row-1]
    
    def extract_column(self, column):
        return [row[column-1] for row in self.grid]
    
    def extract_block(self, br, bc):
        r = br * self.block_size
        c = bc * self.block_size
        ret = []
        for i, j in np.ndindex(self.block_size, self.block_size):
            ret.append(self.grid[r + i][c + j])
        return ret
    
    def extract_block_of(self, cell):
        return self.extract_block((cell.row-1) // self.block_size, (cell.col-1) // self.block_size)
    
    def affected_of(self, cell):
        return [self.extract_row(cell.row), self.extract_column(cell.col), self.extract_block_of(cell)]

    # self[x, y] = self[col, row] = value
    def __setitem__(self, key, value):
        cell = self.grid[key[1]-1][key[0]-1]
        if (cell.value == value):
            return
        cell.set(value)


class Solver:
    def __init__(self, sudoku: Sudoku):
        self.s = sudoku

    def unsolved_cells(self):
        return [cell for row in self.s.grid for cell in row if cell.value == None]
    
    def issolved(self):
        return len(self.unsolved_cells()) == 0
    
    # returns a set of cells that were changed
    def remove_from(self, cells, value) -> set:
        changed = set()
        for cell in cells:
            if cell.remove(value):
                changed.add(cell)
        return changed
    
    def handle_uniques(self, cells):
        changed = set()
        values = chain.from_iterable(map(lambda x: list(x.possible), cells))
        counter = Counter(values)

        uncells = list(filter(lambda x: not x.solved(), cells))
        for value, count in counter.items():
            if count == 1:
                for cell in uncells:
                    if value in cell.possible:
                        cell.set(value)
                        changed.add(cell)
        return changed


    def _use_group(self, values: set, group: set, cells: set, changed: set):
        if len(values) == len(group):
            for cell in cells - group:
                if cell.removeall(values):
                    changed.add(cell)
            return
        for cell in cells:
            if cell in group or cell.solved():
                continue
            if len(cell.possible - values) <= 1:
                self._use_group(values | cell.possible, group | {cell}, cells, changed)


    def use_groups(self, cell, candidates):
        values = set(cell.possible)
        changed = set()
        candidates = set(filter(lambda x: not x.solved(), candidates)) - {cell}
        self._use_group(values, {cell}, candidates, changed)
        return changed

    def propagate_change(self, cell):
        changed = {cell}
        while len(changed) > 0:
            cell = changed.pop()
            row, col, block = self.s.affected_of(cell)
            if cell.solved():
                changed |= self.remove_from(set(row + col + block) - {cell}, cell.value)
                changed |= self.handle_uniques(row)
                changed |= self.handle_uniques(col)
                changed |= self.handle_uniques(block)
            else:
                changed |= self.use_groups(cell, row)
                changed |= self.use_groups(cell, col)
                changed |= self.use_groups(cell, block)
    
    def update(self, x, y, value):
        self.s[x, y] = value
        try:
            self.propagate_change(self.s.grid[y-1][x-1])
        except Exception as e:
            print("Error:", e)
            self.s.pprint_grid()
            raise e

test_hard = """7 1 7
7 2 1
8 3 4
9 2 2
9 3 5
6 3 1
5 3 3
3 2 7
3 3 2
2 2 9
2 3 6
1 3 8
2 4 4
3 6 9
1 7 1
1 8 9
2 8 5
4 6 5
5 6 7
5 5 4
5 4 1
6 4 3
7 4 8
8 5 5
4 7 4
5 9 2
6 8 7
6 9 9
8 8 6
9 7 9"""

test_veryhard = """1 1 6
3 3 8
5 1 1
6 1 2
6 2 8
6 3 9
8 3 7
9 3 4
1 4 1
1 5 9
1 6 7
2 4 6
5 4 2
5 6 9
7 4 3
9 5 6
3 7 3
4 9 8
5 8 7
6 7 4
7 8 9
8 9 2"""

test_hell = """1 2 7
2 3 5
3 2 2
4 1 4
5 2 6
9 1 6
1 6 3
2 4 2
3 5 5
4 5 7
5 4 1
6 4 9
6 6 8
8 4 4
9 6 9
2 9 7
3 8 3
3 9 4
6 7 1
6 9 2
8 7 9
8 8 8
8 9 3
9 7 4"""
      
def make_interactive(solver):
    print("Interactive sudoku solver")
    while not solver.issolved():
        x, y, v = input("Enter x, y, value: ").split()
        solver.update(int(x), int(y), int(v))
        sudoku.pprint_grid()
    print("Solved!")

def apply_test(solver, data):
    for line in data.split("\n"):
        x, y, v = line.split()
        solver.update(int(x), int(y), int(v))
        print(f"Applied ({x}, {y}) -> {v}")
    solver.s.pprint_grid()

if __name__ == "__main__":
    sudoku = Sudoku()
    solver = Solver(sudoku)
    apply_test(solver, test_hell)
    make_interactive(solver)