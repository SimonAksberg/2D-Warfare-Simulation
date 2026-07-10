import constants
from vector2 import Vector2

class SpatialGrid:

    def __init__(self):
        self.cell_size = constants.CELL_SIZE
        self.cells = {}

    def get_cell(self,position):
        cell_x = int(position.x // self.cell_size)
        cell_y = int(position.y // self.cell_size)

        # Makes the key a tuple, might be better to change to Vector2 later?
        return (cell_x, cell_y)
    
    def clear(self):
        self.cells.clear()

    def insert(self,unit):
        cell = self.get_cell(unit.position)

        if cell not in self.cells:
            self.cells[cell] = []
        
        self.cells[cell].append(unit)
