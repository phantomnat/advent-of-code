def get_points(text: str):
    pt_from, pt_to = text.split(' -> ')
    x1, y1 = [int(x) for x in pt_from.split(',')]
    x2, y2 = [int(x) for x in pt_to.split(',')]
    return (x1, y1), (x2, y2)

mem = {}
count = 0
is_diagonal_included = True

while True:
    try:
        text = input()
    except EOFError:
        break

    # print(text)
    (x1, y1), (x2, y2) = get_points(text)
    # print(f'({x1}, {y1}), ({x2}, {y2})')
    
    if x1 == x2:
        start_y = y1 if y1 < y2 else y2
        end_y = y1 if y1 > y2 else y2
        y = start_y
        while y <= end_y:
            mem[(x1, y)] = mem.get((x1, y), 0)+1
            if mem[(x1, y)] == 2:
                count+=1
            y+=1
    elif y1 == y2:
        start_x = x1 if x1 < x2 else x2
        end_x = x1 if x1 > x2 else x2
        x = start_x
        while x <= end_x:
            mem[(x, y1)] = mem.get((x, y1), 0)+1
            if mem[(x, y1)] == 2:
                count+=1
            x+=1
    elif is_diagonal_included and abs(x1-x2) == abs(y1-y2):
        step_y = 1
        if x1 < x2:
            start_x, end_x = x1, x2
            start_y = y1
            if y1 > y2:
                step_y = -1
        else:
            start_x, end_x = x2, x1
            start_y = y2
            if y2 > y1:
                step_y = -1
        
        x = start_x
        y = start_y
        while x <= end_x:
            mem[(x, y)] = mem.get((x, y), 0)+1
            if mem[(x, y)] == 2:
                count += 1
            x += 1
            y += step_y

for i in range(10):
    line = ''
    for j in range(10):
        v = mem.get((j, i), 0)
        if v == 0:
            line += '.'
        else:
            line += str(v)
    
    print(line)
    
print(f'count: {count}')