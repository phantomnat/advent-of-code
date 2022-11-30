count = 0
total = 0

while True:
    try:
        text = input()
        # output = input()
    except EOFError as ex:
        break
    patterns, output = text.split(' | ')
    # print(patterns)
    numbers = output.split()
    # print(numbers)
  
    # determine the patterns
    patterns = [set(p) for p in patterns.split(' ')]
    mapping = {i: set() for i in range(10)}
    segments = {i: '' for i in range(7)}

    for p in patterns:
        if len(p) == 2:
            mapping[1] = p.copy()
            count += 1
        elif len(p) == 3:
            mapping[7] = p.copy()
            count += 1
        elif len(p) == 4:
            mapping[4] = p.copy()
            count += 1
        elif len(p) == 7:
            mapping[8] = p.copy()
            count += 1
    
    # find 3,2,5
    for p in patterns:
        if len(p) == 5:
            if len(p - mapping[1]) == 3:
                mapping[3] = p.copy()
            elif len(p - mapping[4]) == 3:
                mapping[2] = p.copy()
            else:
                mapping[5] = p.copy()
        elif len(p) == 6:
            if len(p - mapping[1]) == 5:
                mapping[6] = p.copy()
            elif len(p - mapping[4]) == 2:
                mapping[9] = p.copy()
            else:
                mapping[0] = p.copy()
    
    patterns_to_number = {tuple(sorted(list(v))): k for k,v in mapping.items()}
    
    def to_num(v: str) -> int:
        return patterns_to_number[tuple(sorted(list(v)))]
    
    total += sum([to_num(v)*(10**(3-i)) for i, v in enumerate(numbers)])
            
print(f'count: {count}')
print(f'total: {total}')