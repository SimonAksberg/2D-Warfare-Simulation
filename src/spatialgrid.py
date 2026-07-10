import constants
import math

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
    
    def query_radius(self, position, radius):
        cell_x, cell_y = self.get_cell(position)

        radius_in_cells = math.ceil(radius / self.cell_size)

        nearby_units = []

        # Calculates square of cells around unit position to be searched
        min_cell_x = cell_x - radius_in_cells
        max_cell_x = cell_x + radius_in_cells

        min_cell_y = cell_y - radius_in_cells
        max_cell_y = cell_y + radius_in_cells

        for cell_x in range(min_cell_x, max_cell_x + 1):
            if cell_x < 0:
                continue

            for cell_y in range(min_cell_y, max_cell_y + 1):
                if cell_y < 0:
                    continue

                cell = (cell_x, cell_y)

                if cell in self.cells:
                    nearby_units.extend(self.cells[cell])
        
        return nearby_units

