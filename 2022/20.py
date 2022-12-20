inputs = []

input_file = 'input/actual'
# input_file = 'input/example'
with open(input_file, 'r') as fp:
    inputs = fp.readlines()
    
# print(inputs)

nums = [int(x.strip()) for x in inputs]
N = len(nums)

# print(nums)

class ListNode:
    def __init__(self, v, p=None, n=None) -> None:
        self.v = v
        self.prev = p
        self.next = n
    def __repr__(self) -> str:
        return f'{self.v}'

    def shift(self, n):
        p = self
        for _ in range(n):
            p = p.next
        return p

# build linked list
def build_ll(nums):
    arr_to_ll = []

    arr_to_ll.append(ListNode(nums[0]))
    zero_node = arr_to_ll[0]

    for i in range(1, len(nums)):
        n = ListNode(nums[i], p=arr_to_ll[i-1])
        arr_to_ll[i-1].next = n
        arr_to_ll.append(n)
        if n.v == 0:
            zero_node = n

    arr_to_ll[0].prev = arr_to_ll[-1]
    arr_to_ll[-1].next = arr_to_ll[0]
    # head.prev = prev
    # prev.next = head

    return arr_to_ll, zero_node

def print_ll(head: 'ListNode'):
    pt = head
    line = f'{pt.v} -> '
    pt = pt.next
    while pt != head:
        line += f'{pt.v} -> '
        pt = pt.next
    print(line)

# print_ll(head)
# print(ptToNums)

def mix(arr_to_ll, times):
    for _ in range(times):
        for i in range(len(nums)):
            pt: ListNode = arr_to_ll[i]

            if pt.v != 0:

                pt.prev.next = pt.next
                pt.next.prev = pt.prev
                
                new_loc = pt
                if pt.v > 0:
                    for i in range(pt.v % (N-1)):
                        new_loc = new_loc.next
                else:
                    new_loc = new_loc.prev
                    for i in range((-pt.v) % (N-1)):
                        new_loc = new_loc.prev
                
                # print(f'move {pt} to between {new_loc.v} and {new_loc.next.v}')
                
                pt.next = new_loc.next
                pt.prev = new_loc
                
                new_loc.next.prev = pt
                new_loc.next = pt

total = 0

arr_to_ll, zero_node = build_ll(nums)
mix(arr_to_ll, 1)

v = zero_node
for i in range(3):
    v = v.shift(1000)
    total += v.v

print(f'20.1: {total}')
    
dec_key = 811589153
arr_to_ll, zero_node = build_ll(nums)
for i in range(N):
    arr_to_ll[i].v = (arr_to_ll[i].v * dec_key)

mix(arr_to_ll, 10)

total = 0
v = zero_node
for i in range(3):
    v = v.shift(1000)
    total += v.v
    
print(f'20.2: {total}')