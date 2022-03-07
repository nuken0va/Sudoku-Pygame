from dataclasses import dataclass

@dataclass
class Point:
    x : int
    y : int

@dataclass
class Move:
    pos : Point
    value : int
    prev_value : int