from math import *
from numpy import *

from puzzle.cell import *
from puzzle.puzzle import *

class ClassicSudoku(Puzzle):
    
    def __init__(self, sudoku : list):
        self.__check_input(sudoku)
        self.__make_grid(sudoku)
    
    """ 
    def __str__(self):
        from utility.printUtility import PrintClassicSudokuBoard
        printer = PrintClassicSudokuBoard(self)
        return (printer.make_top_frame()
                + printer.make_board(self.candidates)
                + printer.make_bottom_frame()) 
    """ 
        
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

    def get_the_value_from_cell(self, cell : IndicesOfCell) -> int:
        return self.__sudoku[cell.row, cell.column]

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
    
    def first_row_of_the_block(self, row_of_cell : int):
        return int(row_of_cell / self.__blocks_for_side_of_a_sudoku) * self.__values_for_side_of_a_block
    
    def first_column_of_the_block(self, column_of_cell : int):
        return int(column_of_cell / self.__blocks_for_side_of_a_sudoku) * self.__values_for_side_of_a_block
        
    def cell_is_empty(self, cell : IndicesOfCell) -> bool:    
        return self.__sudoku[cell.row, cell.column] == 0
        
    def value_not_in_block(self, cell : IndicesOfCell, candidate : int) -> bool: 
        return candidate not in self.__sudoku[self.first_row_of_the_block(cell.row) : 
                                            self.first_row_of_the_block(cell.row) + self.__values_for_side_of_a_block,
                                            self.first_column_of_the_block(cell.column) : 
                                            self.first_column_of_the_block(cell.column) + self.__values_for_side_of_a_block]
    
    def value_not_in_row(self, row : int, candidate : int) ->bool:
        return candidate not in self.__sudoku[row, : ]
        
    def value_not_in_column(self, column : int, candidate : int) ->bool:
        return candidate not in self.__sudoku[ :, column]

    # TODO: Test
    def is_solved(self) -> bool:
        return 0 not in self.__sudoku

    def insert_value_in_cell(self, cell : IndicesOfCell, value : int) -> bool:
        if self.__cell_and_value_is_valid(cell, value):
            self.__sudoku[cell.row, cell.column] = value
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