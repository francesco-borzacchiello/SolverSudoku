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
            self.__check_if_a_stall_has_occurred()
            print(self.sudoku)
            input("press enter")
        if self.__stall:
            print("a stall has occurred")

    def __start_to_solve(self):
        self.__find_cell_with_one_candidate()
        self.__find_row_with_candidate_with_only_one_occurence_and_insert_it()
        

    def __find_cell_with_one_candidate(self):
        for row in range(self.sudoku.values_for_side_of_a_sudoku()):
            for column in range(self.sudoku.values_for_side_of_a_sudoku()):
                self.__count_inserted += int(self.__try_to_solve_the_cell(row, column))

    def __find_row_with_candidate_with_only_one_occurence_and_insert_it(self):
        for row in range(self.sudoku.values_for_side_of_a_sudoku()):
            self.__find_and_insert_candidate_with_only_one_occurence_for_this_row(row)
        
    def __find_and_insert_candidate_with_only_one_occurence_for_this_row(self, row : int):
        for candidate in range(1, self.sudoku.values_for_side_of_a_sudoku() + 1):
            column = self.__find_the_column_in_which_to_insert_value(row, candidate)
            if column >= 0:
                self.__count_inserted += 1
                self.sudoku.insert_value_in_cell(row, column, candidate)

    # If in the row there is a candidate with only one occurrence, 
    # the column in which it can be inserted is returned, otherwise -1
    def __find_the_column_in_which_to_insert_value(self, row : int, candidate : int) -> int:
        reference_to_the_column = -1
        for column in range(self.sudoku.values_for_side_of_a_sudoku()):
            if reference_to_the_column < 0 and self.sudoku.cell_has_candidate(row, column, candidate):
                reference_to_the_column = column
            elif reference_to_the_column >= 0 and self.sudoku.cell_has_candidate(row, column, candidate):
                return -1
        return reference_to_the_column    

    # returns True if it adds value in the sudoku, otherwise False 
    def __try_to_solve_the_cell(self, row : int, column : int) -> bool:
        if self.sudoku.cell_has_only_one_candidate(row, column):
            self.sudoku.confirm_candidate(row, column)
            return True
        return False
        
    def __check_if_a_stall_has_occurred(self):
        self.__stall = self.__count_inserted == 0
        self.__count_inserted = 0

    def get_solution(self) -> ClassicSudoku:
        pass