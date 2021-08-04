from math import *
from typing import Iterator
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
        
    def __str__(self):
        from utility.printUtility import PrintClassicSudokuBoard
        printer = PrintClassicSudokuBoard(self)
        return printer.print_sudoku()

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

    def get_the_iterator_of_the_indices_of_the_sudoku_cells(self):
        return self.__IteratorOfTheIndicesOfTheSudokuCells(self.values_for_side_of_a_sudoku)

    def get_the_iterator_of_the_indices_of_the_block_cells(self, cell_to_start_from : IndicesOfCell):
        return self.__IteratorOfTheIndicesOfTheBlockCells(cell_to_start_from, self.__values_for_side_of_a_block)

    class __IteratorOfTheIndicesOfTheSudokuCells:
        def __init__(self, upper_bound : int):
            self._column_to_start = 0
            self._upper_bound_for_row = self._upper_bound_for_column = upper_bound
        
        def __iter__(self):
            self._current_row = 0
            self._current_column = -1
            return self
        
        def __next__(self) -> IndicesOfCell:
            if self._is_last_column():
                self.__elements_are_finished()
                return self.__next_row()
            return self.__next_column()

        def __next_column(self) -> IndicesOfCell:
            self._current_column += 1
            return IndicesOfCell(self._current_row, self._current_column)

        def __next_row(self) -> IndicesOfCell:
            self._current_column = self._column_to_start
            self._current_row += 1
            return IndicesOfCell(self._current_row, self._current_column)

        def __elements_are_finished(self):
            if self.__is_last_row():
                raise StopIteration

        def __is_last_row(self):
            return self._current_row + 1 >= self._upper_bound_for_row
        
        def _is_last_column(self):
            return self._current_column + 1 >= self._upper_bound_for_column
        
    class __IteratorOfTheIndicesOfTheBlockCells(__IteratorOfTheIndicesOfTheSudokuCells):
        def __init__(self, cell_to_start_from : IndicesOfCell, side_of_block : int):
            self.__cell_to_start_from = cell_to_start_from
            self._column_to_start = cell_to_start_from.column
            self._upper_bound_for_row = cell_to_start_from.row + side_of_block
            self._upper_bound_for_column = cell_to_start_from.column + side_of_block
            
        def __iter__(self):
            self._current_row = self.__cell_to_start_from.row
            self._current_column = self.__cell_to_start_from.column - 1
            return self
        
        def __next__(self) -> IndicesOfCell:
            return super().__next__()