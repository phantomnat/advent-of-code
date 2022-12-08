inputs = []

while True:
    try:
        text = input()
    except EOFError as ex:
        break
    inputs.append(text)

# print('\n'.join(inputs))

edges = (len(inputs)+len(inputs[0])-2)*2
internal = 0
h = len(inputs)
w = len(inputs[0])

def is_visible(forest: list, w: int, h: int, x: int, y: int)->int:
    # left
    tree_h = forest[y][x]
    
    left_ok = True
    for i in range(0, x):
        if forest[y][i] >= tree_h:
            left_ok = False
            break
    if left_ok:
        return 1
    
    right_ok = True
    for i in range(x+1, w):
        if forest[y][i] >= tree_h:
            right_ok = False
            break
    if right_ok == True:
        return 1
    
    top_ok = True
    for i in range(0, y):
        if forest[i][x] >= tree_h:
            top_ok = False
            break
    if top_ok == True:
        return 1
    
    bottom_ok = True
    for i in range(y+1, h):
        if forest[i][x] >= tree_h:
            bottom_ok = False
            break
    if bottom_ok == True:
        return 1
    
    return 0

for y in range(1, h-1):
    for x in range(1, w-1):
        internal += is_visible(inputs, w, h, x, y)

total = edges+internal
print(f'8.1: {total}')

scenic_score = 0

def find_scenic(forest: int, w: int, h: int, x: int, y: int):
    score = 0
    # left
    tree_h = forest[y][x]
    
    left = 0
    for i in range(x-1, -1, -1):
        left += 1
        if forest[y][i] >= tree_h:
            break

    right = 0
    for i in range(x+1, w):
        right += 1
        if forest[y][i] >= tree_h:
            break

    top = 0
    for i in range(y-1, -1, -1):
        top += 1
        if forest[i][x] >= tree_h:
            break
    
    bottom = 0
    for i in range(y+1, h):
        bottom += 1
        if forest[i][x] >= tree_h:
            break
    
    return left*right*top*bottom
    
for y in range(1, h-1):
    for x in range(1, w-1):
        scenic_score = max(scenic_score, find_scenic(inputs, w, h, x, y))

print(f'8.2: {scenic_score}')
