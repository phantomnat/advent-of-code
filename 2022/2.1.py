
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
    
    'A-B': 6,
    'A-C': 0,
    
    'B-A': 0,
    'B-C': 6,
    
    'C-A': 6,
    'C-B': 0
}

mapping =  {
    'X': 'A',
    'Y': 'B',
    'Z': 'C',
}

score = 0

for op, elf in pairs:
    my = mapping[elf]
    score += scores[my]
    if op == my:
        score += 3
    else:
        score += scores[f'{op}-{my}']

print(score)