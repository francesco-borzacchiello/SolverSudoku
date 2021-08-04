from math import *
from numpy import *

from puzzle.cell import *
from puzzle.sudoku import ClassicSudoku

class PrintClassicSudokuBoard:
    def __init__(self, sudoku : ClassicSudoku):
        self.__sudoku = sudoku
        self.__candidates_is_present = False
        self.__dimension_of_a_cell = 1
        self.__board = ""

    def make_top_frame(self) -> str:
        return self.__make_frame_parts("╔", "═", "╦", "╗\n")
    
    def __make_orizontal_divider_frame(self) -> str:
        return self.__make_frame_parts("╠", "═", "╬", "╣\n")

    def make_bottom_frame(self) -> str:
        return self.__make_frame_parts("╚", "═", "╩", "╝\n")

    def __make_frame_parts(self, start: str, edge: str, divider : str, end : str) -> str:
        return self.__make_frame_parts_with_additional_divider(start, edge, divider, edge, end)

    def __make_orizontal_divider_block(self) -> str:
        return self.__make_frame_parts_with_additional_divider("║", "─", "║", "┼", "║\n")

    def __make_frame_parts_with_additional_divider(self, start: str, edge: str, divider : str,
                                                    intermediate_divider : str, end : str) -> str:
        # + 2 for aesthetic reasons, to increase the width of the sudoku  
        border_cell = edge * (self.__dimension_of_a_cell + 2)
        border_block = (((border_cell + intermediate_divider) 
                         * (self.__sudoku.values_for_side_of_a_block - 1))
                        + border_cell)
        return (start 
                + ((border_block + divider) * (self.__sudoku.blocks_for_side_of_a_sudoku - 1)) 
                + border_block
                + end)

    def print_sudoku(self):
        self.__dimension_of_a_cell = 1
        self.__candidates_is_present = False
        return self.__add_the_top_and_bottom_to_frame_of_board({})

    def print_sudoku_with_candidate(self, candidates : dict) -> str:
        self.__dimension_of_a_cell = self.__sudoku.values_for_side_of_a_block
        self.__candidates_is_present = True
        return self.__add_the_top_and_bottom_to_frame_of_board(candidates)

    def __add_the_top_and_bottom_to_frame_of_board(self, candidates : dict) -> str:
        return (self.make_top_frame()
                + self.make_board(candidates)
                + self.make_bottom_frame())

    def make_board(self, candidates : dict) -> str:
        for row in range(self.__sudoku.values_for_side_of_a_sudoku):
            self.__make_row_of_a_board(row, candidates)
            self.__make_orizontal_divider(row)
        return self.__board
    
    def __make_row_of_a_board(self, row : int, candidates : dict):
        for row_of_value in range(self.__dimension_of_a_cell):
                self.__board += "║ "
                self.__make_contents_of_a_row_of_a_board(row, row_of_value, candidates)
                self.__board += "\n"
    
    def __make_contents_of_a_row_of_a_board(self, row : int, row_of_value : int, candidates : dict):
        for column in range(self.__sudoku.values_for_side_of_a_sudoku):
            for column_of_value in range(self.__dimension_of_a_cell):
                cell = IndicesOfCell(row, column)
                self.__make_the_part_of_a_single_cell(cell, IndicesOfCell(row_of_value, column_of_value),
                                                        self.__sudoku.get_the_value_from_cell(cell), candidates)
               
    def __make_the_part_of_a_single_cell(self, cell : IndicesOfCell, part_of_cell : IndicesOfCell, value : int, candidates : dict):
        self.__make_the_content_of_a_part_of_a_single_cell(cell, part_of_cell, value, candidates)
        self.__board += self.__make_vertical_divider_frame(cell.column, part_of_cell.column)

    def __make_the_content_of_a_part_of_a_single_cell(self, cell : IndicesOfCell, part_of_cell : IndicesOfCell,
                                                        value : int, candidates : dict):
        if not self.__sudoku.cell_is_empty(cell):
            self.__board += self.__make_cell_full(part_of_cell, value)
        elif self.__candidates_is_present:
            self.__make_the_part_of_a_single_cell_with_candidates(
                candidates[cell], 
                self.__calculate_expected_candidate(part_of_cell))
        else:
            self.__board += " "

    def __make_vertical_divider_frame(self, column : int, column_of_cell : int) -> str:
        if self.__is_the_boundary_of_cell(column, column_of_cell):
            return " │ "
        elif self.__is_the_boundary_of_block(column, column_of_cell):
            return " ║ "
        return ""

    def __is_the_boundary_of_cell(self, column : int, column_of_cell : int) -> bool:
        return (column_of_cell == self.__dimension_of_a_cell - 1 
                and (column + 1) % self.__sudoku.values_for_side_of_a_block != 0)

    def __is_the_boundary_of_block(self, column : int, column_of_cell : int) -> bool:
        return (column_of_cell == self.__dimension_of_a_cell - 1 
              and (column + 1) % self.__sudoku.values_for_side_of_a_block == 0)

    def __make_cell_full(self, part_of_cell : IndicesOfCell, value : int) -> str:
        if self.__is_center_of_a_cell(part_of_cell):
            return str(value)
        return "•" if self.__candidates_is_present else ""

    def __is_center_of_a_cell(self, part_of_cell : IndicesOfCell):
        return (part_of_cell.row == part_of_cell.column 
                and ceil(self.__dimension_of_a_cell / 2) == (part_of_cell.row + 1))

    def __make_the_part_of_a_single_cell_with_candidates(self, candidates : list, expected_candidate : int):
        if expected_candidate in candidates:
            self.__board += str(expected_candidate)
        else:
            self.__board += " "

    def __calculate_expected_candidate(self, part_of_cell : IndicesOfCell) -> int:
        return (part_of_cell.row * self.__sudoku.values_for_side_of_a_block) + (part_of_cell.column + 1)

    # TODO: check index
    def __make_orizontal_divider(self, row : int):
        if row + 1 != (self.__sudoku.blocks_for_side_of_a_sudoku * self.__sudoku.values_for_side_of_a_block):
            if (row + 1) % self.__sudoku.values_for_side_of_a_block == 0:
                self.__board += self.__make_orizontal_divider_frame()
            else:
                self.__board += self.__make_orizontal_divider_block()