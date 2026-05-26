n = 10

def test():
    for i in range(n):
        print("ABCDEFGHIJ"[i], end=" ")
        yield i # return 후 일시 정지

x = test()

try:
    while True:
        print(next(x))
except StopIteration:
    print("모든 데이터 사용 완료")