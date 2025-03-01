
def format_id(i):
    if i < 10: i = str(f'000{i}')
    elif i < 100: i = str(f'00{i}')
    elif i < 1000: i = str(f'0{i}')
    elif i < 10000: i = str(f'{i}')
    else: i = str(f'-1')
    return i

