from spatialgrid import SpatialGrid

class World:

    def __init__(self):
        self.units = []
        self.allies = []
        self.enemies = []
        self.projectiles = []
        self.grid = SpatialGrid()
        self.destinations =[]