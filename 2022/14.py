inputs = []

while True:
    try:
        text = input()
    except EOFError as ex:
        break
    inputs.append(text)

# print('\n'.join(inputs))

maps = {}

top_left = [500, 0]
bot_right = [500, 0]

for line in inputs:
    coords = [[int(y) for y in x.split(',')] for x in line.split(' -> ')]
    
    # print(coords)
    
    for i in range(1, len(coords)):
        x1, y1 = coords[i-1][0], coords[i-1][1]
        x2, y2 = coords[i][0], coords[i][1]

        top_left[0] = min(top_left[0], x1, x2)
        top_left[1] = min(top_left[1], y1, y2)
        bot_right[0] = max(bot_right[0], x1, x2)
        bot_right[1] = max(bot_right[1], y1, y2)

        if x1 == x2:
            if y1 > y2:
                y1, y2 = y2, y1

            for y in range(y1, y2+1):
                maps[(x1, y)] = '#'

        elif y1 == y2:
            if x1 > x2:
                x1, x2 = x2, x1

            for x in range(x1, x2+1):
                maps[(x, y1)] = '#'
        else:
            print(f'not expected: {x1},{y1}')

def print_map():
    for y in range(top_left[1], bot_right[1]+1):
        line = ''
        for x in range(top_left[0], bot_right[0]+1):
            if x == 500 and y == 0:
                line += '+'
            elif (x, y) in maps:
                line += maps[(x, y)]
            else:
                line += '.'
                
        print(line)

# add sand
sand = 0
while True:
    sx, sy = 500, 0
    
    abyss = False
    
    while True:
        if (sx-1, sy+1) in maps and (sx, sy+1) in maps and (sx+1, sy+1) in maps:
            maps[(sx, sy)] = 'o'
            break
        
        new_y_ok = sy+1 <= bot_right[1]
        
        if new_y_ok and (sx, sy+1) not in maps:
            # fall
            sy += 1
        elif new_y_ok and sx-1 >= top_left[0] and (sx-1, sy+1) not in maps:
            # fall left
            sy += 1
            sx -= 1
        elif new_y_ok and sx+1 <= bot_right[0] and (sx+1, sy+1) not in maps:
            # fall right
            sy += 1
            sx += 1
        else:
            abyss = True
            break

    if abyss:
        break
  
    sand += 1
    # print_map()

print(f'14.1: {sand}')

# add line
add = 10000
for x in range(top_left[0]-add, bot_right[0]+add+1):
    maps[(x, bot_right[1]+2)] = '#'
bot_right[1] += 2
top_left[0] -= add
bot_right[0] += add

print_map()

while True:
    sx, sy = 500, 0

    if (sx-1, sy+1) in maps and (sx, sy+1) in maps and (sx+1, sy+1) in maps:
        sand += 1
        break

    while True:
        if (sx-1, sy+1) in maps and (sx, sy+1) in maps and (sx+1, sy+1) in maps:
            maps[(sx, sy)] = 'o'
            break
        
        new_y_ok = sy+1 <= bot_right[1]
        
        if new_y_ok and (sx, sy+1) not in maps:
            # fall
            sy += 1
        elif new_y_ok and (sx-1, sy+1) not in maps:
            # fall left
            sy += 1
            sx -= 1
        elif new_y_ok and (sx+1, sy+1) not in maps:
            # fall right
            sy += 1
            sx += 1
        else:
            abyss = True
            break

    sand += 1
    # if sand % 1000 == 0:
    #     print_map()
    
print(f'14.2: {sand}')

