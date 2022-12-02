elves = [[]]
elf_idx = 0

while True:
    try:
        text = input()
    except EOFError as ex:
        break
    
    if text == '':
        elves.append([])
        elf_idx += 1
        continue
    
    elves[elf_idx].append(int(text))

total_elves = [sum(v) for i, v in enumerate(elves)]
print(elves)
print(max(total_elves))

sorted_total_cal = sorted(total_elves, key=lambda x: -x)
print(sum(sorted_total_cal[:3]))