class Infantry:

    def __init__(self, x, y, vx, vy):
        self.x = x         
        self.y = y          
        self.vx = vx        # Velocity in the x plane, pixels/second
        self.vy = vy        # Velocity in the y plane, pixels/second

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt