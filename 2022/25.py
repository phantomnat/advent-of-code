inputs = []

input_file = 'input/actual'
# input_file = 'input/example'
with open(input_file, 'r') as fp:
    inputs = fp.readlines()

snafu_to_nums = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2,
}

def to_base_5(num):
    if num == 0:
        return [0]
    arr = []
    while num:
        arr.insert(0, num%5)
        num //= 5
    return arr

def from_snafu(txt):
    total = 0
    for i, c in enumerate(txt):
        total += (5 ** (len(txt)-i-1)) * snafu_to_nums[c]
    return total

def to_snafu(num):
    # txt = ''
    arr = to_base_5(num)
    first = 0

    def addition(i):
        while True:
            if i-1 < 0:
                return 1
            if arr[i-1]+1 < 5:
                arr[i-1] += 1
                return 0
            arr[i-1] = 0
            i -= 1
        
    for i in range(len(arr)-1, -1, -1):
        if arr[i] == 3:
            arr[i] = '='
            first += addition(i)
        elif arr[i] == 4:
            arr[i] = '-'
            first += addition(i)
        else:
            arr[i] = str(arr[i])
    first = '' if first == 0 else str(first)
    return first+''.join(arr)

total = 0
for line in inputs:
    line = line.strip()
    num = from_snafu(line)
    # print(line, '=', num)    
    total += num
    line2 = to_snafu(num)
    assert line2 == line, line + ' vs ' + line2

print('total', total)
print('base 5', to_base_5(total))
print('25.1', to_snafu(total))
