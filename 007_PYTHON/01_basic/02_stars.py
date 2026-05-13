print('*')
print('**')
print('***')
print('****')
print('*****')

print("="*30)
print(f"{' 성적표 ':=^25}")
print("="*30)

print('\n - 1 - ')
for i in range(1,6): # 1부터출발해서 6을 포함하지 않는것
    print("*" * i)

print('\n - 2 - ')
for i in range(1,6):
    print(" " * (5 - i), end="")   # 공백을 찍는 부분
    print("*" * i)         # * 을 찍는 부분
    # print(" " * (5 - i) + "*" * i)

print('\n - 3 - ')
for i in range(1,6):
    print(" " * (5 - i) + '*' * (2*i-1))

for i in range(1,10,2):
    print(f"{'*'*i: ^9}")