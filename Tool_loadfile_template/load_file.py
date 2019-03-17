def load_entries():
    data = []
    with open('C:/Users/yo-ch/Desktop/color.txt', 'r', encoding='UTF-8') as f:
        for line in f.readlines():
            line = line.strip('\n')
            line = line.split(' ')
            print('line 0 is', line[0])
            print('line 1 is', line[1])
            data.append(line)
    print(data)

load_entries()
