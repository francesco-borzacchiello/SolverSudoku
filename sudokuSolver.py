from solver import *
from sudoku import *

class ClassicSudokuSolver(Solver):
    def __init__(self, sudoku : ClassicSudoku):
        self.sudoku = sudoku
        self.__stall = False
        self.__count_inserted = 0
    
    def solve(self):
        print(self.sudoku)
        while not self.sudoku.is_solved() and not self.__stall:
            self.__start_to_solve()
            self.__check_if_a_stall_has_occurred()
            print(self.sudoku)
            # input("press enter")
        if self.__stall:
            print("a stall has occurred")

    def __start_to_solve(self):
        self.__find_cell_with_one_candidate()
        self.__find_row_with_candidate_with_only_one_occurrence_and_insert_it()
        self.__find_column_with_candidate_with_only_one_occurrence_and_insert_it()
        
    def __find_cell_with_one_candidate(self):
        for row in range(self.sudoku.values_for_side_of_a_sudoku()):
            for column in range(self.sudoku.values_for_side_of_a_sudoku()):
                self.__count_inserted += int(self.__try_to_solve_the_cell(IndicesOfCell(row, column)))

    def __find_row_with_candidate_with_only_one_occurrence_and_insert_it(self):
        for row in range(self.sudoku.values_for_side_of_a_sudoku()):
            self.__find_and_insert_candidate_with_only_one_occurence_for_this_row(row)
        
    def __find_and_insert_candidate_with_only_one_occurence_for_this_row(self, row : int):
        for candidate in range(1, self.sudoku.values_for_side_of_a_sudoku() + 1):
            column = self.__find_the_column_in_which_to_insert_value(row, candidate)
            self.__count_inserted += int(self.sudoku.insert_value_in_cell(IndicesOfCell(row, column), candidate))

    def __find_the_column_in_which_to_insert_value(self, row : int, candidate : int) -> tuple:
        references_to_the_columns = []
        for column in range(self.sudoku.values_for_side_of_a_sudoku()):
            self.__if_cell_has_this_candidate_add_it_to_the_list_of_references(row, column, candidate, references_to_the_columns)
        return references_to_the_columns[0][1] if len(references_to_the_columns) == 1 else None

    def __if_cell_has_this_candidate_add_it_to_the_list_of_references(self, row : int, column : int, 
                                                                        candidate : int, references : list):
        if self.sudoku.cell_has_candidate(IndicesOfCell(row, column), candidate):
                references.append((row, column))                                                                

    def __find_column_with_candidate_with_only_one_occurrence_and_insert_it(self):
        for column in range(self.sudoku.values_for_side_of_a_sudoku()):
            self.__find_and_insert_candidate_with_only_one_occurence_for_this_column(column)

    def __find_and_insert_candidate_with_only_one_occurence_for_this_column(self, column : int):
        for candidate in range(1, self.sudoku.values_for_side_of_a_sudoku() + 1):
            row = self.__find_the_row_in_which_to_insert_value(column, candidate)
            self.__count_inserted += int(self.sudoku.insert_value_in_cell(IndicesOfCell(row, column), candidate))

    def __find_the_row_in_which_to_insert_value(self, column : int, candidate : int) -> int:
        references_to_the_rows = []
        for row in range(self.sudoku.values_for_side_of_a_sudoku()):
            self.__if_cell_has_this_candidate_add_it_to_the_list_of_references(row, column, candidate, references_to_the_rows)
        return references_to_the_rows[0][0] if len(references_to_the_rows) == 1 else None


    # returns True if it adds value in the sudoku, otherwise False 
    def __try_to_solve_the_cell(self, cell : IndicesOfCell) -> bool:
        if self.sudoku.cell_has_only_one_candidate(cell):
            self.sudoku.confirm_candidate(cell)
            return True
        return False
        
    def __check_if_a_stall_has_occurred(self):
        self.__stall = self.__count_inserted == 0
        self.__count_inserted = 0

    def get_solution(self) -> ClassicSudoku:
        return self.sudoku