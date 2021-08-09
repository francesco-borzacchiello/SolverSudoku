from math import *
from typing import Any, Callable
from numpy import *

from puzzle.cell import *
from puzzle.puzzle import *

class ClassicSudoku(Puzzle):
    #region Constructor
    def __init__(self, sudoku : list):
        self.__check_input(sudoku)
        self.__make_grid(sudoku)
    
    #region Check if the input is valid
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
    #endregion

    #region Make a grid that contains the sudoku values and related information
    def __make_grid(self, sudoku: list):
        self.__init_information(sudoku)
        self.__sudoku = array(sudoku)
        
    def __init_information(self, sudoku: list):
        self.__values_for_side_of_a_block = int(sqrt(len(sudoku)))
        self.__blocks_for_side_of_a_sudoku = int(sqrt(len(sudoku)))
    #endregion
    #endregion
        
    #region To string
    def __str__(self):
        from utility.printUtility import PrintClassicSudokuBoard
        printer = PrintClassicSudokuBoard(self)
        return printer.print_sudoku()
    #endregion

    #region It's equal to [sudoku]
    def __eq__(self, sudoku):
        return (self.__sudoku is not None
                and type(self) == type(sudoku)
                and array_equal(self.__sudoku, sudoku.__sudoku))
    #endregion

    #region Property
    @property
    def blocks_for_side_of_a_sudoku(self) -> int:
        return self.__blocks_for_side_of_a_sudoku
    
    @property 
    def values_for_side_of_a_block(self) -> int:
        return self.__values_for_side_of_a_block

    @property
    def values_for_side_of_a_sudoku(self) -> int:
        return self.__values_for_side_of_a_block * self.__blocks_for_side_of_a_sudoku
    #endregion

    #region Get information about the sudoku and its contents
    def get_the_value_from_cell(self, cell : IndicesOfCell) -> int:
        return self.__sudoku[cell.row, cell.column]
    
    def first_cell_of_the_block(self, cell : IndicesOfCell) -> IndicesOfCell:
        return IndicesOfCell(
            int(cell.row / self.__blocks_for_side_of_a_sudoku) * self.__values_for_side_of_a_block, 
            int(cell.column / self.__blocks_for_side_of_a_sudoku) * self.__values_for_side_of_a_block)

    def cell_is_empty(self, cell : IndicesOfCell) -> bool:
        return self.__sudoku[cell.row, cell.column] == 0
    
    #region Check if the following cells all belong to the same section
    def these_cells_belong_to_a_single_block(self, references_to_the_cells : list) -> bool: 
        return self.__these_cells_belong_to_a_single_section(references_to_the_cells, self.first_cell_of_the_block)
    
    def these_cells_belong_to_a_single_row(self, references_to_the_cells : list) -> bool:
        return self.__these_cells_belong_to_a_single_section(references_to_the_cells, lambda cell : cell.row)

    def __these_cells_belong_to_a_single_section(self, references_to_the_cells : list, 
                                                    get_information_from_cell : Callable[[IndicesOfCell], Any]) -> bool:
        try:
            first_cell_of_the_blocks = self.__extract_the_first_cells_of_the_blocks_by_the_following_cells(references_to_the_cells, get_information_from_cell)
            return len(first_cell_of_the_blocks) == 1
        except IndexError:
            return False

    def __extract_the_first_cells_of_the_blocks_by_the_following_cells(self, cells : list, get_information_from_cell : Callable[[IndicesOfCell], Any]) -> set:
        first_cell_of_the_blocks = set()
        for cell in cells:
            first_cell_of_the_blocks.add(get_information_from_cell(cell))
        return first_cell_of_the_blocks
    #endregion

    #region Checks if a value is in a part of the sudoku    
    def value_not_in_block(self, cell : IndicesOfCell, candidate : int) -> bool:
        cell_to_start_from = self.first_cell_of_the_block(cell)
        return candidate not in self.__sudoku[
                cell_to_start_from.row : cell_to_start_from.row + self.__values_for_side_of_a_block,
                cell_to_start_from.column : cell_to_start_from.column + self.__values_for_side_of_a_block]
    
    def value_not_in_row(self, row : int, candidate : int) ->bool:
        return candidate not in self.__sudoku[row, : ]
        
    def value_not_in_column(self, column : int, candidate : int) ->bool:
        return candidate not in self.__sudoku[ :, column]
    #endregion

    def get_the_set_of_cells_indeces_of_a_block(self, a_cell_in_the_block) -> set:
        return set(self.get_the_iterator_of_the_indices_of_the_cells_in_the_block(
                    self.first_cell_of_the_block(a_cell_in_the_block)))

    # TODO: Test
    def is_solved(self) -> bool:
        return 0 not in self.__sudoku
    #endregion

    #region Insert a value in a cell of the sudoku
    def insert_value_in_cell(self, cell : IndicesOfCell, value : int) -> bool:
        if self.__cell_and_value_is_valid(cell, value):
            self.__sudoku[cell.row, cell.column] = value
            return True
        return False

    #region Checks if the input of the insert_value_in_cell function is valid
    def __cell_and_value_is_valid(self, cell : IndicesOfCell, value : int) -> bool:
        return cell is not None and self.__cell_is_valid(cell) and self.__value_is_valid(value)

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
    #endregion
    #endregion

    #region Iterators getter
    def get_the_iterator_of_the_indices_of_the_sudoku_cells(self):
        return self.__IteratorOfTheIndicesOfTheSudokuCells(self.values_for_side_of_a_sudoku)

    def get_the_iterator_of_the_indices_of_the_cells_in_the_block(self, cell_to_start_from : IndicesOfCell):
        return self.__IteratorOfTheIndicesOfTheCellsInTheBlock(cell_to_start_from, self.__values_for_side_of_a_block)
    
    def get_the_iterator_of_the_indices_of_the_cells_in_the_row(self, row : int):
        return self.__IteratorOfTheIndicesOfTheCellsInTheRow(row, self.values_for_side_of_a_sudoku)

    def get_the_iterator_of_the_indices_of_the_cells_in_the_column(self, column : int):
        return self.__IteratorOfTheIndicesOfTheCellsInTheColumn(column, self.values_for_side_of_a_sudoku)
    #endregion

    #region Iterators, to navigate the sudoku in different ways
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
        
    class __IteratorOfTheIndicesOfTheCellsInTheBlock(__IteratorOfTheIndicesOfTheSudokuCells):
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

    class __IteratorOfTheIndicesOfTheCellsInTheRow(__IteratorOfTheIndicesOfTheSudokuCells):
        def __init__(self, row : int, upper_bound_for_column : int):
            super().__init__(upper_bound_for_column)
            self._upper_bound_for_row = row
        
        def __iter__(self):
            self._current_row = self._upper_bound_for_row
            self._current_column = self._column_to_start - 1
            return self

        def __next__(self) -> IndicesOfCell:
            return super().__next__()
        
    class __IteratorOfTheIndicesOfTheCellsInTheColumn(__IteratorOfTheIndicesOfTheSudokuCells):
        def __init__(self, column : int, upper_bound_for_row : int):
            super().__init__(upper_bound_for_row)
            self._column_to_start = self._upper_bound_for_column = column
        
        def __iter__(self):
            self._current_row = -1
            self._current_column = self._upper_bound_for_column
            return self

        def __next__(self) -> IndicesOfCell:
            return super().__next__()
    #endregion