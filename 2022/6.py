inputs = []

while True:
    try:
        text = input()
    except EOFError as ex:
        break
    inputs.append(text)

print('\n'.join(inputs))

mem = set()

for i in range(4, len(text)):
    # print(text[i-4:i])
    if len(set(text[i-4:i])) == 4:
        print(f'4: {i}')
        break
            
mem = set()
for i in range(14, len(text)):
    # print(text[i-14:i])
    if len(set(text[i-14:i])) == 14:
        print(f'14: {i}')
        break

    