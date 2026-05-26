n = 10

def test():
    for i in range(n):
        yield i

x = test()

for i in range(n):
    print(next(x))