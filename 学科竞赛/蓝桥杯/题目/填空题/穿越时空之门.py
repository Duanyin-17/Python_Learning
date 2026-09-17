# 2026/4/2 19:01

# print(pow(2,6)-1)
# 特殊题解

def ch_4(x):
    y=0
    while x!=0:
        y=y+x%4
        x=x//4
    return y

def ch_2(x):
    return sum(list(map(int,bin(x)[2:])))

count = 0

for i in range(1,2025):
    if ch_2(i) == ch_4(i):
        count+=1

print(count)









