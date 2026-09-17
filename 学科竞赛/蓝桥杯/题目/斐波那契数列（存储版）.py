
n = int(input())
get = [int(input()) for _ in range(n)]

fb = [0,1]
for i in range(2,max(get)+1):
    fb.append(fb[i-1]+fb[i-2])

for i in get:
    print(fb[i])