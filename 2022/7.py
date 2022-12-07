inputs = []

while True:
    try:
        text = input()
    except EOFError as ex:
        break
    inputs.append(text)

# print('\n'.join(inputs))

from typing import Dict
from dataclasses import dataclass

@dataclass
class FileSystem:
    Name: str
    Dirs: Dict[str, 'FileSystem']
    Files: Dict[str, 'FileSystem']
    Previous: 'FileSystem'
    Size: int
    
    def GetSize(self) -> int:
        size = 0
        for name, f in self.Files.items():
            f: FileSystem
            size += f.Size
        for name, d in self.Dirs.items():
            d: FileSystem
            size += d.GetSize()
        return size
        
    
root_fs = FileSystem('/', {}, {}, None, 0)
current_path = ''

current_fs = root_fs

i = 0
while i < len(inputs):
    line = inputs[i]
    
    if line[0] == '$':
        # command
        cmds = line.split(' ')
        if cmds[1] == 'cd':
            # cd
            if cmds[2] == '/':
                current_fs = root_fs
            elif cmds[2] == '..':
                current_fs = current_fs.Previous
            else:
                # cd into dir
                current_fs = current_fs.Dirs[cmds[2]]
        else:
            # ls
            j = i+1
            while j < len(inputs):
                line2 = inputs[j]
                if line2[0] == '$':
                    break
                
                fsize, fname = line2.split(' ')
                if fsize == 'dir':
                    # dir
                    current_fs.Dirs[fname] = FileSystem(fname, {}, {}, current_fs, 0)
                else:
                    # file
                    current_fs.Files[fname] = FileSystem(fname, {}, {}, current_fs, int(fsize))
                j += 1

        current_path = ''
    i += 1
    

total_size = 0

def print_size(fs: FileSystem):
    size = 0
    if fs.GetSize() <= 100000:
        size += fs.GetSize()
    
    # print(fs.Name, fs.GetSize())
    for _, fs in fs.Dirs.items():
        size += print_size(fs)

    return size

print(f'7.1: {print_size(root_fs)}')

at_least = 0

disk_size = 70000000
need_unused_size = 30000000
current_size = root_fs.GetSize()
current_free = disk_size - current_size
need_to_free = need_unused_size - current_free

# print(f'need to free: {need_unused_size - (current_free)}')

def get_file_sizes(fs: FileSystem) -> list:
    filesizes = []

    filesizes.append(fs.GetSize())
    
    for name, fs in fs.Dirs.items():
        filesizes.extend(get_file_sizes(fs))

    return filesizes

filesizes = sorted(get_file_sizes(root_fs))
# print(filesizes)

for fsize in filesizes:
    if fsize > need_to_free:
        print(f'7.2: {fsize}')
        break