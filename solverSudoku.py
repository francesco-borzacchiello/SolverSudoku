from solver import *
from sudoku import *

class SolverToClassicSudoku(Solver):
    def __init__(self, sudoku : ClassicSudoku):
        self.sudoku = sudoku
        self.__stall = False
        self.__count_inserted = 0
    
    def solve(self):
        while not self.sudoku.is_solved() and not self.__stall:
            self.__start_to_solve()
            print(self.sudoku)
            input("press enter")
        if self.__stall:
            print("a stall has occurred")

    def __start_to_solve(self):
        for row in range(self.sudoku.values_for_side_of_a_sudoku()):
            for column in range(self.sudoku.values_for_side_of_a_sudoku()):
                self.__count_inserted += int(self.__try_to_solve_the_cell(row, column))
        self.__check_if_a_stall_has_occurred()

    # returns True if it adds value in the sudoku, otherwise False 
    def __try_to_solve_the_cell(self, row : int, column : int) -> bool:
        if self.sudoku.cell_has_only_one_candidate(row, column):
            return self.sudoku.confirm_candidate(row, column)
        return False
        
    def __check_if_a_stall_has_occurred(self):
        self.__stall = self.__count_inserted == 0
        self.__count_inserted = 0

    def get_solution(self) -> ClassicSudoku:
        pass