import random

with open("keys.txt", "r") as f:
    keys = [row.strip() for row in f]
    random.shuffle(keys)


DELAY = (0, 100)  #настраиваем delay