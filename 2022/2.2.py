
pairs = []

while True:
    try:
        text = input()
    except EOFError as ex:
        break

    op, elf = text.split()
    
    pairs.append((op, elf))
    # print(op, elf)

scores = {
    'A': 1, # rock
    'B': 2, # paper
    'C': 3, # scissor
}

lose_map = {
    'A': 'C',
    'B': 'A',
    'C': 'B',
}
win_map = {
    'A': 'B',
    'B': 'C',
    'C': 'A',
}
score = 0

for op, elf in pairs:
    
    if elf == 'X':
        # lose
        score += scores[lose_map[op]]
    elif elf == 'Y':
        # draw
        score += 3 + scores[op]
    else:
        # win
        score += 6 + scores[win_map[op]]

print(score)