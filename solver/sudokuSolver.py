from typing import Iterator

from solver.solver import *
from puzzle.sudoku import *
from puzzle.cell import *

class ClassicSudokuSolver(Solver):
    #region Constructor
    def __init__(self, sudoku : ClassicSudoku):
        self.__initialize_the_fields(sudoku)
        self.__calculate_candidates()
    
    def __initialize_the_fields(self, sudoku : ClassicSudoku):
        self.__sudoku = sudoku
        self.__stall = False
        self.__count_inserted = 0
        self.__count_excess_candidates_removed = 0
    #endregion

    #region To stirng
    def __str__(self):
        from utility.printUtility import PrintClassicSudokuBoard
        printer = PrintClassicSudokuBoard(self.__sudoku)
        return printer.print_sudoku_with_candidate(self.__candidates)
    #endregion

    #region Calculate candidates
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
    #endregion
    
    #region Solve
    def solve(self):
        while not self.__sudoku.is_solved() and not self.__stall:
            print(self)
            # input("press enter")
            self.__start_to_solve()
            self.__check_if_a_stall_has_occurred()
        if self.__stall:
            print("a stall has occurred")
            self.__try_to_remove_excess_candidates()
        else:
            print(self.__sudoku)

    def __start_to_solve(self):
        self.__find_cell_with_one_candidate()
        self.__find_row_with_candidate_with_only_one_occurrence_and_insert_it()
        self.__find_column_with_candidate_with_only_one_occurrence_and_insert_it()
        self.__find_block_with_candidate_with_only_one_occurrence_and_insert_it()
    
    def __try_to_remove_excess_candidates(self):
        self.__finds_the_row_in_which_a_candidate_belongs_to_only_one_block()
        self.__finds_the_column_in_which_a_candidate_belongs_to_only_one_block()
        self.__finds_the_block_in_which_a_candidate_belongs_to_a_single_row()
        self.__finds_the_block_in_which_a_candidate_belongs_to_a_single_column()
        self.__find_sets_of_candidates_discovered_in_row()
        print(self)
        self.__check_if_the_stall_has_been_resolved()
        if not self.__stall:
            self.solve()
        else:
            print("not possible remove a stall")
            
    #region Find a cell with only one candidate
    def __find_cell_with_one_candidate(self):
        iterator = self.__sudoku.get_the_iterator_of_the_indices_of_the_sudoku_cells()
        for cell in iterator:
            self.__try_to_solve_the_cell(cell)
    
    def __try_to_solve_the_cell(self, cell : IndicesOfCell):
        if self.__cell_has_only_one_candidate(cell):
            self.__confirm_candidate(cell)

    def __cell_has_only_one_candidate(self, cell : IndicesOfCell) -> bool:
        return (self.__sudoku.cell_is_empty(cell) 
                and cell in self.__candidates 
                and len(self.__candidates[cell]) == 1)

    def __confirm_candidate(self, cell : IndicesOfCell):
        self.__insert_the_value_and_update_the_candidates(cell, self.__candidates[cell][0])
    #endregion

    #region Find a row with a candidate that has only one occurrence and insert it
    def __find_row_with_candidate_with_only_one_occurrence_and_insert_it(self):
        for row in range(self.__sudoku.values_for_side_of_a_sudoku):
            self.__find_and_insert_candidate_with_only_one_occurence_for_this_row(row)
        
    def __find_and_insert_candidate_with_only_one_occurence_for_this_row(self, row : int):
        iterator = self.__sudoku.get_the_iterator_of_the_indices_of_the_cells_in_the_row(row)
        self.__find_and_insert_candidate_with_only_one_occurence_for_this_section(iterator)
    #endregion

    #region Find a column with a candidate that has only one occurrence and insert it
    def __find_column_with_candidate_with_only_one_occurrence_and_insert_it(self):
        for column in range(self.__sudoku.values_for_side_of_a_sudoku):
            self.__find_and_insert_candidate_with_only_one_occurence_for_this_column(column)

    def __find_and_insert_candidate_with_only_one_occurence_for_this_column(self, column : int):
        iterator = self.__sudoku.get_the_iterator_of_the_indices_of_the_cells_in_the_column(column)
        self.__find_and_insert_candidate_with_only_one_occurence_for_this_section(iterator)
    #endregion

    #region Find a block with a candidate that has only one occurrence and insert it
    def __find_block_with_candidate_with_only_one_occurrence_and_insert_it(self):
        for row in range(0, self.__sudoku.values_for_side_of_a_sudoku, 3):
            for column in range(0, self.__sudoku.values_for_side_of_a_sudoku, 3):
                self.__find_and_insert_candidate_with_only_one_occurence_for_this_block(IndicesOfCell(row, column))

    def __find_and_insert_candidate_with_only_one_occurence_for_this_block(self, cell_to_start_from : IndicesOfCell):
        iterator = self.__sudoku.get_the_iterator_of_the_indices_of_the_cells_in_the_block(cell_to_start_from)
        self.__find_and_insert_candidate_with_only_one_occurence_for_this_section(iterator)
    #endregion

    #region Find and insert candidate with only one occurrence for this section of the sudoku
    def __find_and_insert_candidate_with_only_one_occurence_for_this_section(self, iterator : Iterator):
        for candidate in range(1, self.__sudoku.values_for_side_of_a_sudoku + 1):
            cell = self.__find_the_cell_in_which_to_insert_value(iterator, candidate)
            self.__insert_the_value_and_update_the_candidates(cell, candidate)

    def __find_the_cell_in_which_to_insert_value(self, iterator : Iterator, candidate : int) -> IndicesOfCell:
        references_to_the_cells = list(self.__find_the_cells_that_contain_the_candidate(iterator, candidate))
        return references_to_the_cells[0] if len(references_to_the_cells) == 1 else None

    def __find_the_cells_that_contain_the_candidate(self, iterator : Iterator, candidate : int) -> set:
        references_to_the_cells = set()
        for cell in iterator:
            self.__if_cell_has_this_candidate_add_it_to_the_list_of_references(cell, candidate, references_to_the_cells)
        return references_to_the_cells

    def __if_cell_has_this_candidate_add_it_to_the_list_of_references(self, cell : IndicesOfCell, 
                                                                        candidate : int, references : set):
        if self.__cell_has_candidate(cell, candidate):
                references.add(cell)
    #endregion

    #region Insert the value and update the candidates
    def __insert_the_value_and_update_the_candidates(self, cell : IndicesOfCell, value : int):
        if self.__sudoku.insert_value_in_cell(cell, value):
            self.__count_inserted += 1
            self.__update_candidates(cell, value)

    #region Update candidates
    def __update_candidates(self, cell : IndicesOfCell, value_confirmed : int):
        self.__candidates.pop(cell)
        self.__update_row_candidates(cell.row, value_confirmed)
        self.__update_column_candidates(cell.column, value_confirmed)
        self.__update_block_candidates(self.__sudoku.first_cell_of_the_block(cell), value_confirmed)

    def __update_row_candidates(self, row : int, value_confirmed : int):
        for column in range(self.__sudoku.values_for_side_of_a_sudoku):
            self.__remove_a_candidate(IndicesOfCell(row, column), value_confirmed)

    def __update_column_candidates(self, column : int, value_confirmed : int):
        for row in range(self.__sudoku.values_for_side_of_a_sudoku):
            self.__remove_a_candidate(IndicesOfCell(row, column), value_confirmed)

    def __update_block_candidates(self, cell_to_start_from : IndicesOfCell, value_confirmed : int):
        iterator = self.__sudoku.get_the_iterator_of_the_indices_of_the_cells_in_the_block(cell_to_start_from)
        for cell in iterator:
            self.__remove_a_candidate(cell, value_confirmed)

    #region Remove a candidate
    def __remove_a_candidate(self, cell : IndicesOfCell, candidate_to_be_deleted : int) -> bool:
        if self.__cell_has_candidate(cell, candidate_to_be_deleted):
            self.__candidates[cell].remove(candidate_to_be_deleted)
            return True
        return False
    
    def __cell_has_candidate(self, cell : IndicesOfCell, candidate: int) -> bool:
        return cell in self.__candidates and candidate in self.__candidates[cell]
    #endregion
    #endregion
    #endregion

    #region Find the row where a candidate belongs to only one block, if this row exists remove excess candidates from the block
    def __finds_the_row_in_which_a_candidate_belongs_to_only_one_block(self):
        for row in range(self.__sudoku.values_for_side_of_a_sudoku):
            self.__find_the_candidate_belonging_to_only_one_block_in_this_section(
                self.__sudoku.get_the_iterator_of_the_indices_of_the_cells_in_the_row(row)
            )
    #endregion

    #region Find the column where a candidate belongs to only one block, if this column exists remove excess candidates from the block
    def __finds_the_column_in_which_a_candidate_belongs_to_only_one_block(self):
        for column in range(self.__sudoku.values_for_side_of_a_sudoku):
            self.__find_the_candidate_belonging_to_only_one_block_in_this_section(
                self.__sudoku.get_the_iterator_of_the_indices_of_the_cells_in_the_column(column)
            )
    #endregion

    def __find_the_candidate_belonging_to_only_one_block_in_this_section(self, iterator : Iterator):
        for candidate in range(1, self.__sudoku.values_for_side_of_a_sudoku + 1):
            self.__if_the_candidate_belongs_to_only_one_block_in_this_section_update_candidates_of_block(iterator, candidate)

    def __if_the_candidate_belongs_to_only_one_block_in_this_section_update_candidates_of_block(self, iterator : Iterator, 
                                                                                            candidate : int):
        self.__if_the_candidate_belongs_to_a_part_of_the_section_updates_the_candidates_of_this_part(
            iterator, candidate, self.__sudoku.these_cells_belong_to_a_single_block, 
            lambda a_set : self.__sudoku.get_the_set_of_cells_indices_of_a_block(list(a_set)[0])
        )

    #region Find the block where a candidate belongs to only one row, if this block exists remove excess candidates from the row
    def __finds_the_block_in_which_a_candidate_belongs_to_a_single_row(self):
        for row in range(0, self.__sudoku.values_for_side_of_a_sudoku, 3):
            for column in range(0, self.__sudoku.values_for_side_of_a_sudoku, 3):
                self.__find_the_candidate_belonging_to_only_one_row_in_this_block(
                    self.__sudoku.get_the_iterator_of_the_indices_of_the_cells_in_the_block(IndicesOfCell(row, column))
                )
    
    def __find_the_candidate_belonging_to_only_one_row_in_this_block(self, iterator : Iterator):
        for candidate in range(1, self.__sudoku.values_for_side_of_a_sudoku + 1):
            self.__if_the_candidate_belongs_to_only_one_row_in_this_block_update_candidates_of_row(iterator, candidate)
            
    def __if_the_candidate_belongs_to_only_one_row_in_this_block_update_candidates_of_row(self, iterator : Iterator, 
                                                                                            candidate : int):
        self.__if_the_candidate_belongs_to_a_part_of_the_section_updates_the_candidates_of_this_part(
            iterator, candidate, self.__sudoku.these_cells_belong_to_a_single_row,
            lambda a_set : set(self.__sudoku.get_the_iterator_of_the_indices_of_the_cells_in_the_row(list(a_set)[0].row))
        )
    #endregion

    #region Find the block where a candidate belongs to only one column, if this block exists remove excess candidates from the column
    def __finds_the_block_in_which_a_candidate_belongs_to_a_single_column(self):
        for row in range(0, self.__sudoku.values_for_side_of_a_sudoku, 3):
            for column in range(0, self.__sudoku.values_for_side_of_a_sudoku, 3):
                self.__find_the_candidate_belonging_to_only_one_column_in_this_block(
                    self.__sudoku.get_the_iterator_of_the_indices_of_the_cells_in_the_block(IndicesOfCell(row, column))
                )

    def __find_the_candidate_belonging_to_only_one_column_in_this_block(self, iterator : Iterator):
        for candidate in range(1, self.__sudoku.values_for_side_of_a_sudoku + 1):
            self.__if_the_candidate_belongs_to_only_one_column_in_this_block_update_candidates_of_column(iterator, candidate)

    def __if_the_candidate_belongs_to_only_one_column_in_this_block_update_candidates_of_column(self, iterator : Iterator, 
                                                                                            candidate : int):
        self.__if_the_candidate_belongs_to_a_part_of_the_section_updates_the_candidates_of_this_part(
            iterator, candidate, self.__sudoku.these_cells_belong_to_a_single_column,
            lambda a_set : set(self.__sudoku.get_the_iterator_of_the_indices_of_the_cells_in_the_column(list(a_set)[0].column))
        )
    #endregion

    def __if_the_candidate_belongs_to_a_part_of_the_section_updates_the_candidates_of_this_part(self, iterator : Iterator, 
                                                                                            candidate : int,
                                                                                            these_cells_belong_to_a_single_section : Callable[[set], bool],
                                                                                            get_the_set_of_cells_indices_of_a_section : Callable[[IndicesOfCell], set]):
        section_of_interest = self.__find_the_cells_that_contain_the_candidate(iterator, candidate)
        if these_cells_belong_to_a_single_section(section_of_interest):
            self.__delete_the_candidate_from_the_other_parts_of_that_section(
                get_the_set_of_cells_indices_of_a_section(section_of_interest) - set(iterator),
                candidate
            )
    
    def __delete_the_candidate_from_the_other_parts_of_that_section(self, cells_to_modify : set, candidate : int):
        for cell in cells_to_modify:
            self.__count_excess_candidates_removed += bool(self.__remove_a_candidate(cell, candidate))

    #TODO: refactoring
    def __find_sets_of_candidates_discovered_in_row(self):
        for row in range(self.__sudoku.values_for_side_of_a_sudoku):
            iterator = self.__sudoku.get_the_iterator_of_the_indices_of_the_cells_in_the_row(row)
            iterator2 = list(iterator)
            for i in iterator:
                references_of_cell = set()
                if self.__sudoku.cell_is_empty(i):
                    references_of_cell.add(i)
                    iterator2.remove(i)
                    for j in iterator2:
                        if self.__sudoku.cell_is_empty(j) and self.__candidates[i] == self.__candidates[j]:
                            references_of_cell.add(j)
                    if  len(self.__candidates[i]) == len(references_of_cell):
                        for candidate in self.__candidates[i]:
                            self.__delete_the_candidate_from_the_other_parts_of_that_section(
                                set(iterator) - references_of_cell, candidate
                            )

    #region Check if you have stalled, or if you have come out of a stall
    def __check_if_a_stall_has_occurred(self):
        self.__stall = self.__count_inserted == 0
        self.__count_inserted = 0
    
    def __check_if_the_stall_has_been_resolved(self):
        self.__stall = self.__count_excess_candidates_removed == 0
        self.__count_excess_candidates_removed = 0
    #endregion 
    #endregion

    #region Get Solution
    def get_solution(self) -> ClassicSudoku:
        return self.__sudoku
    #endregion