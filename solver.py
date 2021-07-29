from abc import ABC, abstractmethod

from puzzle import *

class Solver(ABC):
    def __init__(self, puzzles_to_solve : Puzzle):
        self.puzzles_to_solve = puzzles_to_solve
    
    @abstractmethod
    def solve(self):
        pass
    
    @abstractmethod
    def get_solution(self) -> Puzzle:
        pass