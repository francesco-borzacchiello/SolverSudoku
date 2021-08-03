from operator import *

class IndicesOfCell(tuple):
    def __new__(self, row : int, column : int):
        IndicesOfCell.row = property(itemgetter(0))
        IndicesOfCell.column = property(itemgetter(1))
        return tuple.__new__(IndicesOfCell, (row, column))