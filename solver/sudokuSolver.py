from solver.solver import *
from puzzle.sudoku import *
from puzzle.cell import *

class ClassicSudokuSolver(Solver):
    def __init__(self, sudoku : ClassicSudoku):
        self.__initialize_the_fields(sudoku)
        self.__calculate_candidates()
    
    def __initialize_the_fields(self, sudoku : ClassicSudoku):
        self.__sudoku = sudoku
        self.__stall = False
        self.__count_inserted = 0

    def __str__(self):
        from utility.printUtility import PrintClassicSudokuBoard
        printer = PrintClassicSudokuBoard(self.__sudoku)
        return printer.print_sudoku_with_candidate(self.__candidates)

    def __calculate_candidates(self):
        self.__candidates =  {}
        iterator = self.__sudoku.get_the_iterator_of_the_indices_of_the_sudoku_cells()
        for cell in iterator:
            self.__if_the_cell_is_empty_calculates_its_candidates(cell)

    def __if_the_cell_is_empty_calculates_its_candidates(self, cell: IndicesOfCell):
        if self.__sudoku.cell_is_empty(cell):
            self.__candidates[cell] = self.__calculate_candidates_for_a_cell(cell)

    def __calculate_candidates_for_a_cell(self, cell: IndicesOfCell) -> list:
        candidates_for_a_cell = []
        for candidate in range(1, self.__sudoku.values_for_side_of_a_sudoku + 1):
            if self.__candidate_is_eligible(cell, candidate):
                candidates_for_a_cell.append(candidate)
        return candidates_for_a_cell

    def __candidate_is_eligible(self, cell : IndicesOfCell, value : int) -> bool:
        return (self.__sudoku.cell_is_empty(cell)
                and self.__sudoku.value_not_in_block(cell, value) 
                and self.__sudoku.value_not_in_row(cell.row, value) 
                and self.__sudoku.value_not_in_column(cell.column, value))
    
    def solve(self):
        while not self.__sudoku.is_solved() and not self.__stall:
            print(self)
            # input("press enter")
            self.__start_to_solve()
            self.__check_if_a_stall_has_occurred()
        if self.__stall:
            print("a stall has occurred")
        else:
            print(self.__sudoku)

    def __start_to_solve(self):
        self.__find_cell_with_one_candidate()
        self.__find_row_with_candidate_with_only_one_occurrence_and_insert_it()
        self.__find_column_with_candidate_with_only_one_occurrence_and_insert_it()
        
    def __find_cell_with_one_candidate(self):
        iterator = self.__sudoku.get_the_iterator_of_the_indices_of_the_sudoku_cells()
        for cell in iterator:
            self.__try_to_solve_the_cell(cell)

    def __find_row_with_candidate_with_only_one_occurrence_and_insert_it(self):
        for row in range(self.__sudoku.values_for_side_of_a_sudoku):
            self.__find_and_insert_candidate_with_only_one_occurence_for_this_row(row)
        
    def __find_and_insert_candidate_with_only_one_occurence_for_this_row(self, row : int):
        for candidate in range(1, self.__sudoku.values_for_side_of_a_sudoku + 1):
            column = self.__find_the_column_in_which_to_insert_value(row, candidate)
            self.__insert_the_value_and_update_the_candidates(IndicesOfCell(row, column), candidate)
            
    def __find_the_column_in_which_to_insert_value(self, row : int, candidate : int) -> tuple:
        references_to_the_columns = []
        for column in range(self.__sudoku.values_for_side_of_a_sudoku):
            self.__if_cell_has_this_candidate_add_it_to_the_list_of_references(IndicesOfCell(row, column),
                                                                                candidate, references_to_the_columns)
        return references_to_the_columns[0].column if len(references_to_the_columns) == 1 else None

    def __if_cell_has_this_candidate_add_it_to_the_list_of_references(self, cell : IndicesOfCell, 
                                                                        candidate : int, references : list):
        if self.__cell_has_candidate(cell, candidate):
                references.append(cell)

    def __find_column_with_candidate_with_only_one_occurrence_and_insert_it(self):
        for column in range(self.__sudoku.values_for_side_of_a_sudoku):
            self.__find_and_insert_candidate_with_only_one_occurence_for_this_column(column)

    def __find_and_insert_candidate_with_only_one_occurence_for_this_column(self, column : int):
        for candidate in range(1, self.__sudoku.values_for_side_of_a_sudoku + 1):
            row = self.__find_the_row_in_which_to_insert_value(column, candidate)
            self.__insert_the_value_and_update_the_candidates(IndicesOfCell(row, column), candidate)

    def __find_the_row_in_which_to_insert_value(self, column : int, candidate : int) -> int:
        references_to_the_rows = []
        for row in range(self.__sudoku.values_for_side_of_a_sudoku):
            self.__if_cell_has_this_candidate_add_it_to_the_list_of_references(IndicesOfCell(row, column),
                                                                                candidate, references_to_the_rows)
        return references_to_the_rows[0].row if len(references_to_the_rows) == 1 else None

    def __insert_the_value_and_update_the_candidates(self, cell : IndicesOfCell, value : int):
        if self.__sudoku.insert_value_in_cell(cell, value):
            self.__count_inserted += 1
            self.__update_candidates(cell, value)

    def __try_to_solve_the_cell(self, cell : IndicesOfCell):
        if self.__cell_has_only_one_candidate(cell):
            self.__confirm_candidate(cell)

    def __cell_has_only_one_candidate(self, cell : IndicesOfCell) -> bool:
        return (self.__sudoku.cell_is_empty(cell) 
                and cell in self.__candidates 
                and len(self.__candidates[cell]) == 1)

    def __confirm_candidate(self, cell : IndicesOfCell):
        self.__insert_the_value_and_update_the_candidates(cell, self.__candidates[cell][0])

    def __update_candidates(self, cell : IndicesOfCell, value_confirmed : int):
        self.__candidates.pop(cell)
        self.__update_row_candidates(cell.row, value_confirmed)
        self.__update_column_candidates(cell.column, value_confirmed)
        self.__update_block_candidates(IndicesOfCell(self.__sudoku.first_row_of_the_block(cell.row), 
                                        self.__sudoku.first_column_of_the_block(cell.column)), value_confirmed)

    def __update_row_candidates(self, row : int, value_confirmed : int):
        for column in range(self.__sudoku.values_for_side_of_a_sudoku):
            self.__remove_a_candidate(IndicesOfCell(row, column), value_confirmed)

    def __update_column_candidates(self, column : int, value_confirmed : int):
        for row in range(self.__sudoku.values_for_side_of_a_sudoku):
            self.__remove_a_candidate(IndicesOfCell(row, column), value_confirmed)

    def __update_block_candidates(self, cell_to_start_from : IndicesOfCell, value_confirmed : int):
        iterator = self.__sudoku.get_the_iterator_of_the_indices_of_the_block_cells(cell_to_start_from)
        for cell in iterator:
            self.__remove_a_candidate(cell, value_confirmed)

    def __remove_a_candidate(self, cell : IndicesOfCell, candidate_to_be_deleted : int):
        if self.__cell_has_candidate(cell, candidate_to_be_deleted):
            self.__candidates[cell].remove(candidate_to_be_deleted)
    
    def __cell_has_candidate(self, cell : IndicesOfCell, candidate: int) -> bool:
        return cell in self.__candidates and candidate in self.__candidates[cell]

    def __check_if_a_stall_has_occurred(self):
        self.__stall = self.__count_inserted == 0
        self.__count_inserted = 0

    def get_solution(self) -> ClassicSudoku:
        return self.__sudoku