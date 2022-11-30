
numbers = [int(x) for x in input().split(',')]

boards = []
boards_idx = -1

while True:
    try:
        text = input()
    except EOFError as ex:
        break
    
    if text == '':
        boards.append([])
        boards_idx += 1
        continue
    boards[boards_idx].append([int(x) for x in text.split()])

print(numbers)

masks = [[[0]*5 for _ in range(5)] for _ in range(len(boards))]

draw_idx = 0

def mark_board(boards: list, masks: list, idx: int, number: int):
    for y in range(5):
        for x in range(5):
            if boards[idx][y][x] == number:
                masks[idx][y][x] = 1
                return

def check_winner(mask: list) -> bool:
    # - horizontal -
    for y in range(5):
        if sum(mask[y]) == 5:
            return True
    # | vertical |
    for x in range(5):
        # if mask[4][x] + mask[3][x] + mask[2][x] + mask[1][x] + mask[0][x] == 5:
            # return True

        if sum([mask[y][x] for y in range(5)]) == 5:
            return True

    # # diagonal
    # if sum([mask[x][x] for x in range(5)]) == 5:
    #     return True
    # if mask[4][0] + mask[3][1] + mask[2][2] + mask[1][3] + mask[0][4] == 5:
    #     return True
    return False

  
def print_boards(boards: list):
    for board in boards:
        print(board)
        print()

print_boards(boards)
print_boards(masks)

win_count = 0
is_wins = [False for _ in range(len(boards))]

# is_win = False    
while win_count < len(boards):
    # draw
    number = numbers[draw_idx]
    
    print(f'draw: {number}')
    # mark
    for i in range(len(boards)):
        mark_board(boards, masks, i, number)
    
    # check winner
    for i in range(len(boards)):
        if not is_wins[i] and check_winner(masks[i]):
            win_count += 1
            is_wins[i] = True
            if win_count == len(boards):
                print(f'winner is board {i}')
                print_boards(boards)
                print_boards(masks)
                
                unmark = 0
                for y in range(5):
                    for x in range(5):
                        if masks[i][y][x] == 0:
                            unmark += boards[i][y][x]
                
                print(f'ans: {unmark*number}')

    draw_idx += 1
  