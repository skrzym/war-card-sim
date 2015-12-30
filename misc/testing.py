thelist = {0: 10, 1: 20, 2: 30, 3: 5}
print thelist
print thelist.values()
print [val == max(thelist.values()) for val in thelist.values()].index(True)


