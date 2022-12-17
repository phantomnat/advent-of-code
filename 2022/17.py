inputs = []

while True:
    try:
        text = input()
    except EOFError as ex:
        break
    inputs.append(text)

# print('\n'.join(inputs))

rocks = [
    ['@@@@'], 
    
    [' @ ',
     '@@@',
     ' @ ',], 
    
    ['@@@',
     '  @',
     '  @'], 
    
    ['@',
     '@',
     '@',
     '@'],
    
    ['@@',
     '@@'],
]
winds = inputs[0]

def run_simulation(n: int, find_pattern = False) -> int:
    rock_count = 0
    wind = 0
    cave = []

    def draw_rock(rock_id, rx, ry):
        for y, row in enumerate(rocks[rock_id]):
            for x, r in enumerate(list(row)):
                if r == ' ':
                    continue
                nx = rx + x
                ny = ry + y
                if ny >= len(cave):
                    cave.append([' ' for _ in range(7)])
                cave[ny][nx] = '#'

    def move_rock_aside(rock_id, rx, ry, dx):
        nx = rx+dx
        ny = ry
        w = len(rocks[rock_id][0])
        if nx < 0 or nx + w > 7:
            return rx, ry
        for y, row in enumerate(rocks[rock_id]):
            for x, r in enumerate(list(row)):
                if r == ' ':
                    continue
                new_x = nx + x
                new_y = ny + y
                if new_y >= len(cave):
                    # ignore outside cave
                    continue
                if cave[new_y][new_x] != ' ':
                    return rx, ry
        return nx, ny

    def move_rock_down(rock_id, rx, ry):
        nx = rx
        ny = ry-1
        if ny == -1:
            return False, rx, ry
        for y, row in enumerate(rocks[rock_id]):
            new_y = ny + y
            if new_y >= len(cave):
                # ignore outside cave
                continue
            for x, r in enumerate(list(row)):
                if r == ' ':
                    continue
                new_x = nx + x
                
                if cave[new_y][new_x] != ' ':
                    return False, rx, ry
        return True, nx, ny

    def print_cave():
        for i in range(len(cave)-1,-1,-1):
            print('|'+''.join(cave[i])+'|')
        print()

    changes = []
    last_h_and_rock = [0, 0]
    
    while rock_count < n:

        rock_id = rock_count % len(rocks)
    
        # create rock
        rx, ry = 2, len(cave)+3
        
        # move rock
        while True:
            assert winds[wind % len(winds)] == '>' or winds[wind % len(winds)] == '<'
            wind_dir = 1 if winds[wind % len(winds)] == '>' else -1
            
            rx, ry = move_rock_aside(rock_id, rx, ry, wind_dir)
            is_fell, rx, ry = move_rock_down(rock_id, rx, ry)
            
            if find_pattern and wind % len(winds) == 0 and rock_count > 0:
                changes.append((len(cave)- last_h_and_rock[0], rock_count-last_h_and_rock[1]))
                last_h_and_rock = [len(cave), rock_count]
                if len(changes) > 50:
                    return changes

            wind += 1

            if not is_fell:
                # draw rock
                draw_rock(rock_id, rx, ry)
                break

        rock_count += 1
        
        # print_cave()

    return len(cave)

print(f'17.1: {run_simulation(2022)}')

target_rock = 1_000_000_000_000

def detect_cycle(changes):
    for i, c in enumerate(changes):
        found = False
        for j, c2 in enumerate(changes):
            if i == j:
                continue
            if c == c2:
                found = True
                length = j-i
                break
        if not found:
            continue
        same = True
        for j in range(i+length,i+(length*3)+1,length):
            for k in range(length):
                if changes[i+k] != changes[j+k]:
                    same = False
                    break
            if not same:
                break
        if same:
            return True, i, length
    return False, 0, 0

changes = run_simulation(target_rock, True)
# print(changes)
cycle_found, cycle_index, cycle_length = detect_cycle(changes)
assert cycle_found

# calculate cycle prefix
prefix_rock, prefix_h = 0, 0
for i in range(cycle_index):
    prefix_rock += changes[i][1]
    prefix_h += changes[i][0]

cycle_rock, cycle_h = 0, 0
for i in range(cycle_length):
    cycle_rock += changes[i+cycle_length][1]
    cycle_h += changes[i+cycle_length][0]

# print(f'cycle: {changes[cycle_index:cycle_index+cycle_length]}')
# print(f'prefix: rock={prefix_rock}, h={prefix_h}')
# print(f'cycle : rock={cycle_rock}, h={cycle_h}')

calc_rock = target_rock - prefix_rock
height = prefix_h + ((calc_rock // cycle_rock) * cycle_h)
leftover = calc_rock % cycle_rock

height += run_simulation(prefix_rock+leftover)-prefix_h

print(f'17.2: {height}')