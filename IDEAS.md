## Gameplay
- Pause simulation
- Variable simulation speed (0.5x, 2x, 4x)

## UI
- (FPS counter)
- (Selected unit information)
- (Toggle grid)
- Camera zoom

## AI
- Retreat behavior
- Suppression
- (Flanking)


## Workspace (thinking about ideas)
### Camera/scale
Ideally I want a simulation where you can zoom the camera, which means the scale has to be dependant of the camera zoom. If I have a constant such as `PIXELS_PER_METER`, I can use that to keep movement constant even though I might be zoomed in or out. How would this work:

1. The unit position stored in `unit.x` and `unit.y` is absolute and is simply the "real world position" regardless of camera zoom/scale. It could for example be `unit.x = 1253`, `unit.y = 217` --> `unit.position = (1253,217)`
2. The renderer then has to scale this down to whatever screen size/zoom I'm currently using, which is where `PIXELS_PER_METER` comes in. Say we have `PIXELS_PER_METER = 4`, this means the unit position above would be rendered on:
`rendered_unit_position = (round(unit.x * PIXELS_PER_METER), round(unit.y * PIXELS_PER_METER)) = (313,54)`
3. If my camera is zoomed in, there needs to be some type of conversion such that 2x zoom --> units take up 2x as much space on screen. Say I have a variable called `camera_zoom`. If `camera_zoom = 2` means the size in the `render()` function has to take in `camera_zoom` as an argument, and the size of the unit would be `(INFANTRY_UNIT_SIZE * camera_zoom)` or something along those lines. This way, camera zoom on 1 keeps units a certain size, and zooming in increases the unit size proportional to the zoom. 

The only thing I'm unsure of how to decide which part of the screen would be displayed when you zoom in. I feel like with this implementation, zooming would just increase the size of everything to the point where things might just overlap instead. I would need to zoom in on a subset of the total "war field" but how would I decide that? I if I use mouse scrolling, the cursor would be a center point, around which I can select a portion of the current screen to display on the full screen.



### Movement system
In order to allow a destination point, I first of all have to create fields for destination coordinates, and maybe some getters/setters to update it since it likely won't be static. Then it's a matter of moving towards that destination, which I feel will be some sort of delta coordinate using the difference between where the unit currently is and where it's going. I'm thinking:

**Example**
<pre>
unit.position(x<sub>1</sub>,y<sub>1</sub>)
unit.destination(x<sub>2</sub>,y<sub>2</sub>)
speed = k

coordinate_diff = destination - position = (x<sub>2</sub> - x<sub>2</sub>, y<sub>2</sub> - y<sub>1</sub>)
</pre>

The simplest way for a unit to move between two point would be the shortest distance, i.e. following the diagonal line which could be seen as the vector (dx,dy) where dy, dx is the difference in x and y coordinates respectively. Calculating the normalised vector would give the ratio between x and y speed, which could then be multiplied by whatever speed the unit has i.e the velocity to move towards the point would be:

k * ṽ, where ṽ = (vx,vy) is the normalised vector found by dividing each component by the length of the vector i.e ($\frac{v1}{|v|}$,$\frac{v2}{|v|}$). Using k = 1, ṽ = (4/5, 3/5)

k * ṽ = 1 * (4/5,3/5) = (4/5, 3/5) --> vx = 4/5, vy = 3/5

Since there are currently no obstacles, there isn't really a way to create a pathfinding algorithm. Instead, using the calculation above, the unit will simply move along the diagonal line as shown below:

<img src="Unit_Movement.png" width="200" height="200"/>

I also need a conditional to check if the unit is close enough/on the destination point. In other words, if the distance to the point is less than the distance of the next movement, the unit should be placed on it's destination. Otherwise it will overshoot and rock back and forth. So I need a:

if movement_diff.length  > coordinate_diff.length:
    self.position = self.destination

