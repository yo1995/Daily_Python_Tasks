import sys
import os
from collections import Counter

if __name__ == '__main__':
    cwd = sys.path[0]
    stats = Counter()

    for root, dirs, files in os.walk(cwd):
        for file in files:
            stats[os.path.splitext(file)[1]] += 1

    print(stats)
