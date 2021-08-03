from math import *
from numpy import *

from puzzle.cell import *
from puzzle.puzzle import *
from utility.printUtility import *

class ClassicSudoku(Puzzle):
    
    def __init__(self, sudoku : list):
        self.__check_input(sudoku)
        self.__make_grid(sudoku)
        self.__calculate_candidates()
    
    def __str__(self):
        printer = PrintClassicSudokuBoard(self.__blocks_for_side_of_a_sudoku, self.__values_for_side_of_a_block)
        return (printer.make_top_frame()
                + printer.make_board(self.__sudoku, self.candidates)
                + printer.make_bottom_frame()) 
        
    def __eq__(self, sudoku):
        return (self.__sudoku is not None
                and type(self) == type(sudoku)
                and array_equal(self.__sudoku, sudoku.__sudoku))

    @property
    def blocks_for_side_of_a_sudoku(self) -> int:
        return self.__blocks_for_side_of_a_sudoku
    
    @property 
    def values_for_side_of_a_block(self) -> int:
        return self.__values_for_side_of_a_block

    @property
    def values_for_side_of_a_sudoku(self) -> int:
        return self.__values_for_side_of_a_block * self.__blocks_for_side_of_a_sudoku

    def __check_input(self, sudoku : list):
        self.__check_dimensions(sudoku)
        self.__check_content(sudoku)
        
    def __check_dimensions(self, sudoku : list):
        square_root = int(sqrt(len(sudoku)))
        if square_root > 1 and (square_root * square_root) != len(sudoku):
            raise ValueError("Dimensione del sudoku non valida, assicurarsi di inserire una griglia valida!!")
    
    def __check_content(self, sudoku : list):
        for row in sudoku:
            if len(row) != len(sudoku):
                raise ValueError("Una riga non è compatibile con il sudoku in questione!!")
            for value in row:
                if value > len(sudoku):
                    raise ValueError(str(value) + " non può essere presente in questo sudoku!!")
    
    def __make_grid(self, sudoku: list):
        self.__init_information(sudoku)
        self.__sudoku = array(sudoku)
        
    def __init_information(self, sudoku: list):
        self.__values_for_side_of_a_block = int(sqrt(len(sudoku)))
        self.__blocks_for_side_of_a_sudoku = int(sqrt(len(sudoku)))
        
    def __index_of_the_next_block(self, start_index: int) -> int:
        return ((start_index + 1) * self.__values_for_side_of_a_block)
    
    def __first_row_of_the_block(self, row_of_cell : int):
        return int(row_of_cell / self.__blocks_for_side_of_a_sudoku) * self.__values_for_side_of_a_block
    
    def __first_column_of_the_block(self, column_of_cell : int):
        return int(column_of_cell / self.__blocks_for_side_of_a_sudoku) * self.__values_for_side_of_a_block

    def __calculate_candidates(self):
        self.candidates =  {}
        for row in range(len(self.__sudoku)):
            for column in range(len(self.__sudoku)):
                candidates_for_a_cell = []
                for candidate in range(1, len(self.__sudoku) + 1):
                    if self.__candidate_is_eligible(IndicesOfCell(row, column), candidate):
                        candidates_for_a_cell.append(candidate)
                if len(candidates_for_a_cell) > 0:
                    self.candidates[IndicesOfCell(row, column)] = candidates_for_a_cell
                
    def __candidate_is_eligible(self, cell : IndicesOfCell, value : int) -> bool:
        return (self.cell_is_empty(cell)
                and self.__value_not_in_block(cell, value) 
                and self.__value_not_in_row(cell.row, value) 
                and self.__value_not_in_column(cell.column, value))
        
    def cell_is_empty(self, cell : IndicesOfCell) -> bool:    
        return self.__sudoku[cell.row, cell.column] == 0

    def cell_has_candidate(self, cell : IndicesOfCell, candidate: int) -> bool:
        return cell in self.candidates and candidate in self.candidates[cell]
        
    def __value_not_in_block(self, cell : IndicesOfCell, candidate : int) -> bool: 
        return candidate not in self.__sudoku[self.__first_row_of_the_block(cell.row) : 
                                            self.__first_row_of_the_block(cell.row) + self.__values_for_side_of_a_block,
                                            self.__first_column_of_the_block(cell.column) : 
                                            self.__first_column_of_the_block(cell.column) + self.__values_for_side_of_a_block]
    
    def __value_not_in_row(self, row : int, candidate : int) ->bool:
        return candidate not in self.__sudoku[row, : ]
        
    def __value_not_in_column(self, column : int, candidate : int) ->bool:
        return candidate not in self.__sudoku[ :, column]

    # TODO: Test
    def is_solved(self) -> bool:
        return len(self.candidates) == 0

    def cell_has_only_one_candidate(self, cell : IndicesOfCell) -> bool:
        return (self.cell_is_empty(cell) 
                and cell in self.candidates 
                and len(self.candidates[cell]) == 1)

    # returns False if the operation fails, otherwise True
    def confirm_candidate(self, cell : IndicesOfCell):
        self.insert_value_in_cell(cell, self.candidates[cell][0])
    
    def insert_value_in_cell(self, cell : IndicesOfCell, value : int) -> bool:
        if self.__cell_and_value_is_valid(cell, value):
            self.__complete_inserting_value_in_cell(cell, value)
            return True
        return False

    def __cell_and_value_is_valid(self, cell : IndicesOfCell, value : int) -> bool:
        return self.__cell_is_valid(cell) and self.__value_is_valid(value)

    def __cell_is_valid(self, cell : IndicesOfCell) -> bool:
        return self.__index_is_valid(cell.row) and self.__index_is_valid(cell.column)
    
    def __index_is_valid(self, index : int) -> bool:
        return (isinstance(index, int) 
                and index >= 0 
                and index < self.values_for_side_of_a_sudoku)

    def __value_is_valid(self, value : int) -> bool:
        return (isinstance(value, int) 
                and value > 0 
                and value <= self.values_for_side_of_a_sudoku)

    def __complete_inserting_value_in_cell(self, cell : IndicesOfCell, value : int):
            self.__sudoku[cell.row, cell.column] = value
            self.__update_candidates(cell, value)

    def __update_candidates(self, cell : IndicesOfCell, value_confirmed : int):
        self.candidates.pop(cell)
        self.__update_row_candidates(cell.row, value_confirmed)
        self.__update_column_candidates(cell.column, value_confirmed)
        self.__update_block_candidates(self.__first_row_of_the_block(cell.row), 
                                        self.__first_column_of_the_block(cell.column), value_confirmed)

    def __update_row_candidates(self, row : int, value_confirmed : int):
        for column in range(self.values_for_side_of_a_sudoku):
            self.__remove_a_candidate(IndicesOfCell(row, column), value_confirmed)

    def __update_column_candidates(self, column : int, value_confirmed : int):
        for row in range(self.values_for_side_of_a_sudoku):
            self.__remove_a_candidate(IndicesOfCell(row, column), value_confirmed)

    def __update_block_candidates(self,row_start : int, column_start : int, value_confirmed : int):
        for row in range(row_start, row_start + self.__values_for_side_of_a_block):
            for column in range(column_start, column_start + self.__values_for_side_of_a_block):
                self.__remove_a_candidate(IndicesOfCell(row, column), value_confirmed)

    def __remove_a_candidate(self, cell : IndicesOfCell, candidate_to_be_deleted : int):
        if self.cell_has_candidate(cell, candidate_to_be_deleted):
            self.candidates[cell].remove(candidate_to_be_deleted)