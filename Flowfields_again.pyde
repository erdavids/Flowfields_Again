w, h = 1000, 1000

left_x = int(w * -0.5)
right_x = int(w * 1.5)
top_y = int(h * -0.5)
bottom_y = int(h * 1.5) 

resolution = int(w * .01)

# Border width around entire image
bw = .8

noise_scale = .2

num_columns = (right_x - left_x) / resolution
num_rows = (bottom_y - top_y) / resolution

num_curves = 10000
num_steps = 1000
step_length = .02

#Essentially separation between the lines
d_sep = 12

grid_width = 100
grid_height = 100

cell_width = float(w)/grid_width
cell_height = float(h)/grid_height


points = []
check_grid = []

def get_grid_position(x, y):
    return int(x/cell_width) + int(y/cell_height) * grid_width 
        
def distance(p1_x, p1_y, p2_x, p2_y):
    return sqrt(pow(p1_x - p2_x, 2) + pow(p1_y - p2_y, 2))
    
def check_valid_position(position, id):
    if (position[0] < -w/2 * bw or position[0] > w/2 * bw or position[1] < -h/2 * bw or position[1] > h/2 * bw):
        return False
    
    grid_position = int(get_grid_position(position[0], position[1]))
    
    compare_list = []

    for c in points[grid_position]:
        compare_list.append(c)
        
    if (grid_position % grid_width > 0):
        for c in points[grid_position - 1]:
            compare_list.append(c)
            
    if (grid_position % grid_width < grid_width - 1):
        for c in points[grid_position + 1]:
            compare_list.append(c)
            
    if (grid_position >= grid_width):
        for c in points[grid_position - grid_width]:
            compare_list.append(c)
            
    if (grid_position < (grid_width * grid_height) - grid_width):
        for c in points[grid_position + grid_width]:
            compare_list.append(c)
            
    if (grid_position % grid_width > 0 and grid_position > grid_width):
        for c in points[grid_position - grid_width - 1]:
            compare_list.append(c)
            
    if (grid_position % grid_width > 0 and grid_position < (grid_width * grid_height) - grid_width):
        for c in points[grid_position + grid_width - 1]:
            compare_list.append(c)
            
    if (grid_position % grid_width < grid_width - 1 and grid_position > grid_width):
        for c in points[grid_position - grid_width + 1]:
            compare_list.append(c)
    
    if (grid_position % grid_width < grid_width - 1 and grid_position < (grid_width * grid_height) - grid_width):
        for c in points[grid_position + grid_width + 1]:
            compare_list.append(c)
    
    valid = True
    for c in compare_list:
        if (c[2] != id):
            distance = sqrt(pow(c[1] - position[1], 2) + pow(c[0] - position[0], 2))
            if (distance < d_sep):
                valid = False
    
    if (valid == True):
        points[grid_position].append([position[0], position[1], id])
    return valid
        
def setup():
    size(w, h)

    # background('#7B9CE9');
    background('#FCF5E5')
    pixelDensity(2)
    points = []
    # Center
    stroke('#000000')
    strokeWeight(1)
    
    
    stroke('#F25757')
    fill('#F25757')
    pushMatrix()
    translate(w* .5, h * .1)
    draw_layer()
    
    # points = []
    
    stroke('#53B3CB')
    fill('#53B3CB')
    popMatrix()
    pushMatrix()
    translate(w * .5, h * .9)
    draw_layer()
    
    points = []
    
    # stroke('#a12867')
    # noFill()
    # draw_layer()
    
    
def draw_layer():
    noiseSeed(int(random(10000)))
    for i in range(grid_width * grid_height):
        if (len(points) > i):
            points[i] = []
        else:
            points.append([])
    
    # noFill()
    
    grid = []
    for c in range(num_columns):
        grid.append([])
        for r in range(num_rows):
            angle = noise(c * noise_scale, r * noise_scale) * (2 * PI)
            # rem = angle % PI/6
            # if (rem !=0):
            #     angle = angle + PI/6 - rem
            grid[c].append(angle)
            # grid[c].append(random(2 * PI))

        
    for k in range(num_curves):
        orig_x = int(random(-w/2, w/2))
        orig_y = int(random(-h/2, h/2))
        
        curve_x = orig_x
        curve_y = orig_y
    
        # noFill()
        beginShape()
        pts = []
        for i in range(num_steps/2):
            if check_valid_position((curve_x, curve_y), k) == False:
                break
            
            # vertex(curve_x, curve_y)
            # pts.append([curve_x, curve_y])
            circle(curve_x, curve_y, 10)
            
            x_offset = curve_x - left_x
            y_offset = curve_y - top_y
        
            column_index = int(x_offset / resolution)
            row_index = int(y_offset / resolution)
            
            grid_angle = grid[column_index][row_index]
            
            x_step = step_length * cos(grid_angle)
            y_step = step_length * sin(grid_angle)
            
            curve_x = curve_x + x_step
            curve_y = curve_y + y_step
            
            # pushMatrix()
            # translate(curve_x, curve_y)
            # rotate(grid_angle)
            # rect(0, 0, 5, 5)
            # popMatrix()
        
        endShape()
        
        curve_x = orig_x
        curve_y = orig_y
        # noFill()
        beginShape()
        for i in range(num_steps/2):
            if check_valid_position((curve_x, curve_y), k) == False:
                break
            
            # vertex(curve_x, curve_y)
            circle(curve_x, curve_y, 10)
            
            x_offset = curve_x - left_x
            y_offset = curve_y - top_y
        
            column_index = int(x_offset / resolution)
            row_index = int(y_offset / resolution)
            
            grid_angle = grid[column_index][row_index]
            
            x_step = step_length * cos(grid_angle)
            y_step = step_length * sin(grid_angle)
            
            curve_x = curve_x - x_step
            curve_y = curve_y - y_step
            
            # pushMatrix()
            # translate(curve_x, curve_y)
            # rotate(grid_angle)
            # rect(0, 0, 5, 5)
            # popMatrix()
        
        endShape()
        
    save("Examples/" + str(int(random(10000))) + ".png")
    
    
