class Faction:

    def __init__(self,
                 name,
                 color,
                 wounded_color,
                 heavily_wounded_color,
                 spawn_point,
                 retreat_point,
                 objective):
        
        self.name = name

        self.color = color
        self.wounded_color = wounded_color
        self.heavily_wounded_color = heavily_wounded_color

        self.spawn_point = spawn_point
        self.retreat_point = retreat_point
        self.objective = objective

    