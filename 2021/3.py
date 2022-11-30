from functools import reduce

total_bit_counts = None
one_bit_counts = None
data = []

while True:
    try:
        text = input()
    except EOFError as ex:
        break
    
    data.append([int(x) for x in text])

one_bit_counts = reduce(lambda x, y: [x[i]+y[i] for i in range(len(x))], data)
total_bit_counts = [len(data) for _ in range(len(data[0]))]

def get_oxygen_rate(data: list, idx: int):
    if idx >= len(data[0]):
        return data[0]
    elif len(data) == 1:
        return data[0]

    one_bit_counts = reduce(lambda x, y: [x[i]+y[i] for i in range(len(x))], data)

    one_bit = one_bit_counts[idx]
    zero_bit = len(data)-one_bit_counts[idx]
    
    expect = 1
    if one_bit < zero_bit:
        expect = 0
    
    return get_oxygen_rate(list(filter(lambda x: x[idx] == expect, data)), idx+1)

def get_co2_rate(data: list, idx: int):
    if idx >= len(data[0]):
        return data[0]
    elif len(data) == 1:
        return data[0]

    one_bit_counts = reduce(lambda x, y: [x[i]+y[i] for i in range(len(x))], data)

    one_bit = one_bit_counts[idx]
    zero_bit = len(data)-one_bit_counts[idx]
    
    expect = 0
    if one_bit < zero_bit:
        expect = 1
    
    return get_co2_rate(list(filter(lambda x: x[idx] == expect, data)), idx+1)

# print(data)
oxygen = get_oxygen_rate(data, 0)
# print(data)
co2 = get_co2_rate(data, 0)

def array_to_num(data: list) -> int:
    total = 0
    for i in range(len(data)):
        total += data[len(data)-i-1]*(2**i)
    return total

oxygen_rate = array_to_num(oxygen)
co2_rate = array_to_num(co2)

print(oxygen_rate)
gamma = ['1' if one_bit_counts[i] > total_bit_counts[i]-one_bit_counts[i] else '0' for i in range(len(one_bit_counts)) ]
epsilon = ['1' if v == '0' else '0' for v in gamma]

print(f'gamma: {"".join(gamma)}')
print(f'epsilon: {"".join(epsilon)}')
gamma_rate = int(''.join(gamma), 2)
epsilon_rate = int(''.join(epsilon), 2)

print(gamma_rate * epsilon_rate)

print(f'oxygen rate: {oxygen_rate} ({oxygen})')
print(f'co2 rate   : {co2_rate} ({co2})')
print(oxygen_rate*co2_rate)