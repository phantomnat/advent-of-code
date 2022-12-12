inputs = []

while True:
    try:
        text = input()
    except EOFError as ex:
        break
    inputs.append(text)

# print('\n'.join(inputs))

visits = set()

head = (0,0)
tail = (0,0)
ropes = [(0,0) for i in range(10)]

visits.add(tail)

def is_touch(head, tail)->bool:
    return abs(head[0]-tail[0]) <= 1 and abs(head[1]-tail[1]) <=1

for line in inputs:
    direction, length = line.split()
    length = int(length)
    
    for i in range(length):
        if direction == 'R':
            head = (head[0]+1, head[1])
            if not is_touch(head, tail):
                tail = (head[0]-1, head[1])
                # visits.add(tail)
        elif direction == 'L':
            head = (head[0]-1, head[1])
            if not is_touch(head, tail):
                tail = (head[0]+1, head[1])
        elif direction == 'U':
            head = (head[0], head[1]-1)
            if not is_touch(head, tail):
                tail = (head[0], head[1]+1)
        elif direction == 'D':
            head = (head[0], head[1]+1)
            if not is_touch(head, tail):
                tail = (head[0], head[1]-1)

        visits.add(tail)

# print(visits)
print(f'9.1: {len(list(visits))}')


visits = set()

ropes = [(0,0) for i in range(10)]

visits.add(ropes[-1])


for line in inputs:
    direction, length = line.split()
    length = int(length)
    
    for i in range(length):
        if direction == 'R':
          ropes[0] = (ropes[0][0]+1, ropes[0][1])
          
        elif direction == 'L':
          ropes[0] = (ropes[0][0]-1, ropes[0][1])
           
        elif direction == 'U':
          ropes[0] = (ropes[0][0], ropes[0][1]-1)
           
        elif direction == 'D':
          ropes[0] = (ropes[0][0], ropes[0][1]+1)
        
        for i in range(1, 10):
            if not is_touch(ropes[i-1], ropes[i]):
                # move to head
                if abs(ropes[i-1][0]-ropes[i][0]) == 0:
                    if ropes[i-1][1] > ropes[i][1]:
                        ropes[i] = (ropes[i-1][0], ropes[i-1][1]-1)
                    else:
                        ropes[i] = (ropes[i-1][0], ropes[i-1][1]+1)
                        
                elif abs(ropes[i-1][1]-ropes[i][1]) == 0:
                    if ropes[i-1][0] > ropes[i][0]:
                        ropes[i] = (ropes[i-1][0]-1, ropes[i-1][1])
                    else:
                        ropes[i] = (ropes[i-1][0]+1, ropes[i-1][1])
                else:
                    if ropes[i-1][0] > ropes[i][0] and ropes[i-1][1] > ropes[i][1]:
                        # move down right
                        ropes[i] = (ropes[i][0]+1, ropes[i][1]+1)
                    elif ropes[i-1][0] > ropes[i][0] and ropes[i-1][1] < ropes[i][1]:
                        # move down right
                        ropes[i] = (ropes[i][0]+1, ropes[i][1]-1)
                        
                    elif ropes[i-1][0] < ropes[i][0] and ropes[i-1][1] < ropes[i][1]:
                        # move down right
                        ropes[i] = (ropes[i][0]-1, ropes[i][1]-1)
                    
                    elif ropes[i-1][0] < ropes[i][0] and ropes[i-1][1] > ropes[i][1]:
                        # move down right
                        ropes[i] = (ropes[i][0]-1, ropes[i][1]+1)
                    # move diagonal

        visits.add(ropes[-1])

print(f'9.2: {len(list(visits))}')