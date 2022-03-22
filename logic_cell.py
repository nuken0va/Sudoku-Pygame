from dataclasses import dataclass

class Cell:
    index: int
    candidates: set[int]
    __value: int
    __fixed: bool
    __fixed_candidates: list[int]
    __current_candidate: list[int]

    def __init__(self, index: int, value: int, candidates: set):
        self.index = index
        self.candidates = candidates
        self.__value = value
        self.__fixed = bool(self.__value)
        self.__fixed_candidates = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value): 
        self.__fixed = True
        self.__value = value 

    @property
    def fixed(self): return self.__fixed

    def fix_candidate(self):
        self.__fixed_candidates = list(self.candidates)
        self.__current_candidate = 0

    def next_candidate(self):
        if self.__fixed_candidates is None:
            self.fix_candidate()
        if self.__current_candidate < len(self.__fixed_candidates):
            self.__value = self.__fixed_candidates[self.__current_candidate]
            self.__current_candidate += 1
            return 1
        else: 
            return 0
    
    def reset_candidate(self):
        self.__current_candidate = 0

    def __hash__(self):
        return self.index

    def to_id(x, y):
        """Converts x,y coordinates of cell to cell id (index)"""
        return x + y * 9

    def to_cord(index):
        """Converts cell id (index) of cell to  its x,y coordinates"""
        return index // 9, index % 9

    def copy(self):
        return Cell(self.copy, self.value, self.candidates.copy())
