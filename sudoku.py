from math import *
from numpy import *

from puzzle import *

class ClassicSudoku(Puzzle):
    
    def __init__(self, sudoku : list):
        self.__check_input(sudoku)
        self.__make_grid(sudoku)
        self.__calculate_candidates()
        #print(self)
    
    def __str__(self):
        return (self.__make_top_frame()
                + self.__make_board()
                + self.__make_bottom_frame()) 
                # + "\n\n" + str(self.candidates)
        
    def __eq__(self, sudoku):
        return (self.__sudoku is not None
                and type(self) == type(sudoku)
                and array_equal(self.__sudoku, sudoku.__sudoku))

    ################################ Function for print a sudoku ################################
    def __make_frame_parts_with_additional_divider(self, start: str, edge: str, divider : str,
                                                    intermediate_divider : str, end : str) -> str:
        # + 2 for aesthetic reasons, to increase the width of the sudoku  
        border_cell = edge * (self.__values_for_side_of_a_block + 2)
        border_block = ((border_cell + intermediate_divider) * (self.__values_for_side_of_a_block - 1)) + border_cell
        return (start 
                + ((border_block + divider) * (self.__blocks_for_side_of_a_sudoku - 1)) 
                + border_block
                + end
                )
                    
    def __make_frame_parts(self, start: str, edge: str, divider : str, end : str) -> str:
        return self.__make_frame_parts_with_additional_divider(start, edge, divider, edge, end)

    def __make_top_frame(self) -> str:
        return self.__make_frame_parts("╔", "═", "╦", "╗\n")
    
    def __make_orizontal_divider_frame(self) -> str:
        return self.__make_frame_parts("╠", "═", "╬", "╣\n")

    def __make_bottom_frame(self) -> str:
        return self.__make_frame_parts("╚", "═", "╩", "╝\n")
    
    def __make_orizontal_divider_block(self) -> str:
        return self.__make_frame_parts_with_additional_divider("║", "─", "║", "┼", "║\n")

    # TODO: refactoring
    def __make_board(self) -> str:
        board = ""
        for row in range(len(self.__sudoku)):
            for row_of_value in range(self.__values_for_side_of_a_block):
                board += "║ "
                for column in range(len(self.__sudoku)):
                    for column_of_value in range(self.__values_for_side_of_a_block):
                        index_candidate = 0
                        if not self.cell_is_empty(row, column):
                            board += self.__make_cell_full(row_of_value, column_of_value, self.__sudoku[row, column])
                        else:
                            expected_candidate = (row_of_value * self.__values_for_side_of_a_block) + (column_of_value + 1)
                            while (index_candidate < len(self.candidates[(row, column)])
                                    and self.candidates[(row, column)][index_candidate] < expected_candidate):
                                    index_candidate += 1
                            if  (index_candidate >= len(self.candidates[(row, column)])
                                or self.candidates[(row, column)][index_candidate] > expected_candidate):  
                                    board += " "
                            else:
                                board += str(self.candidates[(row, column)][index_candidate])
                        board += self.__make_vertical_divider_frame(column, column_of_value)
                board += " ║\n"
            if row + 1 != (self.__blocks_for_side_of_a_sudoku * self.__values_for_side_of_a_block):
                if (row + 1) % self.__values_for_side_of_a_block == 0:
                    board += self.__make_orizontal_divider_frame()
                elif row_of_value == self.__values_for_side_of_a_block - 1:
                    board += self.__make_orizontal_divider_block()
        return board
    
    def __make_cell_full(self, row : int, column : int, value : int) -> str:
        if row == (column % self.__blocks_for_side_of_a_sudoku) and int(self.__blocks_for_side_of_a_sudoku / 2) == row:
            return str(value)
        else:
            return "•"

    def __make_vertical_divider_frame(self, column : int, column_of_cell : int) -> str:
        if (column_of_cell == self.__values_for_side_of_a_block - 1 
            and (column + 1) % self.__values_for_side_of_a_block != 0
            and column != (self.values_for_side_of_a_sudoku()) - 1):
                return " │ "
        elif (column_of_cell == self.__values_for_side_of_a_block - 1 
              and(column + 1) % self.__values_for_side_of_a_block == 0
              and column != (self.values_for_side_of_a_sudoku()) - 1):
                return " ║ "
        return ""
                
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
    
    def values_for_side_of_a_sudoku(self) -> int:
        return self.__values_for_side_of_a_block * self.__blocks_for_side_of_a_sudoku
    
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
                    if self.__candidate_is_eligible(row, column, candidate):
                        candidates_for_a_cell.append(candidate)
                if len(candidates_for_a_cell) > 0:
                    self.candidates[(row, column)] = candidates_for_a_cell
                
    def __candidate_is_eligible(self, row : int, column : int, value : int) -> bool:
        return (self.cell_is_empty(row, column)
                and self.__value_not_in_block(row, column, value) 
                and self.__value_not_in_row(row, value) 
                and self.__value_not_in_column(column, value))
        
    def cell_is_empty(self, row : int, column : int) -> bool:    
        return self.__sudoku[row, column] == 0

    def cell_has_candidate(self, row : int, column : int, candidate: int) -> bool:
        return (row, column) in self.candidates and candidate in self.candidates[(row, column)]
        
    def __value_not_in_block(self, row : int, column : int, candidate : int) -> bool: 
        return candidate not in self.__sudoku[self.__first_row_of_the_block(row) : 
                                            self.__first_row_of_the_block(row) + self.__values_for_side_of_a_block,
                                            self.__first_column_of_the_block(column) : 
                                            self.__first_column_of_the_block(column) + self.__values_for_side_of_a_block]
    
    def __value_not_in_row(self, row : int, candidate : int) ->bool:
        return candidate not in self.__sudoku[row, : ]
        
    def __value_not_in_column(self, column : int, candidate : int) ->bool:
        return candidate not in self.__sudoku[ :, column]

    # TODO: Test
    def is_solved(self) -> bool:
        return len(self.candidates) == 0

    def cell_has_only_one_candidate(self, row : int, column : int) -> bool:
        return (self.cell_is_empty(row, column) 
                and (row, column) in self.candidates 
                and len(self.candidates[(row, column)]) == 1)

    # returns False if the operation fails, otherwise True
    def confirm_candidate(self, row : int, column : int):
        self.insert_value_in_cell(row, column, self.candidates[(row, column)][0])
    
    def insert_value_in_cell(self, row : int, column : int, value : int) -> bool:
        if self.__cell_and_value_is_valid(row, column, value):
            self.__complete_inserting_value_in_cell(row, column, value)
            return True
        return False

    def __cell_and_value_is_valid(self, row : int, column : int, value : int) -> bool:
        return self.__cell_is_valid(row, column) and self.__value_is_valid(value)

    def __cell_is_valid(self, row : int, column : int) -> bool:
        return self.__index_is_valid(row) and self.__index_is_valid(column)
    
    def __index_is_valid(self, index : int) -> bool:
        return (isinstance(index, int) 
                and index >= 0 
                and index < self.values_for_side_of_a_sudoku())

    def __value_is_valid(self, value : int) -> bool:
        return (isinstance(value, int) 
                and value > 0 
                and value <= self.values_for_side_of_a_sudoku())

    def __complete_inserting_value_in_cell(self, row : int, column : int, value : int):
            self.__sudoku[row, column] = value
            self.__update_candidates(row, column, value)

    def __update_candidates(self, row : int, column : int, value_confirmed : int):
        self.candidates.pop((row, column))
        self.__udate_row_candidates(row, value_confirmed)
        self.__udate_column_candidates(column, value_confirmed)
        self.__update_block_candidates(self.__first_row_of_the_block(row), 
                                        self.__first_column_of_the_block(column), value_confirmed)

    def __udate_row_candidates(self, row : int, value_confirmed : int):
        for column in range(self.values_for_side_of_a_sudoku()):
            self.__remove_a_candidate(row, column, value_confirmed)

    def __udate_column_candidates(self, column : int, value_confirmed : int):
        for row in range(self.values_for_side_of_a_sudoku()):
            self.__remove_a_candidate(row, column, value_confirmed)

    def __update_block_candidates(self,row_start : int, column_start : int, value_confirmed : int):
        for row in range(row_start, row_start + self.__values_for_side_of_a_block):
            for column in range(column_start, column_start + self.__values_for_side_of_a_block):
                self.__remove_a_candidate(row, column, value_confirmed)

    def __remove_a_candidate(self, row : int, column : int, candidate_to_be_deleted : int):
        if self.cell_has_candidate(row, column, candidate_to_be_deleted):
            self.candidates[(row, column)].remove(candidate_to_be_deleted)