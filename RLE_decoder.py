from string import digits

def decode(rle):
    out = ""
    skip = 0
    for i, val in enumerate(rle):
        if skip > 0:
            skip -= 1
            continue
        if val not in digits:
            out += val
        else:
            num = ""
            for j, val2 in enumerate(rle[i:]):
                if val2 in digits:
                    num += val2
                else:
                    skip = j
                    for k in range(int(num)):
                        out += val2
                    break
    return out

def print_decoded(decoded):
    print()
    line = ""
    for i in decoded:
        if i == '!':
            print(line)
            break
        elif i == '$':
            print(line)
            line = ""
        else:
            line += i
