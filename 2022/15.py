inputs = []

while True:
    try:
        text = input()
    except EOFError as ex:
        break
    inputs.append(text)

# print('\n'.join(inputs))

def get_num(txt: str) -> int:
    return int(txt.strip(',:').split('=')[1])

lands = {}
top_left = [100000,100000]
bot_right = [0,0]
sensors = []
sensors2 = []

def update_border(x, y):
    top_left[0] = min(top_left[0], x)
    top_left[1] = min(top_left[1], y)
    
    bot_right[0] = max(bot_right[0], x)
    bot_right[1] = max(bot_right[1], y)

def mdist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

for line in inputs:
    arr = line.split()
    sensor = (get_num(arr[2]), get_num(arr[3]))
    beacon = (get_num(arr[8]), get_num(arr[9]))

    top_left[0] = min(top_left[0], sensor[0], beacon[0])
    top_left[1] = min(top_left[1], sensor[1], beacon[1])
    
    bot_right[0] = max(bot_right[0], sensor[0], beacon[0])
    bot_right[1] = max(bot_right[1], sensor[1], beacon[1])
    
    dist = mdist(sensor, beacon)
    # print(f'sensor: {sensor}, beacon: {beacon}, dist: {dist}')
    lands[sensor] = 'S'
    lands[beacon] = 'B'
    sensors.append((sensor, dist))
    sensors2.append((sensor, dist))
    
# print(top_left, bot_right)

def within_range(x, y, sensors):
    for j in range(len(sensors)):
        dist = sensors[j][1]
        if mdist(sensors[j][0], (x, y)) <= dist:
            return True
    
    return False

def print_lands():
    for y in range(top_left[1], bot_right[1]+1):
        line = ''
        for x in range(top_left[0], bot_right[0]+1):
            if (x, y) in lands:
                line += lands[(x, y)]
            elif within_range(x, y, sensors):
                line += '#'
            else:
                line += '.'
        print(line)

# print_lands()

# target_y = 10
target_y = 2000000

for i in range(len(sensors)):
    sensor, dist = sensors[i]
    
    # print(f'check sensor: {sensor}')

    sx, sy = sensor[0], target_y
    
    # left_dist = dist - nearest
    radius = 0
    while mdist(sensor, (sx+radius, sy)) <= dist:
        # if (sx-radius, sy) not in lands:
            # lands[(sx-radius, sy)] = '#'
        if (sx+radius, sy) not in lands:
            lands[(sx+radius, sy)] = '#'
        # update_border(sx-radius, sy)
        update_border(sx+radius, sy)
        radius += 1
    
    radius = 0
    while mdist(sensor, (sx+radius, sy)) <= dist:
        # if (sx-radius, sy) not in lands:
            # lands[(sx-radius, sy)] = '#'
        if (sx+radius, sy) not in lands:
            lands[(sx+radius, sy)] = '#'
        # update_border(sx-radius, sy)
        update_border(sx+radius, sy)
        radius -= 1
    

# # line = ''
count = 0
y = target_y
for x in range(top_left[0], bot_right[0]+1):
    if (x, y) in lands and lands[(x, y)] == '#':
        count += 1

print(f'15.1: {count}')

# print()
# print_lands()


# max_coor = 20
max_coor = 4000000

top_left[0] = max(0, top_left[0])
top_left[1] = max(0, top_left[1])
bot_right[0] = min(bot_right[0], max_coor)
bot_right[1] = min(bot_right[1], max_coor)


def is_found(x, y, lands, sensors, skip):
    if x < 0 or y < 0 or x > max_coor or y > max_coor:
        return False
    elif (x, y) in lands:
        return False

    for j in range(len(sensors)):
        dist = sensors[j][1]
        if mdist(sensors[j][0], (x, y)) <= dist:
            return False
    
    print(f'15.2: {x},{y} = {x*4000000+y}')
    return True

for i in range(len(sensors)):
    sensor, dist = sensors[i]

    # print(f'check sensor: {sensor}')
    
    # right to down
    sx, sy = sensor[0]+dist+1, sensor[1]
    while sx >= sensor[0]:
        if is_found(sx, sy, lands, sensors, i):
            break
        sx -= 1
        sy += 1

    # down to left
    sx, sy = sensor[0], sensor[1]+dist+1
    while sy > sensor[1]:
        if is_found(sx, sy, lands, sensors, i):
            break
        sx -= 1
        sy -= 1
    # left to top
    sx, sy = sensor[0]-dist-1, sensor[1]
    while sx < sensor[0]:
        if is_found(sx, sy, lands, sensors, i):
            break
        sx += 1
        sy -= 1
    # top to right
    sx, sy = sensor[0], sensor[1]-dist-1
    while sy < sensor[1]:
        if is_found(sx, sy, lands, sensors, i):
            break
        sx += 1
        sy += 1

