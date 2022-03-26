from dataclasses import dataclass

@dataclass
class Move:
    value : int
    prev_value : int