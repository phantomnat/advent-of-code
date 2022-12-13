inputs = []

while True:
    try:
        text = input()
    except EOFError as ex:
        break
    inputs.append(text)

# print('\n'.join(inputs))

def compare(a, b) -> int:
    # print(f'compare: {a} vs {b}')
    
    if a is None and b is not None:
        return 0
    elif a is not None and b is None:
        return -1
    elif a is None and b is None:
        return 1
    elif type(a) is int and type(b) is int:
        if a == b:
            return 0
        return 1 if a < b else -1

    if type(a) is int:
        a = [a]
    if type(b) is int:
        b = [b]
    n = max(len(a), len(b))
    
    for i in range(n):
        if i >= len(a) and i < len(b):
            return 1
        elif i >= len(b) and i < len(a):
            return -1
        
        c = compare(a[i], b[i])
        if c == 1:
            return 1
        elif c == -1:
            return -1

    return 0

total = 0
for i in range(0, len(inputs), 3):
    idx = (i//3) + 1
    a = eval(inputs[i])
    b = eval(inputs[i+1])
    result = compare(a, b)
    if result == 1:
        total += idx
    # print(f'{idx} => {result}')

print(f'13.1: {total}')

array = [[[2]], [[6]]]

for line in inputs:
    if not line:
        continue
    array.append(eval(line))

def get_key(x):
    if type(x) is list:
        if not x:
            return 0
        return get_key(x[0])
    return x

sorted_packets = sorted(array, key=get_key)
two = sorted_packets.index([[2]])+1
six = sorted_packets.index([[6]])+1

print(f'13.2: {two*six}')